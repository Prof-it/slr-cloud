# Reproducibility Workflow

This document describes, step by step, how to reproduce the review's
findings from the raw search export to the final manuscript tables/figures.

## Prerequisites

- [TEMPLATE — e.g., Python 3.11+, `pip install -r 08_analysis/requirements.txt`]
- A spreadsheet application capable of opening `.xlsx` (Excel, LibreOffice
  Calc, Google Sheets) for manual inspection of coding/screening data.
- A BibTeX-capable reference manager (Zotero, JabRef, or `bibtexparser` in
  Python) to inspect/validate `.bib` files.

## Steps

1. **Inspect the raw search data**
   - Open [`../01_search/ebsco_export.bib`](../01_search/ebsco_export.bib) and
     confirm the record count matches `search_history.xlsx`.
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
5. **Check quality assessment scoring**
   - Recompute scores in
     [`../04_quality_assessment/quality_assessment.xlsx`](../04_quality_assessment/quality_assessment.xlsx)
     against the rubric documented in that workbook.
6. **Re-derive synthesis artifacts**
   - Confirm [`../05_synthesis/comparative_coverage_matrix.xlsx`](../05_synthesis/comparative_coverage_matrix.xlsx)
     is consistent with `coding_evidence.xlsx` (each cell should be traceable
     to specific `evidence_id`s).
7. **Recompute PRISMA counts**
   - Recompute [`../07_prisma/prisma_counts.xlsx`](../07_prisma/prisma_counts.xlsx)
     from the row counts in steps 1–3.
8. **Regenerate tables/figures**
   - Run the scripts/notebooks in
     [`../08_analysis/`](../08_analysis/README.md) to regenerate the contents
     of [`../09_tables_figures/generated/`](../09_tables_figures/generated/.gitkeep).

## Verifying Consistency

A reproducing researcher should confirm:

- `01_search` record count = `02_screening` row count.
- `02_screening` `Include` rows = `06_included_studies` row count.
- Every `study_id` in `06_included_studies` appears in `03_coding`,
  `04_quality_assessment`.
- Every `code_id` used in `03_coding/coding_evidence.xlsx` exists in
  `03_coding/codebook.xlsx`.
- `07_prisma/prisma_counts.xlsx` totals reconcile with the above.
