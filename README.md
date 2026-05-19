# volcanic-eruptions

Hand-curated catalog of VEI ≥ 5 volcanic eruptions since 1500 CE, plus a handful of notable VEI 4 events with major societal impact (Pelée, Eyjafjallajökull).

Parallel in spirit to `earthquakes`, `spaceweather`, `famines-tracking`, `flood-data`.

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

## Detection-bias notes

| Band | Coverage |
|---|---|
| VEI ≥ 7 | Detection-clean for several millennia (each event leaves a global tephra layer) |
| VEI ≥ 6 | Detection-clean back to ~1500 globally |
| VEI ≥ 5 | Detection-clean back to ~1500 for populated regions; remote events (Aleutians, Kamchatka, Southern Andes) may be undercounted pre-1850 |
| VEI ≤ 4 | Heavy completeness gaps pre-1900; only included if high-impact |

For the correlations work, use VEI ≥ 5 as the M ≥ 7-analog band.

## Source

Primary: Smithsonian Institution Global Volcanism Program — https://volcano.si.edu/

Death-toll estimates from:
- Tanguy, J.-C. et al. (1998). *Victims from volcanic eruptions: a revised database.* Bull Volcanol.
- Witham, C. S. (2005). *Volcanic disasters and incidents.* J Volc Geo Res.

## Intended use

Data source for the volcano correlation tests in [`Biblejustin/correlations`](https://github.com/Biblejustin/correlations). Expected non-null result: volcanic eruptions × earthquakes (subduction-zone coupling is real physics).
