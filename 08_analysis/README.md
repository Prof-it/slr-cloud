# 08_analysis — Analysis Code

**Status: code, not data.** Scripts and notebooks that consume the data
artifacts (mainly `03_coding/`, `04_quality_assessment/`, `05_synthesis/`) and
produce the outputs saved under `09_tables_figures/`.

## Contents

- `scripts/` — Standalone scripts (e.g., Python) for data cleaning,
  inter-rater reliability computation, and figure/table generation.
- `notebooks/` — Exploratory/analysis notebooks.

## Rules

- Scripts/notebooks should read from the `.xlsx`/`.csv`/`.bib` files in this
  repository and write outputs only into
  `09_tables_figures/source_data/` or `09_tables_figures/generated/` —
  never modify files in `01_search/` through `07_prisma/` in place.
- Pin dependencies (e.g., `requirements.txt` or notebook cell listing
  package versions) once real analysis code is added.
