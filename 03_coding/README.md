# 03_coding — Codebook and Coding Evidence

**Status: derived from `06_included_studies/` (primary research artifact).**

## Contents

- `codebook.xlsx` — codes per dimension (definition, grounding, origin),
  dimension assignment rules, coverage scale.
- `coding_evidence.xlsx` — one row per source x dimension cell (84), with
  segment, page, coding decision, v1 coverage and the coverage/evidence
  published in ETECOM 2026.
- `audit_v1_flags.csv` — known inconsistencies in v1 coding (input for v2).
- `coding_legend.md` — how to read the files.
- `source/Coding_Evidence_Workbook_MASTER_V4.xlsx` — original first-coder
  workbook (unmodified).

## Traceability

`06_included_studies/included_studies.csv (study_id)` -> `coding_evidence.xlsx
(study_id, code_id, evidence_id)` -> `codebook.xlsx (code_id)` ->
`05_synthesis/*` (evidence_id, study_id).

## Rules

- Every `code_id` exists in `codebook.xlsx`; every `study_id` in
  `included_studies.csv` (checked by `08_analysis/scripts/check_consistency.py`).
- v2 coding (G1-G3 / M1-M3, independent coders) goes into new files; v1 stays
  unchanged.
