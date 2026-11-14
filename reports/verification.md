# Verification record

- Python 3.11.15 installed in the task's isolated work directory; project virtual environment also lives there. System Python launcher was unusable.
- `01_search.py`: successful real network query across all five cities, PROVISIONAL and VALIDATED collections, 14 November 2026. Saved raw catalog responses, exact query arguments, CSV manifests, coverage reports and candidate chains.
- `02_download.py --dry-run`: one selected Semarang granule, 2,269,118,464 advertised bytes. Real invocation exits with an explicit missing-netrc blocker. No authenticated download has been claimed.
- `03_inspect.py --help`: succeeds. Synthetic unit fixture checks arbitrary-path discovery, shapes, attributes and scalar metadata. No NASA science granule inspected yet.
- `export_catalog.py`: 157 real catalog footprint records; initial exported data size 137,208 bytes. The 25 MB cap is enforced.
- Seven pytest checks pass (catalog logic plus synthetic HDF5 inspection). Test fixtures are not scientific observations.
- TypeScript and production Vite build pass. MapLibre produces a bundle-size advisory; the initial compressed JavaScript is approximately 295 kB.
- The in-app browser could not reach the local preview server. The public deployment was subsequently tested in the browser: city selection, data/limitations dialog, story navigation and footprint click all worked.
- Browser QA found two issues: the initial CARTO tiles required an API key, and MapLibre 6 required an explicitly bundled worker. Fixed with OpenStreetMap standard tiles and a Vite worker asset; rechecked actual map rendering and a real Semarang product's source details.
- Public deployment succeeded for commit `fe2b6a1` at the initially selected account, likalight1. The participant corrected the owner to likalight and accepted the transfer. GitHub now confirms the correct owner and Pages URL https://likalight.github.io/sinkingcities/. Redeployment follows the transfer; the old Pages URL is not the final link.
- The seven-test run initially encountered the sandbox's inaccessible temporary directory. Rerunning with an explicit workspace-local pytest base directory passed all seven tests.
