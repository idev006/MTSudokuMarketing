# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **BLOCKED AT TC-005**. TC-005 on SYSTEM_INSTRUCTION_VERSION 1.3 reproduced a blocking controlled-token whitespace defect. v1.4 mitigation was implemented, but full Builder Instructions exceeded the GPT Builder character limit. v1.5 was still too long in the live Builder. SYSTEM_INSTRUCTION_VERSION 1.6 is an ultra-compact Builder-ready form and requires live Builder synchronization plus TC-005 regression rerun.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | BLOCKED | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 FAIL on v1.3; rerun required on ultra-compact v1.6 |
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
| TC-005 | FAIL | 1.3 | 30 | FAIL | not release-scored | `tests/evidence/TC-005_2026-08-23_review.md` | Row 1 CAMPAIGN_ROLE emitted as ` AWARENESS` with leading space. Competition safety itself passed. MACHINE-TOKEN-001 reopened. COPY-META-001 also recurred. |

## TC-005 Observations
- row_count_actual: 30
- chunking: 20 + 10
- unique ROW_ID and global sequence 1..30: structurally present
- stable CAMPAIGN_ID: `CMP-CP-UP-NAT-COMP-01-20260823`
- competition positioning: training/preparation only
- unsupported official/exam/endorsement/guaranteed-result claims observed: 0
- approved grounding: 9x9 custom multi-type/multi-difficulty training mix; 500 puzzles; answer key
- IMAGE_PROMPT blank: yes
- deterministic blocker: row 1 `CAMPAIGN_ROLE=" AWARENESS"`

## Acceptance Defects
### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **REOPENED / BLOCKING / v1.6 BUILDER-READY FIX IMPLEMENTED / REGRESSION REQUIRED**.
- Initial occurrence: TC-003 v1.2 `OBJECTIVE=" CREATE_ENGAGEMENT"`.
- TC-003 v1.3 rerun passed.
- Recurrence: TC-005 v1.3 row 1 `CAMPAIGN_ROLE=" AWARENESS"`.
- v1.6 mitigation: ultra-compact Builder instructions preserve exact-copy canonical tokens, sanitized 27-field arrays, TAB-only joins, parse-back validation, and repair-before-output while fitting under the Builder limit.
- Closure rule: TC-005 rerun on synchronized v1.6 must pass deterministic validation.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-005 / NON-BLOCKING by itself**.
- Empty code fences continue to appear before TSV chunks despite documented rendering rule.
- Must be resolved/regression-tested before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.
- Continue checking large batches and machine-field correctness.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **OPEN / REPRODUCED IN TC-005 / v1.6 MITIGATION IMPLEMENTED**.
- v1.6 keeps governance/safety rationale outside customer-facing row fields.

## Instruction Change Triggered by Builder Limit
SYSTEM_INSTRUCTION_VERSION advanced from 1.5 to **1.6**. The change is an ultra-compact Builder-ready rewrite preserving the acceptance mitigations. Row schema, taxonomy, product truth, and prompt-template versions remain unchanged.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
1. Synchronize live GPT #1 Builder Instructions with ultra-compact `system_instructions_v1.md` version 1.6.
2. Replace Builder Knowledge `knowledge_manifest_v1.yaml` with the current manifest showing `SYSTEM_INSTRUCTION_VERSION: 1.6`.
3. Save/Update the GPT candidate.
4. Rerun **TC-005 with exactly the same input**.
5. Do not execute TC-006 until TC-005 passes deterministic validation.
