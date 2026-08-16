# 01_search — Raw Search Data

**Status: raw / source data.** Files here must reflect exactly what was
retrieved from the literature databases, without any manual filtering.

## Contents

- `search_strategy.md` — Research questions, databases searched, full boolean
  query strings, date ranges, and inclusion/exclusion criteria used to build
  the queries.
- `search_history.xlsx` — Log of every query execution (database, query
  string, date run, number of hits, notes).
- `ebsco_export.bib` — Raw, unmodified BibTeX export from the EBSCO database
  search. This is the primary raw search artifact for EBSCO; if additional
  databases were searched, add one export file per database (e.g.
  `scopus_export.bib`, `ieee_export.csv`) and document them in
  `search_history.xlsx`.

## Rules

- Never hand-edit `ebsco_export.bib` (or any other raw export) to add/remove
  records — filtering happens in `02_screening/`, not here.
- If a database export is re-run (e.g., updated search), keep the previous
  export (e.g., `ebsco_export_2026-01-15.bib`) and log the re-run in
  `search_history.xlsx` rather than overwriting silently.
