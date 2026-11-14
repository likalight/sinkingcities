# Coverage: North Jakarta

Queried UTC: 2026-11-14T04:42:28.630156+00:00
Bounding box (EPSG:4326): `[106.65, -6.25, 107.05, -5.9]`
Status: catalog search complete
Catalog granules returned: 32. These are metadata records, not validated measurements.

| Maturity | Track | Frame | Pass | Pol. | Bandwidth | CRID | Unique pairs | Date span | Longest full-AOI 12-day chain |
|---|---:|---:|---|---|---|---|---:|---|---:|
| PROVISIONAL | 10 | 174 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-26 to 2026-10-12 | 1 |
| PROVISIONAL | 18 | 92 | DESCENDING | HH | 40 | P05023 | 8 | 2026-06-27 to 2026-10-13 | 0 |
| PROVISIONAL | 18 | 91 | DESCENDING | HH | 40 | P05023 | 8 | 2026-06-27 to 2026-10-13 | 0 |
| PROVISIONAL | 10 | 175 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-26 to 2026-10-12 | 0 |

## Candidate for inspection

Selected group: `('PROVISIONAL', 10, 174, 'ASCENDING', 'HH', '40', 'P05023')`.
1 pairs, 2026-06-26 to 2026-07-08.
Total advertised HDF5 bytes: 2,315,255,808.
Manifest: `data/manifests/jakarta_selected.csv`.

## Interpretation

Ranking is within maturity, track, frame, pass, polarization, bandwidth and CRID. Duplicate date pairs retain the latest processing date. PROVISIONAL is preferred as requested.
Full-AOI means at least 99% polygon overlap in longitude/latitude, a screening heuristic, not valid-pixel coverage. Dates are acquisition days; inspect exact acquisition epochs before processing.
No gaps are bridged. Separate chains must not be concatenated without a network solution. No coherence, reference stability, or velocity has been assessed.
Searches use ASF pagination without a maxResults cap. Acquisition bounds and complete source records are saved in data/manifests/.
[ASF search documentation](https://nisar-docs.asf.alaska.edu/asf-search/)
