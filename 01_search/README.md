# 01_search — Search Data

**Status: raw / source data (v1, search run April 2026).**

## Contents

- `search_strategy.md` — research question, databases, executed query strings,
  criteria, citation tracking.
- `search_history.xlsx` — one row per database run (hits, after deduplication,
  notes).
- `exports/search_results_by_database_2026-04.xlsx` — archived result lists per
  database (IEEE Xplore, ACM DL, SpringerLink, ScienceDirect, EBSCO). The EBSCO
  sheet holds 777 records after EBSCO-internal deduplication; the raw 996-record
  export was not archived.
- `exports/ebsco_export_partial_18records.bib` — partial EBSCO BibTeX export
  (18 records), not the full result set.

See `../docs/known_issues.md` (items 1-4) for date-filter and deduplication
issues.

## Rules

- Never hand-edit archived exports.
- New search runs (journal extension) go into new, dated files and new rows in
  `search_history.xlsx`.
