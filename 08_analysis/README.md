# 08_analysis — Analysis Code

**Status: code, not data.**

- `scripts/check_consistency.py` — checks referential integrity (study_id,
  code_id, cite keys), PRISMA arithmetic and the full-text/included link;
  reports archived EBSCO records outside the date filter and cells where
  published Table III differs from v1 coding; writes
  `09_tables_figures/generated/coverage_frequency_v1.csv` and
  `tableIII_published_etecom2026.csv`.
- `requirements.txt` — dependencies.

Scripts read `01_search` .. `07_prisma` and write only to
`09_tables_figures/generated/`.
