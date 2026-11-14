"""Export real catalog evidence only. This is not the deferred raster export stage."""
import csv
import json
import shutil
from pathlib import Path
from utils.catalog import pair_dates

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT/'data/manifests'
    output = ROOT/'web/public/data'
    output.mkdir(parents=True, exist_ok=True)
    summaries = json.loads((source/'coverage.json').read_text(encoding='utf-8'))
    features = []
    for city in summaries:
        slug = city['city']
        with (source/f'{slug}_selected.csv').open(encoding='utf-8') as f:
            selected = {r['scene'] for r in csv.DictReader(f)}
        # Export only catalog files from successful queries in the current run.
        queries = json.loads((source/f'{slug}_queries.json').read_text(encoding='utf-8'))
        for query in queries['queries']:
            if query['status'] != 'complete':
                continue
            maturity = query['parameters']['dataMaturity']
            catalog = json.loads((source/f'{slug}_{maturity.lower()}_catalog.json').read_text(encoding='utf-8'))
            for feature in catalog['features']:
                p = feature['properties']
                start, end = pair_dates(p['sceneName'])
                features.append({'type':'Feature','geometry':feature['geometry'],'properties':{
                    'city':slug,'scene':p['sceneName'],'track':p['pathNumber'],'frame':p['frameNumber'],
                    'direction':p['flightDirection'],'start':start,'end':end,'maturity':maturity,
                    'selected':p['sceneName'] in selected,'url':p['url']}})
        shutil.copy2(ROOT/f'reports/coverage_{slug}.md',output/f'coverage_{slug}.md')
    shutil.copy2(source/'coverage.json',output/'coverage.json')
    (output/'footprints.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},separators=(',',':')),encoding='utf-8')
    size = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    if size > 25_000_000:
        raise SystemExit('Web assets exceed the 25 MB budget')
    print(f'Exported {len(features)} actual catalog footprints for {len(summaries)} cities; {size:,} bytes. No measurement layers exported.')


if __name__ == '__main__':
    main()
