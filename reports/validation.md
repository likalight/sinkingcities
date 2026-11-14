# Scientific decision log

## Evidence status — 14 November 2026

Actual inputs inspected: ASF catalog metadata only. No HDF5 science granule, phase array, coherence array, DEM or projection array has been inspected. No displacement or velocity has been produced. No GNSS ground truth is present.

## Coverage decisions

- Search all five analyst-defined city boxes, initially 17 June–14 November 2026. Save exact query cutoff and responses.
- Search PROVISIONAL and VALIDATED independently; prefer an eligible PROVISIONAL chain as requested. Do not mix maturities, tracks, frames, directions, polarizations, bandwidths or CRIDs.
- Select consecutive 12-day acquisition-date edges. Never bridge missing observations. Duplicate pairs retain the latest processing date.
- Require 99% bounding-box footprint overlap for the initial candidate chain. This is a conservative geometric heuristic in geographic coordinates, not coherent-pixel coverage. Refine land-only AOIs or jointly inspect neighboring frames before rejecting a city.
- Semarang is the first inspection candidate; primary target Jakarta remains under consideration. No coherence-based city choice has been made.
- The selected Semarang chain covers 60 days, not five months. Its descending and ascending groups require separate processing before any decomposition.

## Gates before conversion

| Decision | Status |
|---|---|
| Actual HDF5 paths and shapes | TODO: run stage 03 on authenticated product |
| Phase, coherence, component and ionosphere grids aligned | TODO: inspect dimensions, axes, projection, spacing, fill values and units |
| Wavelength | TODO: read metadata; if only center frequency exists, derive from c/f and record source path and units |
| Interferogram/sign convention | TODO: verify GUNW specification and reference/secondary order before choosing ± λ/(4π) |
| Ionosphere | Required; product includes a screen that is not applied by default; confirm sign and units before subtraction |
| Coherence threshold | Initial hypothesis 0.3, not calibrated or applied; report sensitivity to threshold |
| Components | Select a nonzero connected component containing the reference area for each pair; do not independently reference disjoint islands |
| Reference polygon | TODO: literature justification and high coherence across all included dates; do not assume inland means stable |
| Common grid and pixels | TODO: crop in a consistent projected CRS; mask nodata; no interpolation across invalid components |
| Troposphere and tides | TODO: inspect included correction lookup tables and document what remains unapplied |

Source: [ASF GUNW guide](https://nisar-docs.asf.alaska.edu/gunw/). The [linked product specification](https://nisar.asf.earthdatacloud.nasa.gov/NISAR-SAMPLE-DATA/DOCS/NISAR_D-102272_RevE_NASA_SDS_Product_Specification_L2_GUNW_Nov8_2024_w-sigs.pdf) could not be retrieved through web search in this session; sign convention remains unresolved.

## Time series and uncertainty

Use only connected temporal chains on pixels valid throughout the required edges, or a documented network solver. Shared acquisitions create correlated errors. A linear fit on cumulative values does not automatically give independent observations.

Report velocity in cm/year and residual scatter in cm separately. A residual standard deviation is **not** a velocity uncertainty. Any displayed velocity ± uncertainty needs a slope-error estimator with cm/year units and documented statistical assumptions. A short chain can alias seasonal motion and atmospheric delay; do not label a two-month fitted trend a confirmed annual rate.

LOS is not vertical. Single-orbit vertical approximation requires a verified sign convention and incidence angle, with an explicit negligible-horizontal-motion assumption. Two-orbit vertical/east decomposition additionally assumes or constrains northward motion and needs heading/look-vector geometry plus compatible spatial and temporal referencing.

## Literature comparison

| Area and source | Published evidence | Our comparison |
|---|---|---|
| Jakarta, [Abidin et al. 2015](https://piahs.copernicus.org/articles/372/115/2015/) | Typical historical rates 3–10 cm/year; observations reviewed span 1974–2010 | TODO: no measured rates; periods do not overlap |
| Semarang, [Abidin et al.](https://www.tandfonline.com/doi/pdf/10.1080/19475705.2012.692336) | Relevant study identified; location-specific numeric extraction remains TODO | TODO: no measured rates |

Agreement with an old citywide range would be a plausibility check, not independent validation. Compare matching locations and definitions, and retain disagreements. Do not assign the historical Jakarta range to Semarang or other cities.

## Relative sea-level scenario

AR6 local total projections can include vertical-land-motion terms. Inspect the selected product components before adding NISAR-derived subsidence to avoid double counting. Align the projection baseline with the NISAR observation epoch; a 2050 anomaly relative to 1995–2014 cannot simply be presented as additional rise since 2026.

For positive-down subsidence s and a consistently rebased ocean component, scenario change is ocean change + s × elapsed years. Convert cm to metres explicitly. This assumes constant subsidence and is not a prediction. Reference-area uncertainty and short-trend extrapolation dominate many local interpretations.

NASADEM is not automatically a bare-earth, present-day, tidal-datum DEM. Check source epoch, vertical datum, urban/vegetation bias and accuracy. A low-elevation mask is not a hydrodynamic flood model; levees, tides, drainage and connectivity matter. No inundation or exposure numbers will be published without these checks.

## Go/no-go gate

Saturday 14 November 20:00 SGT: if no plausible, coherent, properly referenced velocity result exists, evaluate the requested GCOV flood fallback. That fallback still requires actual before/after data, compatible acquisition geometry and polarization, an independently documented event and validation. Authentication failure does not prove GUNW scientifically unusable. Do not switch early or invent a flood result.
