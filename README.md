# SLR Cloud — Multi-Cloud Governance Evidence Repository

Evidence package for the systematic literature review and cross-framework gap
analysis reported in:

**Sabazadeh, S. and Lu, T. (2026).** *Cybersecurity Governance in Multi-Cloud
Environments: A Systematic Review and Cross-Framework Gap Analysis.* IEEE 2026
International Conference on Emerging Trends in Engineering and Computing
(ETECOM), Paris, France, 26–27 October 2026. **Accepted.**

```bibtex
@inproceedings{sabazadeh_lu_2026_multicloud,
  author    = {Sabazadeh, Sahel and Lu, Tianxiang},
  title     = {Cybersecurity Governance in Multi-Cloud Environments: A Systematic Review and Cross-Framework Gap Analysis},
  booktitle = {IEEE 2026 International Conference on Emerging Trends in Engineering and Computing (ETECOM)},
  year      = {2026},
  address   = {Paris, France},
  month     = oct,
  note      = {Accepted, 26--27 October 2026}
}
```

The state of the evidence underlying that paper is released as
**`v1.0-etecom2026`**. The journal extension (extended search, revised coding
scheme with independent duplicate coding) will be added as new, separately
versioned material; v1 records are not overwritten.

## Status of the v1 record

- Complete: search strings and log, archived database exports, full-text
  screening decisions, codebook, cell-level coding evidence (84 cells), coverage
  matrices, gap taxonomy, PRISMA counts, included-study bibliography.
- Not archived: raw 996-record EBSCO export, record-level title/abstract
  decisions, per-study quality scores.
- Single reviewer/coder; no inter-rater reliability.

All gaps and inconsistencies are listed in
[docs/known_issues.md](docs/known_issues.md); coding-level issues in
[03_coding/audit_v1_flags.csv](03_coding/audit_v1_flags.csv).

## Directory Structure

| Directory | Contents | Raw / Derived |
|---|---|---|
| [01_search/](01_search/README.md) | Search strategy, search log, archived exports | Raw |
| [02_screening/](02_screening/README.md) | Full-text screening decisions, exclusion reasons | Derived |
| [03_coding/](03_coding/README.md) | Codebook, coding evidence, original coding workbook, audit flags | Derived (primary artifact) |
| [04_quality_assessment/](04_quality_assessment/README.md) | Quality rubric (scores not archived) | Derived |
| [05_synthesis/](05_synthesis/README.md) | Coverage matrices, gap taxonomy, synthesis notes | Derived |
| [06_included_studies/](06_included_studies/README.md) | Included studies (CSV + BibTeX), open-licence PDFs | Derived |
| [07_prisma/](07_prisma/README.md) | PRISMA flow counts | Derived |
| [08_analysis/](08_analysis/README.md) | Consistency-check script | Code |
| [09_tables_figures/](09_tables_figures/README.md) | Generated tables | Derived outputs |
| [docs/](docs/) | Reproducibility, data availability, known issues | Documentation |

## Identifiers

`study_id` (`STU-01`..`STU-10` academic studies, `NRM-01`..`NRM-04`
normative sources) joins all artifacts; `evidence_id` (`EV-001`..`EV-084`)
identifies a coded source x dimension cell.

## Quick check

```bash
pip install -r 08_analysis/requirements.txt
python 08_analysis/scripts/check_consistency.py
```

## Evidence integrity

1. Do not edit v1 records in place; corrections are documented in
   `docs/known_issues.md` or `audit_v1_flags.csv`.
2. Keep raw search evidence, screening records, coding evidence and derived
   synthesis separate.
3. Add journal-extension material (new search runs, v2 codebook, independent
   coding) as new files or folders and document them in the folder READMEs.

## License

See [LICENSE](LICENSE). Third-party publications in `06_included_studies/`
remain under their publishers' licences.
