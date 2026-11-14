# Remaining pipeline after authenticated inspection

These stages are intentionally not implemented against assumed product paths.

1. `04_extract.py`: consume an explicit inspected layer mapping; reject ambiguous paths, incompatible grids, unknown CRS/units and fill values. Clip windows before reading large arrays. Save per-pair GeoTIFFs and complete provenance.
2. `05_timeseries.py`: mask coherence and connected components, subtract validated ionosphere screen, convert using metadata wavelength and verified sign, reference to a documented stable polygon, chain without gaps, fit velocity and separately report residual scatter and slope uncertainty. Preserve valid counts and source dates.
3. `06_sealevel.py`: ingest actual NASA AR6 SSP2-4.5/SSP5-8.5 projections, record station and baseline, resolve embedded vertical motion, align DEM datum and output a clearly labeled scenario.
4. `07_hotspots.py`: derive polygons in a metric CRS, calculate area and valid-pixel statistics, and use verified landmark sources. No threshold can be claimed as validated before inspecting rates and uncertainty.
5. `08_export_web.py`: produce COGs, reprojected colorized overlays with transparent nodata and EPSG:4326 bounds, sampled-cell time series, and GeoJSON. Mark samples as samples; clicking outside coverage must return no data. Enforce the 25 MB asset budget.

`export_catalog.py` is a separate working exporter for the current evidence prototype; it does not replace the raster export stage.
