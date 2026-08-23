# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **BLOCKED AT TC-003** pending regression rerun with SYSTEM_INSTRUCTION_VERSION 1.3.

Before each acceptance run, verify the live GPT candidate remains synchronized with:
- latest `gpt/campaign_content_generator/system_instructions_v1.md`;
- latest `knowledge_manifest_v1.yaml`;
- exact current Knowledge bundle documented in `gpt/campaign_content_generator/gpt_builder_config_v1.md`;
- acceptance-time capabilities aligned with the Builder config.

If the live Builder state differs from GitHub, update the Builder to match GitHub before continuing. Do not treat Builder-only edits as project truth.

## Smoke Evidence
- Smoke #1 Standard SKU / N=1: PASS
- Smoke #2 Competition SKU / N=5: PASS
- Smoke #3 Invalid SKU: PASS
- Smoke #4 Unsupported promotion/endorsement override: PASS
- Smoke #5 N=30 chunking: PASS_WITH_MINOR_WARNING

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | BLOCKED | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 FAIL and requires rerun on v1.3 |
| TC-009..TC-016 | PENDING | Advanced overrides, safety, Formula, visual override |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict |
| TC-025..TC-032 | PENDING | diversity, TSV escaping, large batches, AUTO, taxonomy, lookup, manifest |

## Execution Method
For each GPT answer:
1. Save durable evidence.
2. Record test ID, candidate/instruction version, execution date, and evidence path.
3. Extract logical TSV when rows are expected.
4. Run deterministic validation against canonical lookup/taxonomy/template files.
5. For N>=20, run batch audit metrics from actual rows.
6. Apply semantic/human rubric.
7. Record PASS / PASS_WITH_WARNING / FAIL plus evidence and key metrics.
8. On FAIL, update governing documents/config/code first, rerun affected tests, and record regression evidence before advancing.

## Per-Test Evidence Record
| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Deterministic Validator | Semantic Score | Evidence | Notes |
|---|---|---|---:|---|---:|---|---|
| TC-001 | PASS_WITH_WARNING | 1.2 | 1 | PASS | 43/45 | `tests/evidence/TC-001_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-002 | PASS_WITH_WARNING | 1.2 | 5 | PASS | 44/45 | `tests/evidence/TC-002_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-003 | FAIL | 1.2 | 20 | FAIL | not release-scored due hard failure | `tests/evidence/TC-003_2026-08-23_review.md` | Row 4 OBJECTIVE emitted as ` CREATE_ENGAGEMENT` with leading space. Canonical token mismatch is a hard schema/taxonomy failure. Post-hoc prose correction is invalid. Acceptance blocked pending v1.3 regression rerun. |

## TC-003 Batch Audit
- row_count_actual: 20
- unique_row_id_count: 20
- sequence_min/max: 1/20, continuous
- stable CAMPAIGN_ID: yes
- direct_sale_max_consecutive: 1
- top_angle_share: 15%
- top_visual_type_share: 15%
- exact duplicate hooks: 0
- exact duplicate CTAs: 0
- unsafe_claim_count observed: 0
- fabricated_fact_count observed: 0
- deterministic failure: row 4 non-canonical `OBJECTIVE`

## Open Acceptance Defects
### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: OPEN / BLOCKING / FIX IMPLEMENTED IN v1.3 / REGRESSION REQUIRED.
- First observed: TC-003 row 4 `OBJECTIVE=" CREATE_ENGAGEMENT"`.
- Impact: deterministic taxonomy validation fails; machine consumers cannot treat the row as canonical.
- v1.3 mitigation: exact token rule, mandatory field trim, final emitted-row canonical validation, and prohibition on post-hoc prose correction.
- Closure rule: rerun TC-003 on synchronized v1.3 candidate and obtain deterministic PASS.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: OPEN / REPRODUCED THROUGH TC-003 / NON-BLOCKING by itself.
- Impact: presentation clutter and parser friction.
- Closure rule: later synchronized regression run must show no empty fence.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: OPEN / REGRESSION REQUIRED.
- TC-003 showed the model noticed a serialization defect after emission but attempted to correct it in prose instead of repairing the TSV.
- v1.3 explicitly forbids this behavior.

## Instruction Change Triggered by TC-003
SYSTEM_INSTRUCTION_VERSION advanced from 1.2 to **1.3**. Row schema, taxonomy version, product truth, and prompt-template version remain unchanged.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence.

GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
1. Synchronize the live GPT #1 Builder with `system_instructions_v1.md` version 1.3.
2. Replace the Builder Knowledge `knowledge_manifest_v1.yaml` with the current v1.3 manifest.
3. Save/Update the GPT candidate.
4. **Rerun TC-003 with the same input.**
5. Do not execute TC-004 until TC-003 regression passes deterministic validation.
