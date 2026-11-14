# Coverage: Manila

Queried UTC: 2026-11-14T04:42:28.659844+00:00
Bounding box (EPSG:4326): `[120.8, 14.3, 121.2, 14.85]`
Status: catalog search complete
Catalog granules returned: 43. These are metadata records, not validated measurements.

| Maturity | Track | Frame | Pass | Pol. | Bandwidth | CRID | Unique pairs | Date span | Longest full-AOI 12-day chain |
|---|---:|---:|---|---|---|---|---:|---|---:|
| PROVISIONAL | 32 | 81 | DESCENDING | HH | 40 | P05023 | 8 | 2026-06-28 to 2026-10-14 | 5 |
| PROVISIONAL | 140 | 9 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-23 to 2026-10-09 | 5 |
| VALIDATED | 140 | 9 | ASCENDING | HH | 40 | P05036 | 1 | 2026-10-09 to 2026-10-21 | 1 |
| PROVISIONAL | 133 | 81 | DESCENDING | HH | 20 | P05023 | 9 | 2026-06-23 to 2026-10-21 | 0 |
| PROVISIONAL | 133 | 81 | DESCENDING | HH | 40 | P05023 | 9 | 2026-06-23 to 2026-10-21 | 0 |
| PROVISIONAL | 39 | 9 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-28 to 2026-10-14 | 0 |

## Candidate for inspection

Selected group: `('PROVISIONAL', 32, 81, 'DESCENDING', 'HH', '40', 'P05023')`.
5 pairs, 2026-08-15 to 2026-10-14.
Total advertised HDF5 bytes: 11,672,748,032.
Manifest: `data/manifests/manila_selected.csv`.

## Interpretation

Ranking is within maturity, track, frame, pass, polarization, bandwidth and CRID. Duplicate date pairs retain the latest processing date. PROVISIONAL is preferred as requested.
Full-AOI means at least 99% polygon overlap in longitude/latitude, a screening heuristic, not valid-pixel coverage. Dates are acquisition days; inspect exact acquisition epochs before processing.
No gaps are bridged. Separate chains must not be concatenated without a network solution. No coherence, reference stability, or velocity has been assessed.
Searches use ASF pagination without a maxResults cap. Acquisition bounds and complete source records are saved in data/manifests/.
[ASF search documentation](https://nisar-docs.asf.alaska.edu/asf-search/)
