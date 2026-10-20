# Search Strategy

## Research Question (as published, ETECOM 2026)

Which governance dimensions relevant to multi-cloud environments are covered
by established cybersecurity frameworks, to what extent are they
operationalised for cross-provider coordination, and what recurring gaps
emerge from a structured comparative analysis?

The original thesis formulation (RQ1, SRQ1-SRQ4) was condensed into this
single question for the conference paper.

## Databases Searched

| Database | Interface/Platform | Date Range Covered | Access Date |
|---|---|---|---|
| EBSCO HOST (Academic Search Complete, Business Source Complete, Computer Source) | EBSCOhost | 2020-01-01 to 2025-12-31 | 2026-04 |
| IEEE Xplore | IEEE Xplore Digital Library | 2020-01-01 to 2025-12-31 | 2026-04 |
| ACM Digital Library | ACM Digital Library | 2020-01-01 to 2025-12-31 | 2026-04 |
| SpringerLink | SpringerLink | 2020-01-01 to 2025-12-31 | 2026-04 |
| ScienceDirect | ScienceDirect (Elsevier) | 2020-01-01 to 2025-12-31 | 2026-04 |

## Search String

Boolean query used against IEEE Xplore, ACM Digital Library, SpringerLink, and EBSCO HOST:
```
("multi-cloud" OR "multi cloud" OR "multicloud")
AND
("governance" OR "security framework" OR "policy enforcement" OR "shared responsibility" OR "risk posture" OR "IAM" OR "identity federation")
AND
("cloud security" OR "cybersecurity" OR "information security")

```
Adapted query used against ScienceDirect (does not support the same nested quoted-phrase syntax):
```
multi-cloud
AND
(governance OR "security framework" OR "policy enforcement" OR "shared responsibility" OR "risk posture" OR IAM OR "identity federation")
AND
(cybersecurity OR "cloud security" OR "information security")
```

Field restrictions: Title/Abstract/Keywords
Document types included: peer-reviewed journal articles, conference papers
Language: English only

## Note on reporting

ETECOM 2026 Sec. III-A reports a simplified conceptual Boolean structure. The
strings above are the executed queries.

## Inclusion Criteria (for screening)

1. Peer-reviewed journal article or conference proceeding substantively addressing multi-cloud security, cloud governance, cybersecurity governance frameworks, CSPM, cloud IAM, shared responsibility, or cloud security systematic literature reviews
2. Indexed in IEEE Xplore, ACM Digital Library, SpringerLink, or ScienceDirect (EBSCO HOST was searched as a fifth database; see ../docs/known_issues.md, item 6)
3. Published between 2020 and 2025

## Exclusion Criteria (for screening)

See [../02_screening/exclusion_reasons.md](../02_screening/exclusion_reasons.md) for the standardized exclusion reason codes applied during screening.

## Snowballing / Supplementary Search

Forward and backward citation tracking was performed on three key sources identified during the primary database search: Diningrat et al. (2025), Aljarrah et al. (2024), and Alouffi et al. (2021). This added 3 records, 2 of which (AlGhamdi et al. 2020 and Pöhn & Hillmann 2021) were ultimately included in the final corpus. No grey literature or manual venue search was performed.
