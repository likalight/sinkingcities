# Verification record

- Python 3.11.15 installed in the task's isolated work directory; project virtual environment also lives there. System Python launcher was unusable.
- `01_search.py`: successful real network query across all five cities, PROVISIONAL and VALIDATED collections, 14 November 2026. Saved raw catalog responses, exact query arguments, CSV manifests, coverage reports and candidate chains.
- `02_download.py --dry-run`: one selected Semarang granule, 2,269,118,464 advertised bytes. Real invocation exits with an explicit missing-netrc blocker. No authenticated download has been claimed.
- `03_inspect.py --help`: succeeds. Synthetic unit fixture checks arbitrary-path discovery, shapes, attributes and scalar metadata. No NASA science granule inspected yet.
- `export_catalog.py`: 157 real catalog footprint records; initial exported data size 137,208 bytes. The 25 MB cap is enforced.
- Seven pytest checks pass (catalog logic plus synthetic HDF5 inspection). Test fixtures are not scientific observations.
- TypeScript and production Vite build pass. MapLibre produces a bundle-size advisory; the initial compressed JavaScript is approximately 295 kB.
- The in-app browser could not reach the local preview server. Browser checks of the deployed app remain pending; local build success is not a substitute for visual QA.
- Public deployment: pending.
