# Reproducibility Workflow

This document describes, step by step, how to reproduce the review's
findings from the raw search export to the final manuscript tables/figures.

## Prerequisites

- Python 3.9+ and `pip install -r 08_analysis/requirements.txt`
- A spreadsheet application capable of opening `.xlsx` (Excel, LibreOffice
  Calc, Google Sheets) for manual inspection of coding/screening data.
- A BibTeX-capable reference manager (Zotero, JabRef, or `bibtexparser` in
  Python) to inspect/validate `.bib` files.

## Steps

1. **Inspect the raw search data**
   - Open [`../01_search/search_history.xlsx`](../01_search/search_history.xlsx)
     and the archived exports in `../01_search/exports/`. Note that the EBSCO
     export is post-internal-deduplication (777 of 996 records; see
     [`known_issues.md`](known_issues.md)).
2. **Review screening decisions**
   - Open [`../02_screening/screening.xlsx`](../02_screening/screening.xlsx).
   - Cross-check exclusion codes against
     [`../02_screening/exclusion_reasons.md`](../02_screening/exclusion_reasons.md).
3. **Confirm the included study set**
   - Compare [`../06_included_studies/included_studies.csv`](../06_included_studies/included_studies.csv)
     against studies marked `Include` in `screening.xlsx`.
4. **Validate coding traceability**
   - For a sample of rows in
     [`../03_coding/coding_evidence.xlsx`](../03_coding/coding_evidence.xlsx),
     open the referenced source PDF at the given page/section and confirm the
     quote/paraphrase is accurate.
   - Cross-check every `code_id` against
     [`../03_coding/codebook.xlsx`](../03_coding/codebook.xlsx).
5. **Check quality assessment**
   - The rubric is in
     [`../04_quality_assessment/quality_assessment.xlsx`](../04_quality_assessment/quality_assessment.xlsx);
     v1 item scores were not archived.
6. **Re-derive synthesis artifacts**
   - Confirm [`../05_synthesis/comparative_coverage_matrix.xlsx`](../05_synthesis/comparative_coverage_matrix.xlsx)
     is consistent with `coding_evidence.xlsx` (each cell should be traceable
     to specific `evidence_id`s).
7. **Recompute PRISMA counts**
   - Recompute [`../07_prisma/prisma_counts.xlsx`](../07_prisma/prisma_counts.xlsx)
     from the row counts in steps 1–3.
8. **Run the consistency check and regenerate tables**
   - `python 08_analysis/scripts/check_consistency.py`, i.e. the scripts in
     [`../08_analysis/`](../08_analysis/README.md) to regenerate the contents
     of [`../09_tables_figures/generated/`](../09_tables_figures/generated/.gitkeep).

## Verifying Consistency

A reproducing researcher should confirm:

- PRISMA arithmetic in `07_prisma/prisma_counts.xlsx` is consistent (record-level
  title/abstract screening is not archived, so this cannot be checked per record).
- `02_screening` `Include` rows = `06_included_studies` row count.
- Every `study_id` in `06_included_studies` appears in `03_coding`,
  `04_quality_assessment`.
- Every `code_id` used in `03_coding/coding_evidence.xlsx` exists in
  `03_coding/codebook.xlsx`.
- `07_prisma/prisma_counts.xlsx` totals reconcile with the above.
