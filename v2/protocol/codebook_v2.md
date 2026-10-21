# Codebook v2 — Generic Coverage (G) vs. Multi-Cloud Operationalisation (M)

**Status: DRAFT for author review (TL, SS). Freeze before calibration; any later
change is versioned (v2.1, ...) and logged in the change log below.**

## 1. Purpose and what changes from v1

v1 rated each source × dimension cell on one Yes/Partial/No scale. That scale
mixed two questions: whether a governance capability is covered at all, and
whether it is operationalised across heterogeneous providers. It also
mixed two kinds of source: a framework *provides* a provision, whereas a paper
*reports on* a problem or mechanism (`03_coding/audit_v1_flags.csv`, A01–A17).

v2 separates these concerns:

| v1 | v2 |
|---|---|
| D1 "multi-cloud environment focus" as a dimension | Source-level attribute **S** (scope). D1 is no longer a coded dimension, because multi-cloud operationalisation is now measured *within* every dimension by M. |
| Yes / Partial / No per cell | Two independent ordinal ratings per cell: **G1–G3** and **M1–M3** |
| One scale for frameworks and papers | Same G/M levels, **source-type-specific anchors** (§4); papers additionally carry **E** (evidence basis) |
| Absence (No / n/a) supported by a scope sentence | Absence supported by a **logged term search** in the full text (§6) |
| Gap categories read off dimension codes | Gaps derived by an explicit **gap rule** over G/M ratings (§8) |

## 2. Unit of analysis

One **cell** = one source × one dimension (D2–D6). Each cell receives:
`G`, `M`, `aspects` (multi-select, §5), `evidence` (≥1 quote with PDF page
and section, or a term-search record for G1/M1), and `rationale` (one or two
sentences referencing the decision rule applied, e.g. "M2 per R-M2a").

Source-level attributes (once per source): `S` scope, `T` source type,
`N` normativity, and for academic studies `E` evidence basis.

## 3. Dimensions

| ID | Dimension | Includes | Excludes (code elsewhere) |
|---|---|---|---|
| D2 | Governance structure | Decision rights, governance roles and oversight, risk-management strategy, governance of provider relationships (cf. NIST CSF GV.OC/RM/RR/OV/SC; ISO/IEC 27001 Cl. 4–6, 9) | Allocation of security *duties* between provider and customer → D4 |
| D3 | Policy definition and enforcement | Security policies and their technical or organisational enforcement: configuration baselines, policy-as-code, preventive guardrails, authorisation policy rules | Identity establishment, trust and lifecycle → D6; detective monitoring → D5 |
| D4 | Shared responsibility and accountability | Allocation of security obligations between provider(s) and customer, responsibility matrices (SSRM), accountability for keys and encryption, contractual or SLA allocation | Internal role assignment within the customer organisation → D2 |
| D5 | Risk posture and security monitoring | Risk identification and assessment, continuous monitoring, CSPM, logging/telemetry, aggregation and normalisation of posture data, reporting obligations | Incident response procedures (record as aspect D5-other) |
| D6 | Identity and federation | IdP–RP trust, federation protocols (SAML, OIDC, OAuth), identity lifecycle (provisioning, de-provisioning), token validation, cross-provider identity mapping | Generic authorisation policy rules → D3 |

**Tie-breaker:** if a segment fits two dimensions, code it in the dimension
named by the segment's *governance object* (what is being governed). If it
fits both equally, code it in both and mark `dual=Y`. Dual-coded segments
are reported.

## 4. Rating scales

G and M are rated **independently**. Constraint check: `M3` with `G1` is
allowed but triggers adjudicator review.

### 4.1 G — generic coverage (is the capability addressed at all?)

| Level | Normative document (provides) | Academic study (contributes) |
|---|---|---|
| **G1** absent / mention | Term or topic appears at most in passing; no requirement, guidance or outcome statement | Topic mentioned in passing (e.g. in a list, introduction, future work) |
| **G2** general | A requirement, guidance or outcome is stated at objective level, without implementation specification | The capability is discussed substantively (analysed, compared, or problematised) without a specified mechanism |
| **G3** specified | Control-, subcategory- or clause-level requirement with implementation guidance or verifiable criteria | A concrete mechanism, model, or procedure for the capability is specified (architecture-agnostic or single-provider) |

### 4.2 M — multi-cloud operationalisation (is it specified across heterogeneous providers?)

| Level | Normative document | Academic study |
|---|---|---|
| **M1** none | No content on applying the capability across two or more independent providers | No cross-provider content for this dimension |
| **M2** acknowledged | Multi-cloud or cross-provider situation acknowledged, or advisory statement ("organisations should consider …"), without a mechanism | Cross-provider problem described, argued or evidenced for this dimension, without a proposed mechanism |
| **M3** mechanism | Explicit mechanism for applying, reconciling, enforcing, monitoring or auditing the capability across ≥2 independent providers (procedure, required artefact, requirement, or reference architecture) | A mechanism for cross-provider operation of the capability is proposed (record evaluation status in E) |

### 4.3 Decision rules

