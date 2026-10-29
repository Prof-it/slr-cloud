# Search Protocol v2 — Precision-Oriented Single-Database Search with Validated Recall

**Status: DRAFT. Register the frozen version (e.g. on OSF) before running the
final search.**

## 1. Design rationale

v1 retrieved 1,818 records and included 10, a precision of 0.6%. v2 does not
add databases. It improves precision through a facet structure derived from
codebook v2, and it demonstrates that recall is retained against an
independently built gold set. Coverage gaps of a single database are
mitigated by citation snowballing (Wohlin, 2014) and an OpenAlex cross-check;
neither adds a second full screening pile.

| Element | Choice |
|---|---|
| Primary source | EBSCO (EBSCO Research interface, IU licence). Record which collections are active on the search date. |
| Complementary | One round of backward and forward snowballing from the included set (OpenAlex API); OpenAlex search as a recall cross-check only |
| Fields | Title, abstract, author keywords, subject terms |
| Date window | 2020-01-01 to the search date (decision: TL). Enforced by the pipeline (rule `F-YEAR`), not by the database filter alone (v1 export contained 73 records outside the window). |
| Types | Peer-reviewed journal articles and conference papers (`F-TYPE`), English (`F-LANG`) |
| Normative documents | Selected by rule, outside PRISMA (§6) |

## 2. Facets (derived from codebook v2)

**Facet A — multi-cloud context**
```
multi-cloud OR multicloud OR "multi cloud" OR cross-cloud OR "cross cloud"
OR inter-cloud OR intercloud OR "cloud federation" OR "federated cloud*"
OR "multiple cloud provider*" OR "multiple cloud service provider*"
OR "heterogeneous cloud*" OR "hybrid multi-cloud"
```

**Facet B — governance object (D2–D6)**
```
governance OR compliance OR accountab* OR oversight                          (D2)
OR "policy enforcement" OR "policy as code" OR "policy-as-code"
OR "policy management" OR guardrail* OR "configuration drift"                  (D3)
OR "shared responsibilit*" OR "responsibility model" OR "key management"       (D4)
OR "security posture" OR CSPM OR "posture management" OR "security monitoring" (D5)
OR "identity federation" OR "federated identit*" OR "identity management"
OR "identity and access management" OR "single sign-on"                        (D6)
```
Deliberately excluded from B: bare `IAM`, `access control`, `security`,
`encryption`, `authentication`. Each pulls in large cryptography and
performance literatures. Whether this costs recall is tested in §4 (iteration
log variant V1b).

**Facet C — framework anchor (precision booster, variant V3 only)**
```
"ISO 27001" OR "ISO/IEC 27001" OR "NIST CSF" OR "Cybersecurity Framework"
OR "Cloud Controls Matrix" OR "CSA" OR framework* OR standard*
```

### 2a. Scope decision: second literature stream (decide before the pilot)

Several v1 includes are **not** multi-cloud studies; they are cloud security
**framework comparisons**: Hegde et al. 2023, Aljarrah et al. 2024, and
possibly Alouffi et al. 2021. AlGhamdi et al. 2020 and Pöhn & Hillmann 2021
came from citation tracking and contain no multi-cloud terms. Facet A cannot
retrieve them. Choose one of:

- **Option 1 — single stream:** eligibility requires a multi-cloud or
  cross-provider focus (S ≥ S2). Framework-comparison papers are then cited
  as related work, not included. Gold-set entries GS-02/04/09/10 (and
  possibly GS-07) leave the recall denominator.
- **Option 2 — two streams:** Stream 1 = A AND B. Stream 2 = framework
  comparisons in a cloud context:
  ```
  cloud AND ("ISO 27001" OR "ISO/IEC 27001" OR "NIST CSF" OR "Cybersecurity Framework"
  OR "Cloud Controls Matrix" OR "security framework*" OR "governance framework*")
  AND (compar* OR mapping OR benchmark* OR "gap analysis" OR coverage)
  ```
  Both streams are screened together after deduplication; report recall per stream.

