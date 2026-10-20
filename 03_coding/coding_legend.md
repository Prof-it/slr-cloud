# Coding Legend (v1, ETECOM 2026)

## Approach

Abductive qualitative content analysis (Mayring, 2014). Six dimensions
(D1-D6) were fixed deductively a priori; within each dimension an initial set
of mutually exclusive codes was derived from named field taxonomies (NIST SP
800-145, NIST CSF 2.0 GOVERN, ISO/IEC 27001:2022 Annex A control types, CSA v5
SSRM, NIST CSF 2.0 functions, Cuzzocrea & Belmerabet's IAM taxonomy), and
extension codes were added where segments were not covered (origin
`Abductive` in `codebook.xlsx`).

Each source x dimension cell carries two separate attributes:

- **code** (`code_id`) - what the cited segment asserts (`NA` = dimension not
  substantively addressed);
- **coverage** (Yes / Partial / No) - how completely the source treats the
  dimension at organisational level (see sheet `Coverage_scale_v1`). Coverage
  does not imply explicit cross-provider coordination.

## Files

| File | Content |
|---|---|
| `codebook.xlsx` | Codes, dimensions with grounding and assignment rules, coverage scale |
| `coding_evidence.xlsx` | 84 cells (14 sources x 6 dimensions) with segment, page, decision, v1 coverage and the coverage/evidence published in ETECOM 2026 Tables III/IV |
| `audit_v1_flags.csv` | Known inconsistencies in v1 coding, input for v2 |
| `source/Coding_Evidence_Workbook_MASTER_V4.xlsx` | Original first-coder workbook, unmodified |

## `coding_evidence.xlsx` columns

| Column | Meaning |
|---|---|
| `evidence_id` | `EV-nnn`, equal to the segment number in the original workbook |
| `study_id` | Key into `06_included_studies/included_studies.csv` |
| `dimension`, `code_id` | Dimension and code (key into `codebook.xlsx`) |
| `page_as_recorded` | Page as recorded by the coder (mixes journal and PDF pages; see audit flag A15) |
| `segment_verbatim` | Quoted or paraphrased evidence |
| `coding_decision` | Coder's rationale |
| `coverage_v1_workbook` | Coverage as originally coded (`*` = see CSA footnote in the paper) |
| `coverage_published_etecom2026` | Coverage as published in ETECOM 2026 Table III (normative sources only) |
| `published_evidence_etecom2026` | Clause/section evidence as published in Table IV |
| `revision_note` | Present where published coverage differs from v1 |
| `coder`, `second_coder`, `second_coder_agreement` | SS; no second coder in v1 |

## Reliability

Single coder (SS). No inter-rater reliability was computed for v1. The
journal extension (v2) will use a revised codebook and independent duplicate
coding.
