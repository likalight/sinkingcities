"""Search all five cities; preserve source metadata and reproducible coverage decisions."""
import argparse
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import asf_search as asf
import yaml
from shapely.geometry import box, shape
from utils.catalog import groups, pair_dates

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['city', 'maturity', 'scene', 'reference_date', 'secondary_date', 'track', 'frame',
          'direction', 'polarization', 'bandwidth', 'crid', 'processing_date', 'aoi_fraction',
          'url', 'bytes', 'md5']


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def search_city(item, maturities, start, end):
    slug, city = item
    aoi = box(*city['bbox'])
    rows, queries, errors = [], [], []
    output = ROOT / 'data' / 'manifests'
    output.mkdir(parents=True, exist_ok=True)
    for maturity in maturities:
        params = dict(dataset='NISAR', processingLevel='GUNW', dataMaturity=maturity,
                      intersectsWith=aoi.wkt, start=start, end=end)
        try:
            result = asf.search(**params)
            if not result.searchComplete:
                raise RuntimeError('ASF returned an incomplete search; no complete coverage claim is possible')
            geojson = result.geojson()
            (output / f'{slug}_{maturity.lower()}_catalog.json').write_text(json.dumps(geojson, indent=2), encoding='utf-8')
            queries.append({'parameters': params, 'count': len(result), 'status': 'complete'})
            for feature in geojson['features']:
                p = feature['properties']
                ref, sec = pair_dates(p['sceneName'])
                size = p.get('bytes', {}).get(p.get('fileName'), {}).get('bytes')
                rows.append(dict(city=slug, maturity=maturity, scene=p['sceneName'], reference_date=ref,
                    secondary_date=sec, track=p['pathNumber'], frame=p['frameNumber'], direction=p['flightDirection'],
                    polarization=','.join(p.get('mainBandPolarization') or []), bandwidth=','.join(p.get('rangeBandwidth') or []),
                    crid=p.get('crid', ''), processing_date=p.get('processingDate', ''),
                    aoi_fraction=round(shape(feature['geometry']).intersection(aoi).area/aoi.area, 6),
                    url=p['url'], bytes=size, md5=p.get('md5sum')))
        except Exception as exc:
            errors.append(f'{maturity}: {type(exc).__name__}: {exc}')
            queries.append({'parameters': params, 'status': 'failed', 'error': str(exc)})
    stamp = datetime.now(timezone.utc).isoformat()
    (output / f'{slug}_queries.json').write_text(json.dumps({'queried_at': stamp, 'queries': queries}, indent=2), encoding='utf-8')
    write_csv(output / f'{slug}.csv', rows)
    ranked = groups(rows)
    # Follow brief: prefer PROVISIONAL if any full-coverage continuous chain exists.
    preferred = [g for g in ranked if g['key'][0] == 'PROVISIONAL' and g['chain']]
    selected = next(iter(preferred or [g for g in ranked if g['chain']]), None)
    chain = selected['chain'] if selected else []
    write_csv(output / f'{slug}_selected.csv', chain)
    lines = [f'# Coverage: {city["name"]}', '', f'Queried UTC: {stamp}',
             f'Bounding box (EPSG:4326): `{city["bbox"]}`',
             f'Status: {"INCOMPLETE — one or more searches failed" if errors else "catalog search complete"}',
             f'Catalog granules returned: {len(rows)}. These are metadata records, not validated measurements.', '',
             '| Maturity | Track | Frame | Pass | Pol. | Bandwidth | CRID | Unique pairs | Date span | Longest full-AOI 12-day chain |',
             '|---|---:|---:|---|---|---|---|---:|---|---:|']
    for group in ranked:
        values = group['rows']
        span = min(r['reference_date'] for r in values) + ' to ' + max(r['secondary_date'] for r in values)
        lines.append('| ' + ' | '.join(map(str, group['key'])) + f' | {len(values)} | {span} | {len(group["chain"])} |')
    lines += ['', '## Candidate for inspection', '']
    if chain:
        lines += [f'Selected group: `{selected["key"]}`.',
                  f'{len(chain)} pairs, {chain[0]["reference_date"]} to {chain[-1]["secondary_date"]}.',
                  f'Total advertised HDF5 bytes: {sum(r["bytes"] or 0 for r in chain):,}.',
                  f'Manifest: `data/manifests/{slug}_selected.csv`.']
    else:
        lines += ['No eligible full-AOI 12-day chain found in successfully returned metadata.']
    lines += ['', '## Interpretation', '',
              'Ranking is within maturity, track, frame, pass, polarization, bandwidth and CRID. Duplicate date pairs retain the latest processing date. PROVISIONAL is preferred as requested.',
              'Full-AOI means at least 99% polygon overlap in longitude/latitude, a screening heuristic, not valid-pixel coverage. Dates are acquisition days; inspect exact acquisition epochs before processing.',
              'No gaps are bridged. Separate chains must not be concatenated without a network solution. No coherence, reference stability, or velocity has been assessed.',
              'Searches use ASF pagination without a maxResults cap. Acquisition bounds and complete source records are saved in data/manifests/.',
              '[ASF search documentation](https://nisar-docs.asf.alaska.edu/asf-search/)']
    if errors:
        lines += ['', '## Search errors', ''] + errors
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    (reports / f'coverage_{slug}.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    summary = {'city': slug, 'name': city['name'], 'bbox': city['bbox'], 'queried_at': stamp,
               'catalog_count': len(rows), 'search_complete': not errors, 'chain_pairs': len(chain),
               'selected_group': list(selected['key']) if selected else None,
               'start': chain[0]['reference_date'] if chain else None,
               'end': chain[-1]['secondary_date'] if chain else None, 'measurement_status': 'not_processed'}
    print(json.dumps(summary), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--city', default='all')
    parser.add_argument('--maturity', nargs='+', choices=['PROVISIONAL', 'VALIDATED', 'BETA'], default=['PROVISIONAL', 'VALIDATED'])
    parser.add_argument('--start', default='2026-06-17T00:00:00Z')
    parser.add_argument('--end', default='2026-11-14T04:38:00Z', help='Explicit cutoff; update for subsequent runs')
    args = parser.parse_args()
    cities = yaml.safe_load((ROOT/'config/cities.yaml').read_text(encoding='utf-8'))['cities']
    if args.city != 'all':
        if args.city not in cities:
            parser.error('Unknown city')
        cities = {args.city: cities[args.city]}
    with ThreadPoolExecutor(max_workers=5) as pool:
        summaries = list(pool.map(lambda item: search_city(item, args.maturity, args.start, args.end), cities.items()))
    (ROOT/'data/manifests/coverage.json').write_text(json.dumps(summaries, indent=2), encoding='utf-8')
    if any(not s['search_complete'] for s in summaries):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