- **R-M3a (all three must hold):** the segment (i) explicitly refers to two or more independent providers or to "multiple CSPs/clouds"; (ii) specifies *what* is to be done or produced, not only that something is a challenge; (iii) is actionable without further design, i.e. it names a procedure, artefact, requirement or architecture.
- **R-M3b:** naming providers in an example, or listing cross-provider tools (e.g. Azure Arc, Anthos), is **not** a mechanism unless R-M3a(ii)–(iii) hold.
- **R-M2a:** a cross-provider *problem* statement for the dimension → M2, even if well evidenced empirically. Evidence strength goes into E, not M.
- **R-M2b:** advisory multi-cloud statements in normative documents ("should", "consider") without (ii)–(iii) → M2.
- **R-G3a:** for normative documents, G3 requires a numbered control, subcategory or clause *and* either implementation guidance or a verifiable criterion; a clause title alone → G2.
- **R-G2a:** for academic studies, discussion that only cites other work for the capability → G1 unless the study analyses it.
- **R-S:** S is coded from the source's stated scope (abstract, introduction, method), not from individual segments.
- **R-ABS:** G1 or M1 requires a completed term search (§6). Without it the cell is `unresolved` and cannot be finalised.
- **R-NORM:** normativity (binding / voluntary / advisory) is recorded in N and **never** changes G or M. The guidance–obligation distinction (v1 CRPNG-2) is analysed from N × M, not coded into M.

## 5. Aspects (multi-select per cell; feed gap instances)

| Dim. | Aspect codes |
|---|---|
| D2 | `D2-roles`, `D2-oversight`, `D2-risk-strategy`, `D2-provider-mgmt`, `D2-other` |
| D3 | `D3-sync` (one policy kept consistent across providers), `D3-translate` (mapping one policy to provider-native mechanisms, e.g. SCP / Azure Policy / GCP Org Policy), `D3-enforce` (enforcement or guardrail mechanism), `D3-other` |
| D4 | `D4-allocate` (allocation of duties), `D4-reconcile` (reconciling differing provider models), `D4-keys` (encryption and key-management boundaries), `D4-other` |
| D5 | `D5-assess` (risk identification/assessment), `D5-monitor` (continuous monitoring, CSPM), `D5-normalise` (aggregation and normalisation across providers), `D5-other` |
| D6 | `D6-trust` (IdP–RP trust establishment and audit), `D6-lifecycle` (provisioning, de-provisioning, synchronisation), `D6-token` (token validation, protocol interoperability), `D6-mapping` (cross-provider identity or role mapping), `D6-other` |

`*-other` requires a free-text label. Recurring `other` labels (≥2 sources)
are proposed as new aspects through the change log (abductive extension).

## 6. Evidence requirements

- **Positive ratings (G2/G3, M2/M3):** ≥1 verbatim quote of up to 50 words, with the **PDF page number** (not the journal page) and section heading.
- **Absence (G1, M1):** record the term search performed in the full text. Use the dimension term list below plus the multi-cloud terms for M: `multi-cloud, multicloud, multiple cloud, cross-cloud, inter-cloud, federat*, heterogeneous provider*, CSPs`. Record the number of hits inspected.

| Dim. | Minimum search terms |
|---|---|
| D2 | governance, oversight, role*, responsibilit*, risk strategy |
| D3 | policy, polic*, enforce*, guardrail, configuration, baseline |
| D4 | shared responsibility, SSRM, responsibility model, accountab*, key management |
| D5 | monitor*, posture, CSPM, risk assess*, logging, telemetry |
| D6 | identity, federat*, IdP, SAML, OIDC, OAuth, provisioning, token |

## 7. Source-level attributes

| Attr. | Levels |
|---|---|
| **S** scope | S0 single-cloud or architecture-agnostic · S1 hybrid (cloud + on-premises) · S2 multi-cloud conceptual or review scope · S3 multi-cloud operational (≥2 concurrent public providers implemented, benchmarked or evaluated) |
| **T** type | normative standard · normative framework · normative guidance · empirical · design/artefact · review/SLR · survey · reference model |
| **N** normativity | binding (certifiable) · voluntary framework · advisory guidance · n/a (academic) |
| **E** evidence basis (academic, for M2/M3 cells) | E1 asserted or cited · E2 literature synthesis · E3 lab/simulation evaluation · E4 field or case evaluation |

## 8. Gap rule (replaces v1 derivation)

For dimension *d* and aspect *a*, a **coverage–operationalisation gap** is
recorded if all three hold:

1. **Frameworks cover it generically:** ≥2 of the principal frameworks have G ≥ G2 on *d* **and** M ≤ M2 on *d* with aspect *a* absent from any M3 cell.
2. **The literature reports it:** ≥2 independent academic studies have M ≥ M2 on *d* with aspect *a*.
3. **Unless resolved in the literature:** no academic study has M3 with aspect *a* and E ≥ E3. If one does, the gap is recorded as "*addressed in literature, not in frameworks*".

Every gap instance lists the cell IDs satisfying (1)–(3). Instances
supported only by (1), without literature evidence, are labelled
*inference* and reported separately.

## 9. Coding procedure and reliability

1. **Calibration:** both coders and the adjudicator code 2 sources (1 framework, 1 study) jointly. These cells are excluded from agreement statistics. Rules are clarified and the codebook is frozen.
2. **Independent coding:** ≥2 coders code all remaining cells blind to each other and to v1 ratings, using the coding form (`coding_form_v2.xlsx`).
3. **Agreement:** computed per scale on cells. Report Krippendorff's α (ordinal) for G and M separately, percent agreement, and Gwet's AC1. Report κ only alongside AC1, given skewed categories. Aspects use per-code agreement (Jaccard).
4. **Threshold:** α ≥ 0.667 to proceed. Below that, revise rules once, re-code a fresh sample, and report both rounds.
5. **Adjudication:** the adjudicator (TL, non-coder) resolves disagreements; each resolution is logged with the rule applied.

## 10. Change log

| Version | Date | Change | By |
|---|---|---|---|
| v2.0-draft | 2026-10-20 | Initial draft from v1 audit (A01–A17) | Drafted for TL |
