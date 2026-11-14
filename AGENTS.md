# SinkingCities — agent rules
Project: NASA Space Apps 2026 "Dancing with the SARs". NISAR InSAR subsidence + relative sea-level rise for SEA coastal cities. Primary city: Jakarta.
Deadline: Sun 15 Nov 2026 23:59 SGT (target submit 22:00).

- Python pipeline in pipeline/ (numbered scripts, run in order). Static MapLibre web app in web/.
- Data: NISAR L2 GUNW from ASF (asf_search/earthaccess). Earthdata creds via ~/.netrc ONLY, never in code or git.
- Never hardcode HDF5 paths: inspect the granule first (pipeline/03_inspect.py).
- Read wavelength, incidence angle and sign convention from product metadata/spec; document them in reports/validation.md.
- Apply the coherence mask + connected-component mask + ionospheric correction. Reference to a stable area.
- LOS is not vertical: label approximations.
- No invented numbers or citations. Unknown = TODO.
- Raw data in data/raw/ (gitignored). Only small derived assets in web/public/data/.
- Run and verify after every step. Small commits with clear messages.
- Fallback at Sat 20:00 SGT if no usable velocity map: NISAR GCOV flood change detection, same app shell.
