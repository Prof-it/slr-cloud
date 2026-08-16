# 03_coding — Codebook and Coding Evidence

**Status: derived from `06_included_studies/` (primary research artifact of
this review).**

## Contents

- `codebook.xlsx` — Defines the coding scheme: every code, its definition,
  category/theme grouping, and an example application. This is the
  authoritative reference for what each code means.
- `coding_evidence.xlsx` — **The most important artifact in this repository.**
  Records every individual coding decision applied to an included study,
  linked to the exact page/section/quote in the source document that
  justifies the code. This enables full traceability from a synthesis claim
  back to the original evidence.
- `coding_legend.md` — Human-readable explanation of the coding process,
  confidence levels, and how to read `coding_evidence.xlsx`.

## Traceability Chain

```
06_included_studies (study_id)
        │
        ▼
03_coding/coding_evidence.xlsx (study_id, code_id, page/section, quote)
        │
        ▼
03_coding/codebook.xlsx (code_id → definition/category)
        │
        ▼
05_synthesis/* (aggregated by code/category)
```

## Rules

- Every row in `coding_evidence.xlsx` MUST reference a `code_id` that exists
  in `codebook.xlsx`, and a `study_id` that exists in
  `06_included_studies/included_studies.csv`.
- Page/section references are mandatory — a coding decision without a
  traceable location is not acceptable for this review's evidentiary
  standard.
- If the codebook changes (codes added/renamed/merged), re-run coding
  consistency checks and note the change in `coding_legend.md`.
