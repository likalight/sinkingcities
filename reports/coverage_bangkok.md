# Coverage: Bangkok

Queried UTC: 2026-11-14T04:42:28.787766+00:00
Bounding box (EPSG:4326): `[100.3, 13.45, 100.9, 14.0]`
Status: catalog search complete
Catalog granules returned: 47. These are metadata records, not validated measurements.

| Maturity | Track | Frame | Pass | Pol. | Bandwidth | CRID | Unique pairs | Date span | Longest full-AOI 12-day chain |
|---|---:|---:|---|---|---|---|---:|---|---:|
| PROVISIONAL | 112 | 9 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-21 to 2026-10-19 | 0 |
| PROVISIONAL | 112 | 8 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-21 to 2026-10-19 | 0 |
| PROVISIONAL | 4 | 82 | DESCENDING | HH | 40 | P05023 | 8 | 2026-06-26 to 2026-10-12 | 0 |
| PROVISIONAL | 4 | 81 | DESCENDING | HH | 40 | P05023 | 8 | 2026-06-26 to 2026-10-12 | 0 |
| PROVISIONAL | 11 | 9 | ASCENDING | HH | 40 | P05023 | 7 | 2026-07-08 to 2026-10-12 | 0 |
| PROVISIONAL | 11 | 8 | ASCENDING | HH | 40 | P05023 | 7 | 2026-07-08 to 2026-10-12 | 0 |

## Candidate for inspection

No eligible full-AOI 12-day chain found in successfully returned metadata.

## Interpretation

Ranking is within maturity, track, frame, pass, polarization, bandwidth and CRID. Duplicate date pairs retain the latest processing date. PROVISIONAL is preferred as requested.
Full-AOI means at least 99% polygon overlap in longitude/latitude, a screening heuristic, not valid-pixel coverage. Dates are acquisition days; inspect exact acquisition epochs before processing.
No gaps are bridged. Separate chains must not be concatenated without a network solution. No coherence, reference stability, or velocity has been assessed.
Searches use ASF pagination without a maxResults cap. Acquisition bounds and complete source records are saved in data/manifests/.
[ASF search documentation](https://nisar-docs.asf.alaska.edu/asf-search/)
