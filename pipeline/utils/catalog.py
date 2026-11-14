"""Catalog-only decisions; never treat footprint coverage as coherence."""
import re
from collections import defaultdict
from datetime import datetime


def pair_dates(name):
    stamps = re.findall(r"\d{8}T\d{6}", name)
    if len(stamps) != 4:
        raise ValueError(f"Expected four acquisition timestamps in GUNW name: {name}")
    dates = [datetime.strptime(s, "%Y%m%dT%H%M%S") for s in stamps]
    if not dates[0] <= dates[1] < dates[2] <= dates[3]:
        raise ValueError(f"Invalid acquisition ordering: {name}")
    return dates[0].date().isoformat(), dates[2].date().isoformat()


def longest_chain(rows):
    """Longest connected directed chain of 12-day edges; never bridge gaps."""
    best = {}
    for row in sorted(rows, key=lambda r: (r['secondary_date'], r['reference_date'])):
        start, end = row['reference_date'], row['secondary_date']
        if (datetime.fromisoformat(end) - datetime.fromisoformat(start)).days != 12:
            continue
        candidate = best.get(start, []) + [row]
        if len(candidate) > len(best.get(end, [])):
            best[end] = candidate
    return max(best.values(), key=len, default=[])


def groups(rows):
    grouped = defaultdict(list)
    for row in rows:
        key = tuple(row[k] for k in ('maturity', 'track', 'frame', 'direction', 'polarization', 'bandwidth', 'crid'))
        grouped[key].append(row)
    result = []
    for key, values in grouped.items():
        # Multiple revisions of the same pair must not inflate coverage counts.
        unique = {}
        for row in sorted(values, key=lambda r: r['processing_date']):
            unique[(row['reference_date'], row['secondary_date'])] = row
        values = list(unique.values())
        full = [r for r in values if r['aoi_fraction'] >= 0.99]
        chain = longest_chain(full)
        result.append({'key': key, 'rows': values, 'chain': chain})
    return sorted(result, key=lambda g: (len(g['chain']), len(g['rows'])), reverse=True)
