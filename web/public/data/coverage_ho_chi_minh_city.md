# Coverage: Ho Chi Minh City

Queried UTC: 2026-11-14T04:42:28.644677+00:00
Bounding box (EPSG:4326): `[106.5, 10.3, 107.0, 11.0]`
Status: catalog search complete
Catalog granules returned: 17. These are metadata records, not validated measurements.

| Maturity | Track | Frame | Pass | Pol. | Bandwidth | CRID | Unique pairs | Date span | Longest full-AOI 12-day chain |
|---|---:|---:|---|---|---|---|---:|---|---:|
| PROVISIONAL | 47 | 83 | DESCENDING | HH | 40 | P05023 | 9 | 2026-06-17 to 2026-10-15 | 5 |
| PROVISIONAL | 155 | 7 | ASCENDING | HH | 40 | P05023 | 7 | 2026-06-24 to 2026-10-10 | 5 |

## Candidate for inspection

Selected group: `('PROVISIONAL', 47, 83, 'DESCENDING', 'HH', '40', 'P05023')`.
5 pairs, 2026-08-16 to 2026-10-15.
Total advertised HDF5 bytes: 11,723,079,680.
Manifest: `data/manifests/ho_chi_minh_city_selected.csv`.

## Interpretation

Ranking is within maturity, track, frame, pass, polarization, bandwidth and CRID. Duplicate date pairs retain the latest processing date. PROVISIONAL is preferred as requested.
Full-AOI means at least 99% polygon overlap in longitude/latitude, a screening heuristic, not valid-pixel coverage. Dates are acquisition days; inspect exact acquisition epochs before processing.
No gaps are bridged. Separate chains must not be concatenated without a network solution. No coherence, reference stability, or velocity has been assessed.
Searches use ASF pagination without a maxResults cap. Acquisition bounds and complete source records are saved in data/manifests/.
[ASF search documentation](https://nisar-docs.asf.alaska.edu/asf-search/)
