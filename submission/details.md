# Project details — current prototype draft

## What works

A static Vite/TypeScript/MapLibre app displays NASA NISAR acquisition footprints for Jakarta, Semarang, Bangkok, Manila and Ho Chi Minh City. Users can change city, toggle footprints and study-area boundaries, inspect product dates and provenance, read coverage reports and follow a five-step explanation of the intended scientific workflow.

The Python pipeline queries ASF using `asf_search`, saves source metadata and manifests, groups compatible products, removes duplicate pairs and identifies continuous 12-day chains. Download tooling uses local Earthdata credentials, retains partial transfers for retry and verifies product size and HDF5 readability. An inspection tool prints the actual HDF5 tree and candidate metadata without assuming paths.

The 14 November search returned 157 catalog records. The selected Semarang sequence has five pairs from 12 August to 11 October 2026. These are catalog findings, not subsidence measurements. Authentication is pending; no radar science arrays have been processed.

## NASA data actually used

- **NASA–ISRO NISAR L2 GUNW catalog metadata, distributed by ASF DAAC.** Used fields include acquisition times, footprints, orbit direction, track/frame, polarization, maturity, processing version and product links. Saved query parameters and responses allow every coverage number to be traced. [Product guide](https://nisar-docs.asf.alaska.edu/gunw/) · [Search method](https://nisar-docs.asf.alaska.edu/asf-search/).
- **NASA NISAR documentation.** Used to design the quality-control and correction gates. The app does not claim catalog metadata alone completes the challenge's surface-change objective.

## Planned NASA inputs, not yet used in results

- [NASA/IPCC AR6 Sea Level Projection Tool](https://sealevel.nasa.gov/data_tools/17/): local SSP2-4.5 and SSP5-8.5 scenarios, after baseline and land-motion accounting.
- [NASADEM HGT v001](https://www.earthdata.nasa.gov/data/catalog/lpcloud-nasadem-hgt-001): elevation context after datum and accuracy checks.

## Method to complete

Inspect actual GUNW arrays; mask low coherence and incompatible connected components; apply the ionospheric correction; read wavelength; establish the product's sign convention; reference each pair to a justified stable area; chain connected dates; and estimate velocity with explicitly labeled uncertainty. Single-orbit LOS estimates will not be described as measured vertical motion. Compare matching locations against literature and independent observations when available.

## Tools and complementary sources

Python 3.11, asf_search, earthaccess, h5py, NumPy, PyYAML, Shapely, Requests, pytest, TypeScript, Vite and MapLibre GL JS. OpenStreetMap and CARTO provide contextual basemap tiles. Google Fonts provides DM Sans and Manrope. These are complements, not NASA datasets. [Jakarta historical research](https://piahs.copernicus.org/articles/372/115/2015/) supplies motivation, not current measurements.

## AI assistance disclosure

The participant supplied the SinkingCities concept and scientific brief. OpenAI Codex assisted with code, tests, source research and draft writing. NASA catalog records were retrieved from ASF; no AI-generated values are represented as observations. Synthetic unit-test fixtures are isolated from the app's data. Human review and scientific validation remain necessary.

## Limits and next steps

No validated velocity or coherence result yet; no GNSS data; short continuous sequences; unknown reference stability; unresolved sign convention until product inspection; unmodeled atmospheric effects. Next milestone: authenticate and inspect one real Semarang GUNW granule. Broader goals include validated displacement, uncertainty maps and carefully constructed relative sea-level scenarios.

## Team and links

Team name: TODO — participant input required.
Member names: TODO — participant input required.
Public project and demo links: TODO — verify deployment before submission.
The project has not been submitted for judging.
