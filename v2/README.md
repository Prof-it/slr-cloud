# v2 — Journal Extension (JCC)

Material for the journal extension of the ETECOM 2026 review. v1 records
(top-level folders, release `v1.0-etecom2026`) are not modified.

| Path | Content | Status |
|---|---|---|
| `protocol/codebook_v2.md` | G1–G3 / M1–M3 codebook: dimensions D2–D6, decision rules, aspects, evidence requirements, gap rule, reliability procedure | Draft, to be frozen before calibration |
| `protocol/search_protocol_v2.md` | Single-database (EBSCO) precision-oriented search, facets, variants, recall validation, snowballing, screening | Draft; **scope decision §2a open** |
| `protocol/gold_set.csv` | Quasi-gold standard for recall (seeded with the 10 v1 includes; extend to 15–25) | Seed |
| `protocol/search_iterations.csv` | Log of every executed search string | Empty |
| `pipeline/slr_pipeline.py` | ingest → dedup → filter → recall → snowball → export, coding-form generator | Tested on v1 exports (see below) |
| `pipeline/filter_rules.json` | Rule-based exclusions (F-YEAR, F-RETRACT, F-TYPE, F-LANG, F-NOTITLE) | Set the date window before use |
| `runs/` | One folder per pipeline run (created by the script); commit these as evidence | — |

## Quick start

```bash
P=v2/pipeline/slr_pipeline.py; RUN=v2/runs/2026-11-ebsco-V1
python $P ingest  --run $RUN --db EBSCO path/to/ebsco_export.csv
python $P dedup   --run $RUN
python $P filter  --run $RUN --config v2/pipeline/filter_rules.json
python $P recall  --run $RUN --gold v2/protocol/gold_set.csv
python $P export  --run $RUN          # 05_screening.csv / .ris for ASReview or Rayyan
python $P prisma  --run $RUN
# after inclusion decisions:
export OPENALEX_MAILTO=you@example.org
python $P snowball --run $RUN --seeds included.csv --direction both
python $P coding-form --included included.csv --coder C1 --out form_C1.xlsx
```

`ingest` reads EBSCO CSV, RIS and BibTeX (and its own schema CSV, e.g.
snowball output). Every command appends to `run_log.jsonl`; `prisma` prints
the counts for the flow diagram, including "marked ineligible by automation
tools" per rule.

## Test on the v1 exports (2026-10-20)

- **Ingest:** EBSCO (777) + SpringerLink (423).
- **Dedup:** 204 duplicates removed. Of these, 106 + 6 are EBSCO∩SpringerLink and 90 are within EBSCO. Run on EBSCO alone, the dedup finds 122 duplicates in the archived export.
- **Same title, different DOI:** 4 Springer chapter pairs share a title but have different DOIs. They are logged but not merged, by design.
- **Filter (window 2020–2025):** 68 F-YEAR, 11 F-LANG and 4 F-TYPE exclusions.
- **RIS round-trip:** re-ingesting the exported RIS and running `dedup --against` the exported screening CSV removes all 913 records as previously screened. This confirms the round trip is lossless for matching.
- **Coding form:** 14 sources × 5 dimensions = 70 cells, with dropdowns.
- **Not yet tested:** `snowball` and `openalex-search`. The OpenAlex API is not reachable from the test sandbox; run them once on your machine.
