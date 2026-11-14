# SinkingCities

**Watching Southeast Asia's coastal cities change, from orbit, through the clouds.**

NASA Space Apps Challenge 2026 · Singapore · [Dancing with the SARs](https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/)

## Current status: coverage prototype, not measured subsidence

The app visualizes real NASA–ISRO NISAR catalog footprints and acquisition dates for five coastal cities. It does **not yet measure surface displacement**. Downloading and inspecting authenticated GUNW arrays is the next gate. No velocity, coherence, uncertainty, population exposure or 2050 sea-level values have been fabricated.

Catalog snapshot: 14 November 2026, approximately 12:42 SGT. Query cutoff: 12:38 SGT. Source responses, query parameters and selected product lists are preserved in `data/manifests/`.

| Study region | Catalog granules | Longest selected full-box 12-day chain |
|---|---:|---:|
| North Jakarta | 32 | 1 pair |
| Semarang | 18 | 5 pairs |
| Bangkok | 47 | 0 pairs |
| Manila | 43 | 5 pairs |
| Ho Chi Minh City | 17 | 5 pairs |

These counts come from `pipeline/01_search.py`, not published subsidence estimates. They depend on analyst-selected search boxes. Jakarta's box crosses frame boundaries; Bangkok's result is not a claim that no usable data exist. See the city coverage reports for tracks, frames, passes, dates and selection rules.

**First inspection candidate:** Semarang, PROVISIONAL track 162/frame 92, descending HH, five pairs from 12 August to 11 October 2026. Coherence and stable-reference availability remain unknown. A two-month continuous chain must not be described as five months of measurements.

## Why this problem matters

Subsidence can compound rising sea levels in coastal communities. Historical surveys in Jakarta reported spatially and temporally varying subsidence, with typical rates around 3–10 cm/year over the study periods. Those historical findings motivate this project; they are **not** 2026 NISAR results. [Abidin et al., 2015](https://piahs.copernicus.org/articles/372/115/2015/).

NISAR offers repeat radar observations through clouds. Its long L-band wavelength can help observe vegetated landscapes, but does not guarantee coherence or remove atmospheric and ionospheric errors. [NASA mission overview](https://science.nasa.gov/mission/nisar/).

## NASA sources and their actual role

| Source | Used now | Intended next use |
|---|---|---|
| [NISAR L2 GUNW / ASF DAAC](https://nisar-docs.asf.alaska.edu/gunw/) | Catalog metadata, footprints, acquisition dates, product availability | Corrected and referenced LOS time series |
| [ASF search API documentation](https://nisar-docs.asf.alaska.edu/asf-search/) | Reproducible searches of PROVISIONAL and VALIDATED collections | Repeatable updates |
| [NASA/IPCC AR6 Sea Level Projection Tool](https://sealevel.nasa.gov/data_tools/17/) | Method planning only | Coastal SSP2-4.5 and SSP5-8.5 scenarios |
| [NASADEM HGT v001](https://www.earthdata.nasa.gov/data/catalog/lpcloud-nasadem-hgt-001) | Not downloaded | Elevation context after vertical-datum checks |

OpenStreetMap/CARTO provide a non-NASA basemap. Do not claim the planned NASA products were already incorporated. A completed surface-change analysis is still required to demonstrate the central challenge objective.

## Run locally

Python 3.11:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python pipeline/01_search.py
python pipeline/02_download.py --city semarang --dry-run
python pipeline/02_download.py --city semarang --limit 1
python pipeline/03_inspect.py data/raw/semarang/ACTUAL_PRODUCT_NAME.h5
python pipeline/export_catalog.py
```

The last inspection argument must be the real downloaded filename printed by stage 02. Stage 02 requires a local `~/.netrc` Earthdata entry for `urs.earthdata.nasa.gov`. It never requests credentials in source files or command-line arguments. Raw products and partial downloads are gitignored. The first selected Semarang granule is approximately 2.27 GB; the selected five-pair chain is approximately 11.32 GB, based on ASF metadata.

```powershell
cd web
npm ci
npm run dev
npm run build
```

The static output is `web/dist/`. Relative asset paths support GitHub Pages project URLs. No backend or NASA credentials are shipped to the browser. Map tiles and fonts require network access.

## Processing gates

Stages 01–03 are implemented. Stage 02 dry-run succeeds but authenticated download is blocked until Earthdata credentials are configured. Stage 03 has not been run against a NASA granule. Downstream stages 04–08 are deliberately deferred until actual HDF5 paths, shapes, CRS and metadata have been inspected, as required by the project brief. See `pipeline/ROADMAP.md` and `reports/validation.md`.

The web app has working catalog map, city selector, layer toggles, source-record inspector, provenance panel and guided story. Measurement layers are unavailable and explicitly labeled. This is not a completed P0 subsidence application.

## Verification

Six catalog tests pass: acquisition-date parsing, malformed names, gap handling, 12-day filtering, duplicate removal and partial-footprint exclusion. TypeScript checking and the Vite production build pass. Web data export contains 157 actual catalog footprint records and initially totals 137,208 bytes. Browser verification and public URL status are recorded in `reports/verification.md`.

## Attribution and AI assistance

The project concept and scientific brief were supplied by the participant. OpenAI Codex assisted with implementation, source research, documentation and test generation. Catalog data originate from ASF/NASA–ISRO, not AI generation. Test fixtures are synthetic and never presented as scientific observations. No NASA logos or generated NASA branding are used. Third-party dependencies retain their own licenses.

Submission drafts in `submission/` describe the current prototype honestly. They are not a claim that the hackathon project has been submitted or is scientifically complete.
