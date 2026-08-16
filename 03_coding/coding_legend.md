# Coding Legend

> **TEMPLATE — adapt to the review's actual coding protocol.**

## How to Read `coding_evidence.xlsx`

Each row represents one **coding decision**: a single instance where a coder
applied a code from `codebook.xlsx` to a specific piece of evidence in an
included study.

| Column | Meaning |
|---|---|
| `evidence_id` | Unique ID for this coding decision (e.g., `EV-0001`). |
| `study_id` | Foreign key to `06_included_studies/included_studies.csv`. |
| `code_id` | Foreign key to `03_coding/codebook.xlsx`. |
| `page` | Page number in the source PDF where the evidence appears. |
| `section` | Section/subsection heading (e.g., "4.2 Access Control"). |
| `quote_or_paraphrase` | Verbatim quote (preferred) or close paraphrase of the evidence. |
| `evidence_type` | `quote`, `paraphrase`, `table`, `figure`, or `derived`. |
| `coder` | Initials/ID of the coder who made the decision. |
| `confidence` | `High` / `Medium` / `Low` — coder's confidence in the code's applicability. |
| `second_coder_agreement` | `Agree` / `Disagree` / `Not double-coded` — used for inter-rater reliability. |
| `notes` | Free-text notes, disagreement resolution, etc. |

## Coding Process (TEMPLATE)

1. [TEMPLATE — e.g., Each included study is read in full by a primary coder.]
2. [TEMPLATE — e.g., A random 20% subsample is double-coded by a second coder
   for inter-rater reliability (Cohen's kappa reported in
   `05_synthesis/synthesis_notes.md`).]
3. [TEMPLATE — e.g., Disagreements are resolved via discussion and logged in
   the `notes` column.]

## Confidence Levels

- **High** — Evidence directly and unambiguously supports the code.
- **Medium** — Evidence supports the code but requires some interpretation.
- **Low** — Evidence is suggestive; flagged for review/discussion.
