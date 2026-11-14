# Coverage: Semarang

Queried UTC: 2026-11-14T04:42:28.233411+00:00
Bounding box (EPSG:4326): `[110.25, -7.1, 110.55, -6.85]`
Status: catalog search complete
Catalog granules returned: 18. These are metadata records, not validated measurements.

| Maturity | Track | Frame | Pass | Pol. | Bandwidth | CRID | Unique pairs | Date span | Longest full-AOI 12-day chain |
|---|---:|---:|---|---|---|---|---:|---|---:|
| PROVISIONAL | 162 | 92 | DESCENDING | HH | 40 | P05023 | 8 | 2026-06-25 to 2026-10-11 | 5 |
| PROVISIONAL | 154 | 174 | ASCENDING | HH | 40 | P05023 | 8 | 2026-06-24 to 2026-10-10 | 5 |

## Candidate for inspection

Selected group: `('PROVISIONAL', 162, 92, 'DESCENDING', 'HH', '40', 'P05023')`.
5 pairs, 2026-08-12 to 2026-10-11.
Total advertised HDF5 bytes: 11,316,232,192.
Manifest: `data/manifests/semarang_selected.csv`.

## Interpretation

Ranking is within maturity, track, frame, pass, polarization, bandwidth and CRID. Duplicate date pairs retain the latest processing date. PROVISIONAL is preferred as requested.
Full-AOI means at least 99% polygon overlap in longitude/latitude, a screening heuristic, not valid-pixel coverage. Dates are acquisition days; inspect exact acquisition epochs before processing.
No gaps are bridged. Separate chains must not be concatenated without a network solution. No coherence, reference stability, or velocity has been assessed.
Searches use ASF pagination without a maxResults cap. Acquisition bounds and complete source records are saved in data/manifests/.
[ASF search documentation](https://nisar-docs.asf.alaska.edu/asf-search/)
