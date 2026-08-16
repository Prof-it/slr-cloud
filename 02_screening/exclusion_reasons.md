# Exclusion Reason Codes

> **TEMPLATE — adapt codes to the review's actual protocol.** These codes are
> referenced by the `exclusion_reason_code` column in
> [screening.xlsx](screening.xlsx).

| Code | Reason | Screening Stage |
|---|---|---|
| E1 | Not related to cloud computing | Title/Abstract |
| E2 | Not related to governance (e.g., pure performance/cost optimization) | Title/Abstract |
| E3 | Single-cloud only (no multi-cloud/hybrid-cloud aspect) | Title/Abstract |
| E4 | Not peer-reviewed (blog post, whitepaper, non-archival) | Title/Abstract |
| E5 | Duplicate record | Title/Abstract |
| E6 | Wrong document type (e.g., editorial, poster, tutorial) | Title/Abstract |
| E7 | Full text not accessible | Full-text |
| E8 | No empirical or conceptual governance contribution on closer reading | Full-text |
| E9 | Secondary study (survey/SLR) without new primary contribution | Full-text |
| E10 | Language other than [TEMPLATE — e.g., English] | Title/Abstract |

Add or remove codes as needed, but keep codes stable once screening has
started so that `screening.xlsx` and `07_prisma/prisma_counts.xlsx` remain
consistent.
