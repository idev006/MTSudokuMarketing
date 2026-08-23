# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN PROGRESS** on the synchronized ultra-compact SYSTEM_INSTRUCTION_VERSION 1.6 candidate. TC-005 v1.6 rerun passed deterministic and competition-safety gates with a non-blocking rendering warning.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | IN_PROGRESS | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 next |
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

## TC-005 v1.6 Rerun Observations
- row_count_actual: 30
- chunking: 20 + 10
- stable CAMPAIGN_ID: `CMP-CP-UP-NAT-COMP-01-20260823`
- global SEQUENCE: 1..30 continuous
- controlled machine-token outer whitespace observed: 0
- row 1 `CAMPAIGN_ROLE`: exact `AWARENESS`
- IMAGE_PROMPT blank: yes
- competition positioning: training/preparation only
- approved grounding: 9x9 training content; custom multi-type/multi-difficulty training mix; 500 puzzles; answer key
- unsupported official/exam/endorsement/guaranteed-result claims observed: 0
- unsupported price/discount/deadline/stock/review/award/testimonial claims observed: 0

## Acceptance Defects
### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.6**.
- Initial occurrence: TC-003 v1.2 `OBJECTIVE=" CREATE_ENGAGEMENT"`.
- Recurrence: TC-005 v1.3 row 1 `CAMPAIGN_ROLE=" AWARENESS"`.
- TC-005 v1.6 rerun emits exact controlled tokens in observed rows, including row 1 `CAMPAIGN_ROLE="AWARENESS"`.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-005 v1.6 / NON-BLOCKING by itself**.
- Empty code fences continue to appear before TSV chunks despite documented rendering rule.
- Must be resolved/regression-tested before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.
- Continue checking large batches and machine-field correctness.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **IMPROVED / MONITOR**.
- v1.6 TC-005 rerun no longer repeatedly exposes internal policy/governance language in row copy; training/preparation is expressed in customer-facing language.
- Continue monitoring later competition and safety tests.

## Instruction Change Triggered by Builder Limit
SYSTEM_INSTRUCTION_VERSION advanced to **1.6** as an ultra-compact Builder-ready rewrite preserving the acceptance mitigations. Row schema, taxonomy, product truth, and prompt-template versions remain unchanged.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
Execute **TC-006** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the synchronized v1.6 candidate. Preserve raw response, validate all 60 rows across three chunks, verify stable CAMPAIGN_ID/global SEQUENCE/full-batch diversity/competition-safety claims, and write the result back to this SSOT before advancing.
