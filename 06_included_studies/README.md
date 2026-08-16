# 06_included_studies — Final Included Study Set

**Status: derived (filtered) from `01_search/` via `02_screening/`.**

## Contents

- `included_studies.bib` — BibTeX records for every study that passed
  full-text screening (`Include` decision in `02_screening/screening.xlsx`).
- `included_studies.csv` — Flat summary table (one row per included study)
  with the `study_id` used as the join key across `03_coding/`,
  `04_quality_assessment/`, and `05_synthesis/`.

## Rules

- `study_id` values here are the canonical IDs referenced everywhere else in
  the repository — do not renumber them once coding has started.
- Every entry here must trace back to a `record_id` in
  `02_screening/screening.xlsx` with an `Include` full-text decision.
