# 02_screening — Screening Decisions

**Status: derived from `01_search/` (first derived layer).**

## Contents

- `screening.xlsx` — One row per record retrieved from the search, tracking
  title/abstract screening and full-text screening decisions, reviewer(s),
  and the reason for exclusion (coded per `exclusion_reasons.md`).
- `exclusion_reasons.md` — The controlled vocabulary of exclusion reason
  codes used in `screening.xlsx`.

## Rules

- Every record in `01_search/ebsco_export.bib` (and any other raw export)
  must have a corresponding row in `screening.xlsx` — this preserves
  full traceability for the PRISMA flow diagram (`07_prisma/`).
- Use the `record_id` column to link back to the BibTeX `cite_key` in the raw
  export.
- Studies marked `Include` at the full-text stage feed into
  `06_included_studies/`.
