# 09_tables_figures — Manuscript Tables and Figures

**Status: derived outputs.**

## Contents

- `source_data/` — Intermediate data extracts used to build a specific
  table/figure (e.g., a pivoted CSV feeding a plotting script).
- `generated/` — Final rendered tables/figures (e.g., `.png`, `.pdf`, `.csv`)
  ready for inclusion in the manuscript.

## Rules

- Everything in this directory should be regeneratable by re-running the
  scripts/notebooks in `08_analysis/` against the data in `03_coding/`,
  `04_quality_assessment/`, and `05_synthesis/`. Do not hand-edit generated
  files.
