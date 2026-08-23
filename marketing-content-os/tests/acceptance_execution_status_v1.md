# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **BLOCKED AT TC-006**. TC-006 on SYSTEM_INSTRUCTION_VERSION 1.6 reproduced a blocking controlled-token error where a CONTENT_PILLAR token was emitted in the OBJECTIVE column. SYSTEM_INSTRUCTION_VERSION 1.7 is implemented and requires live Builder synchronization plus TC-006 regression rerun.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | BLOCKED | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 FAIL on v1.6; rerun required on v1.7 |
| TC-009..TC-016 | PENDING | Advanced overrides, safety, Formula, visual override |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict |
| TC-025..TC-032 | PENDING | diversity, TSV escaping, large batches, AUTO, taxonomy, lookup, manifest |

## Per-Test Evidence Record
| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Deterministic/Structural Gate | Semantic Score | Evidence | Notes |
|---|---|---|---:|---|---:|---|---|
| TC-001 | PASS_WITH_WARNING | 1.2 | 1 | PASS | 43/45 | `tests/evidence/TC-001_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-002 | PASS_WITH_WARNING | 1.2 | 5 | PASS | 44/45 | `tests/evidence/TC-002_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-003 initial | FAIL | 1.2 | 20 | FAIL | not release-scored | `tests/evidence/TC-003_2026-08-23_review.md` | Row 4 OBJECTIVE had leading whitespace; MACHINE-TOKEN-001 opened. |
| TC-003 rerun | PASS_WITH_WARNING | 1.3 | 20 | PASS | 44/45 | `tests/evidence/TC-003_2026-08-23_rerun_v1.3_review.md` | MACHINE-TOKEN-001 regression passed; OUTPUT-FMT-001 still reproduced. |
| TC-004 | PASS_WITH_WARNING | 1.3 | 30 | PASS | 42/45 | `tests/evidence/TC-004_2026-08-23_raw.md` | 20+10 chunking, stable campaign, global sequence/diversity/product truth pass. OUTPUT-FMT-001 reproduced; COPY-META-001 opened. |
| TC-005 initial | FAIL | 1.3 | 30 | FAIL | not release-scored | `tests/evidence/TC-005_2026-08-23_review.md` | Row 1 CAMPAIGN_ROLE emitted as ` AWARENESS` with leading space. Competition safety itself passed. MACHINE-TOKEN-001 reopened. COPY-META-001 also recurred. |
| TC-005 rerun | PASS_WITH_WARNING | 1.6 | 30 | PASS | 44/45 | `tests/evidence/TC-005_2026-08-23_rerun_v1.6_review.md` | MACHINE-TOKEN-001 regression passed; competition safety and product grounding pass. COPY-META-001 materially improved. OUTPUT-FMT-001 still reproduced. |
| TC-006 initial | FAIL | 1.6 | 60 | FAIL | not release-scored | `tests/evidence/TC-006_2026-08-23_review.md` | Row 31 emitted `OBJECTIVE=PARENT_TEACHER_INSIGHT`, which is a CONTENT_PILLAR token, not an OBJECTIVE token. MACHINE-TOKEN-002 opened. |

## TC-006 Observations
- row_count_actual: 60
- chunking: 20 + 20 + 20
- unique_ROW_ID_count: 60
- stable CAMPAIGN_ID: `CMP-CP-LS-NAT-COMP-01-20260823`
- global SEQUENCE: 1..60 continuous
- field count: 27 fields per data row
- IMAGE_PROMPT blank: yes
- direct_sale_max_consecutive: 1
- top_angle_share: 8.33% (12 angle families, 5 rows each)
- top_visual_type_share: 10.00% (10 visual types, 6 rows each)
- exact duplicate hook count: 0
- exact duplicate CTA count: 0
- competition positioning: training/preparation only
- unsupported official/exam/endorsement/guaranteed-result claims observed: 0
- deterministic blocker: row 31 `OBJECTIVE=PARENT_TEACHER_INSIGHT`

## Acceptance Defects

### MACHINE-TOKEN-002 — Controlled token from wrong taxonomy column
- Status: **OPEN / BLOCKING / v1.7 FIX IMPLEMENTED / REGRESSION REQUIRED**.
- Initial occurrence: TC-006 v1.6 row 31 `OBJECTIVE=PARENT_TEACHER_INSIGHT`.
- `PARENT_TEACHER_INSIGHT` is valid only as CONTENT_PILLAR; it is not valid as OBJECTIVE.
- v1.7 mitigation: instructions now require column-specific token-set validation and explicitly forbid using a token from another controlled column.
- Closure rule: TC-006 rerun on synchronized v1.7 must pass deterministic validation.

### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.6**.
- No outer-whitespace recurrence observed in TC-006; keep monitoring.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-006 / NON-BLOCKING by itself**.
- Empty code fences continue to appear before TSV chunks despite documented rendering rule.
- Must be resolved/regression-tested before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.
- Continue checking large batches and machine-field correctness.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **IMPROVED / MONITOR**.
- No material recurrence observed in TC-006.

## Instruction Change Triggered by TC-006
SYSTEM_INSTRUCTION_VERSION advanced from 1.6 to **1.7**. The change preserves the ultra-compact Builder-ready format and adds explicit column-specific controlled-token validation. Row schema, taxonomy, product truth, and prompt-template versions remain unchanged.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
1. Synchronize live GPT #1 Builder Instructions with `system_instructions_v1.md` version 1.7.
2. Replace Builder Knowledge `knowledge_manifest_v1.yaml` with the current manifest showing `SYSTEM_INSTRUCTION_VERSION: 1.7`.
3. Save/Update the GPT candidate.
4. Rerun **TC-006 with exactly the same input**.
5. Do not execute TC-007 until TC-006 passes deterministic validation.
