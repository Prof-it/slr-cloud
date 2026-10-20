# Known Issues and Gaps in the v1 Evidence Record

This file documents, without retroactive repair, where the archived v1 evidence
(ETECOM 2026 paper) is incomplete or inconsistent. Items marked **[v2]** are to
be resolved in the journal extension, not by editing v1 records.

## Search (01_search)

1. **Raw EBSCO export not archived.** The search log reports 996 EBSCO hits;
   the archived export (`exports/search_results_by_database_2026-04.xlsx`,
   sheet `EBSCO`) holds 777 records, i.e. the state after EBSCO-internal
   deduplication. `exports/ebsco_export_partial_18records.bib` is a partial
   BibTeX export only.
2. **Date filter.** 73 of the 777 archived EBSCO records carry 2026 publication
   dates, although the search was restricted to 2020-2025. None of the 16
   full-text candidates is affected (all 2020-2025).
3. **Duplicate attribution not reproducible.** 219 duplicates were removed
   (1,818 -> 1,599). EBSCO indexes IEEE Xplore (`edseee`), Springer and other
   publisher content; an approximate normalised-title match finds overlaps of
   EBSCO with SpringerLink (~83), IEEE Xplore (~21), ScienceDirect (~6) and
   ACM DL (~5). A statement that all duplicates were EBSCO-internal (used in an
   early journal draft) is therefore not supported. **[v2]** Deduplicate
   across all exports by DOI/title with a logged script.
4. **Reported vs. executed query.** ETECOM Sec. III-A reports a simplified
   conceptual Boolean structure; the executed strings (search_history.xlsx)
   additionally contain "multi cloud", "security framework", "risk posture"
   and "information security".

## Screening (02_screening)

5. **No record-level title/abstract log.** Only aggregate counts exist for the
   1,583 title/abstract exclusions. Full-text decisions (16 records) are
   archived. Single reviewer (SS) throughout.
6. **Eligibility criterion vs. databases.** The indexing criterion names four
   databases (IEEE Xplore, ACM DL, SpringerLink, ScienceDirect) while EBSCO
   HOST was searched as a fifth.

## Quality assessment (04_quality_assessment)

7. **Item scores not archived.** The rubric is documented; per-study scores
   are not. **[v2]** Re-score independently.

## Coding (03_coding)

8. **Single coder, no inter-rater reliability.** As stated in the ETECOM
   paper (Sec. VI). Test-retest re-coding of three papers was reported but its
   record is not archived.
9. **Cell-level rating.** 84 rows = 14 sources x 6 dimensions, one exemplar
   segment per cell.
10. **Revisions at publication.** NIST SP 800-210 D1, D4, D5 were re-rated
    during ETECOM author review (`coverage_published_etecom2026`,
    `revision_note`); supporting segments for the revised ratings were not
    recorded.
11. **Code/coverage inconsistencies** are itemised in
    `03_coding/audit_v1_flags.csv` (A01-A17). **[v2]** Replace Yes/Partial/No
    with separate generic-coverage (G1-G3) and multi-cloud operationalisation
    (M1-M3) ratings with deterministic decision rules, and code independently
    with at least two coders.

## Synthesis (05_synthesis)

12. **Gap-to-evidence links are source-level.** Published Table V cites
    sources per gap instance; `candidate_evidence_cells` derives the linked
    cells, but no segment-level justification per gap instance exists.
13. **CPCG-2 evidence conflict** between the v1 workbook and published Table V
    (see `governance_gap_taxonomy.xlsx`).

## Included studies (06_included_studies)

14. **Full-text PDFs.** Only the two IEEE Access papers (CC BY 4.0) may be
    redistributed. The other eight publisher PDFs are excluded via
    `.gitignore`, but they are still tracked in the current index and present
    in git history and must be removed from both before the repository is
    made public.
