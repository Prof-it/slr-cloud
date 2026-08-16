# 07_prisma — PRISMA Flow Counts

**Status: derived (aggregated) from `01_search/`, `02_screening/`, and
`06_included_studies/`.**

## Contents

- `prisma_counts.xlsx` — Record counts at each PRISMA stage (identification,
  deduplication, screening, eligibility, inclusion), broken down by database
  and by exclusion reason. Used to generate the PRISMA flow diagram for the
  manuscript (output stored under `09_tables_figures/generated/`).

## Rules

- Counts must reconcile exactly with the row counts in
  `01_search/ebsco_export.bib`, `02_screening/screening.xlsx`, and
  `06_included_studies/included_studies.csv`. Recompute after any change to
  screening decisions.