Option 2 matches the paper's cross-framework claim. Option 1 gives the
smaller screening set. Either is defensible if stated a priori.
-> We agree on option 2. 

## 3. Search-string variants for the pilot

The syntax shown is EBSCOhost classic (`TI`/`AB`/`SU`, proximity `Nn`).
**Verify each in the EBSCO Research interface before use** and record the
exact string as executed in the iteration log.

| Variant | Structure | Expected effect |
|---|---|---|
| V1 | (TI A OR AB A OR SU A) AND (TI B OR AB B OR SU B) | Baseline: plain conjunction |
| V1b | V1 with `"access control" OR IAM OR authentication` added to B | Recall check for the excluded terms |
| V2 | TI A AND (TI B OR AB B), plus AB (A N10 B) | Higher precision: proximity in abstract, or multi-cloud in title |
| V3 | V1 AND (TI C OR AB C) | Highest precision; risk to recall for papers that do not name frameworks |

## 4. Recall validation (quasi-gold standard)

1. **Build the gold set before running any variant** (`gold_set.csv`), independently of the search strings:
   - the 10 v1 includes;
   - relevant primary studies cited by the v1 SLRs (Diningrat et al. 2025; Alouffi et al. 2021; Ali et al. 2025), screened against the v2 eligibility criteria;
   - a manual check of 2–3 core venues (e.g. Journal of Cloud Computing, IEEE CLOUD, Computers & Security) for the date window.

   Target: 15–25 papers. Record the source of each entry.
2. Run each variant and export the results. Then run `slr_pipeline.py recall` to obtain the gold-set recall.
3. **Acceptance:** recall ≥ 0.90. Among accepted variants, choose the one with the fewest records after deduplication and rule filtering. Report every variant's hits, recall and estimated precision in the iteration log.
4. **Precision estimate:** screen a random sample of 100 records of the chosen variant (or all, if fewer). Report the proportion included.
5. **Missed gold papers:** inspect each one and document why it was missed. If a missed paper reveals a missing synonym, add the synonym to the facets and re-run, logging the new iteration.

## 5. Pipeline (scripted, logged)

```
ingest    → normalise EBSCO/OpenAlex exports (CSV, RIS, BibTeX) to one schema
dedup     → DOI match, then normalised-title + year (±1) match; every pair logged
filter    → rule-based exclusions F-YEAR, F-TYPE, F-LANG, F-RETRACT; every exclusion logged
recall    → gold-set recall report
snowball  → OpenAlex backward/forward citations of the included set; dedup against screened set
export    → screening CSV (ASReview/Rayyan) + RIS
```

In PRISMA 2020, records removed by `filter` are reported as *"marked as
ineligible by automation tools"*, with counts per rule. Duplicate pairs are
archived so that the duplicate count can be reproduced.

## 6. Normative documents (Phase 2)

Selection rule: documents that (i) are named as a comparator, benchmark, or
coding basis in ≥2 included studies, or (ii) are cloud-specific security
governance guidance from a standards body or a recognised industry consortium.
Apply the rule after study inclusion and report the resulting list,
including documents considered and rejected (e.g. ISO/IEC 27017, CSA CCM,
NIST SP 800-53).

## 7. Screening

- **Title/abstract:** one screener on all records (ASReview prioritisation allowed; stopping rule: stop once ≥50% of records are screened **and** the last 100 consecutive decisions were exclusions). A second screener independently screens, blind to screener 1, all records the first included plus a random 10% of the excluded and of the unscreened records (`slr_pipeline.py sample`, fixed seed). Report agreement and the estimated number of missed includes.
- **Full text:** two reviewers independently; disagreements are adjudicated and logged.
- **Eligibility criteria:** as v1 (`01_search/search_strategy.md`), with the date window updated and the indexing criterion replaced by "retrieved by the registered search or snowballing".

## 8. Iteration log

Record every executed string in `search_iterations.csv`, one row per run:
`run_id, date, interface, variant, exact_string, filters, hits, after_dedup,
after_rules, gold_found, gold_total, recall, notes`.
