# volcanic-eruptions

Hand-curated catalog of VEI ≥ 5 volcanic eruptions since 1500 CE, plus a handful of notable VEI 4 events with major societal impact (Pelée, Eyjafjallajökull).

Parallel in spirit to `earthquakes`, `spaceweather`, `famines-tracking`, `flood-data`.

## Quick findings

- **28 VEI≥5 eruptions since 1500**; **8 VEI≥6** and **1 VEI≥7** (1815 Tambora).
- **Mean inter-VEI≥6 interval = 58.7 years** (~once per long generation). The 155-year gap 1660 → 1815 is the longest in the catalog; the 1815–1991 stretch had 5 VEI≥6 events at ~35-year cadence.
- **Tambora 1815** is the only VEI 7 in recorded history — caused the global "Year Without Summer" of 1816 and contributed to several famines (incl. one in this catalog).
- **VEI 5 occurs on average every ~20 years** in the modern era, but with strong clustering (1980 St Helens, 1982 El Chichón, 1991 Pinatubo, 1991 Cerro Hudson, 1991 was a major year, then a quiet 2000s–2010s, then 2022 Hunga Tonga).
- **Most VEI≥5 eruptions have low death tolls** (single-digit thousands or less); the high-fatality outliers (Krakatau, Tambora, Mt Pelée) killed mostly via tsunamis or pyroclastic flows reaching coastal populations.

See `plots/` for the four charts.

## What's in it

`volcanoes.csv` — columns:

- `year`, `month` — eruption start
- `name` — primary volcano name
- `country_region`
- `vei` — Volcanic Explosivity Index. **5 is the detection-clean band globally back to 1500**; VEI 4 is included sparingly for notable high-impact events
- `deaths_estimate` — published estimates (often dominated by tsunamis or lahars, not the eruption itself)
- `sources_notes`

Coverage: 1500 → 2022 (Hunga Tonga). Major events include:

- 1600 Huaynaputina (largest South American)
- 1815 Tambora (largest in recorded history, VEI 7, "Year Without Summer" 1816)
- 1883 Krakatau (VEI 6, ~36k deaths via tsunami)
- 1902 Pelée (29k deaths despite "only" VEI 4)
- 1912 Novarupta (largest 20th C)
- 1980 Mt St Helens
- 1991 Pinatubo (~0.5°C global cooling)
- 2022 Hunga Tonga (largest atmospheric blast since 1883)

## Plots

`make_plots.py` generates four standalone analytical plots:

### `plots/01_vei_timeline.png`
VEI vs year scatter, bubble size ∝ √deaths, red highlights VEI≥6. Big names (Tambora, Krakatau, Pinatubo, etc.) annotated.

### `plots/02_decadal_counts_by_vei.png`
Stacked bars: eruptions per decade by VEI band (5, 6, 7+). Catalog starts 1500.

### `plots/03_great_eruption_timing.png`
Cumulative VEI≥6 count vs constant-rate reference line (0.016/yr ≈ once per 61yr) + inter-event interval bar chart. Shows the 155-yr gap 1660→1815 and the relatively even cadence afterward.

### `plots/04_vei_distribution.png`
VEI histogram + semi-log survival curve. Each step up in VEI is roughly a 10× decrease in count, matching the canonical Gutenberg-Richter analog.

## Detection-bias notes

| Band | Coverage |
|---|---|
| VEI ≥ 7 | Detection-clean for several millennia (each event leaves a global tephra layer) |
| VEI ≥ 6 | Detection-clean back to ~1500 globally |
| VEI ≥ 5 | Detection-clean back to ~1500 for populated regions; remote events (Aleutians, Kamchatka, Southern Andes) may be undercounted pre-1850 |
| VEI ≤ 4 | Heavy completeness gaps pre-1900; only included if high-impact |

For the correlations work, use VEI ≥ 5 as the M ≥ 7-analog band.

## Reproducing the plots

```bash
python3 -m venv .venv
.venv/bin/pip install pandas numpy matplotlib
.venv/bin/python make_plots.py
```

## Source

Primary: Smithsonian Institution Global Volcanism Program — https://volcano.si.edu/

Death-toll estimates from:
- Tanguy, J.-C. et al. (1998). *Victims from volcanic eruptions: a revised database.* Bull Volcanol.
- Witham, C. S. (2005). *Volcanic disasters and incidents.* J Volc Geo Res.

## Intended use

Data source for the volcano correlation tests in [`Biblejustin/correlations`](https://github.com/Biblejustin/correlations). Expected non-null result: volcanic eruptions × earthquakes (subduction-zone coupling is real physics, though at much shorter timescales than yearly counts).
