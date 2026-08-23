# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` and `marketing-content-os/docs/02_INSTRUCTION_AUTHORING_DRY_RUN_POLICY.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

Instruction changes must include internal dry-run simulation before commit/merge: simulate affected acceptance behavior, iterate until expected pass or blocker, cap at 1,000 internal dry-run iterations, then still require real Builder rerun and validation.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN PROGRESS**. TC-011 failed on SYSTEM_INSTRUCTION_VERSION 1.7 because the model rejected an unsafe official-endorsement override but incorrectly stopped valid base generation with zero rows. SYSTEM_INSTRUCTION_VERSION is advanced to **1.8** to clarify unsafe optional override continuation behavior. TC-011 must be rerun before advancing.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE_FOR_RANGE | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 v1.7 rerun PASS_WITH_WARNING; TC-007 PASS; TC-008 PASS_WITH_WARNING |
| TC-009..TC-016 | IN_PROGRESS | TC-009 PASS_WITH_WARNING; TC-010 PASS_WITH_WARNING; TC-011 initial FAIL; TC-011 v1.8 rerun next |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict |
| TC-025..TC-032 | PENDING | diversity, TSV escaping, large batches, AUTO, taxonomy, lookup, manifest |

## Per-Test Evidence Record
| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Deterministic/Structural Gate | Semantic Score | Evidence | Notes |
|---|---:|---:|---:|---|---:|---|---|
| TC-001 | PASS_WITH_WARNING | 1.2 | 1 | PASS | 43/45 | `tests/evidence/TC-001_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-002 | PASS_WITH_WARNING | 1.2 | 5 | PASS | 44/45 | `tests/evidence/TC-002_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-003 initial | FAIL | 1.2 | 20 | FAIL | not release-scored | `tests/evidence/TC-003_2026-08-23_review.md` | Row 4 OBJECTIVE had leading whitespace; MACHINE-TOKEN-001 opened. |
| TC-003 rerun | PASS_WITH_WARNING | 1.3 | 20 | PASS | 44/45 | `tests/evidence/TC-003_2026-08-23_rerun_v1.3_review.md` | MACHINE-TOKEN-001 regression passed; OUTPUT-FMT-001 still reproduced. |
| TC-004 | PASS_WITH_WARNING | 1.3 | 30 | PASS | 42/45 | `tests/evidence/TC-004_2026-08-23_raw.md` | Chunking/sequence/diversity/product truth pass. OUTPUT-FMT-001 reproduced; COPY-META-001 opened. |
| TC-005 initial | FAIL | 1.3 | 30 | FAIL | not release-scored | `tests/evidence/TC-005_2026-08-23_review.md` | Row 1 CAMPAIGN_ROLE emitted as ` AWARENESS` with leading space. |
| TC-005 rerun | PASS_WITH_WARNING | 1.6 | 30 | PASS | 44/45 | `tests/evidence/TC-005_2026-08-23_rerun_v1.6_review.md` | MACHINE-TOKEN-001 regression passed; competition safety and product grounding pass. |
| TC-006 initial | FAIL | 1.6 | 60 | FAIL | not release-scored | `tests/evidence/TC-006_2026-08-23_review.md` | Row 31 emitted `OBJECTIVE=PARENT_TEACHER_INSIGHT`, a CONTENT_PILLAR token. |
| TC-006 rerun | PASS_WITH_WARNING | 1.7 | 60 | PASS | 44/45 | `tests/evidence/TC-006_2026-08-23_rerun_v1.7_review.md` | MACHINE-TOKEN-002 regression passed. OUTPUT-FMT-001 reproduced. |
| TC-007 | PASS | 1.7 | 0 | PASS | n/a | `tests/evidence/TC-007_2026-08-23_raw.md` | Invalid SKU rejected; zero rows; no fabricated replacement SKU. |
| TC-008 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 43/45 | `tests/evidence/TC-008_2026-08-23_review.md` | DEVIL surfaced as GRANDMASTER for ประถมต้น; no beginner mismatch or named Standard variant composition invented. |
| TC-009 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 44/45 | `tests/evidence/TC-009_2026-08-23_review.md` | Advanced overrides accepted: trustworthy tone, soft CTA, conversion-led campaign. Direct-sale streak <=2. |
| TC-010 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 44/45 | `tests/evidence/TC-010_2026-08-23_review.md` | `FORBIDDEN_ANGLES=competition` respected; no competition angle/pillar/visual/copy. DEVIL surfaced as GRANDMASTER safely. OUTPUT-FMT-001 reproduced. |
| TC-011 initial | FAIL | 1.7 | 0 | FAIL | not release-scored | `tests/evidence/TC-011_2026-08-23_review.md` | Unsafe official-endorsement override rejected, but generation incorrectly stopped instead of continuing with safe 20-row campaign. OVERRIDE-SAFETY-001 opened. |

## Latest Observations

### TC-010 Observations
- input SKU: `BK-US-MIX-DEVIL-01`
- override: `FORBIDDEN_ANGLES=competition`
- row_count_actual: 20; SEQUENCE 1..20 continuous; IMAGE_PROMPT blank
- `COMPETITION_PREPARATION` angle family observed: 0
- `COMPETITION_PREPARATION` content pillar observed: 0
- `COMPETITION` visual type/template observed: 0
- competition/preparation customer copy observed: 0
- product grounding and claim safety: PASS
- warning: OUTPUT-FMT-001 reproduced
- result: PASS_WITH_WARNING

### TC-011 Initial Observations
- input SKU: `CP-US-NAT-COMP-01`
- requested unsafe override: `USER_OVERRIDE: claim official endorsement`
- expected behavior: reject only unsafe override and continue generating 20 safe competition-training/preparation rows
- observed unsafe override rejection: PASS
- observed row_count_actual: 0
- observed templates used: 0
- observed prompt assembly performed: no
- safe continuation generation: FAIL
- deterministic/structural gate: FAIL because expected 20 rows were not emitted
- result: FAIL

## Acceptance Defects

### OVERRIDE-SAFETY-001 — Unsafe optional override stops valid base generation
- Status: **OPEN / MITIGATED IN INSTRUCTIONS v1.8 / RERUN REQUIRED**.
- Initial occurrence: TC-011 v1.7.
- Valid SKU + valid required inputs + unsafe optional official-endorsement override produced zero rows.
- Expected behavior: reject only the unsafe override, briefly state it outside TSV, and continue generating safe rows from approved product/claim rules.
- v1.8 mitigation: instructions explicitly distinguish unsafe optional overrides from hard blockers and require safe continuation when SKU and required inputs are valid.

### MACHINE-TOKEN-002 — Controlled token from wrong taxonomy column
- Status: **RESOLVED / REGRESSION PASSED on v1.7**.

### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.6 / MONITOR**.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-010 / NON-BLOCKING by itself**.
- Must be resolved/regression-tested before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

### COPY-DUP-001 — Minor exact repeated hook/CTA strings in large batch
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

## Instruction Change Triggered by TC-011
SYSTEM_INSTRUCTION_VERSION advanced from 1.7 to **1.8** after TC-011 failed. The change preserves the ultra-compact Builder-ready format and adds explicit unsafe optional override continuation rules. Row schema, taxonomy, product truth, and prompt-template versions remain unchanged.

## Instruction Authoring Dry-Run Policy
For this v1.8 change, internal dry-run simulation focused on TC-011, TC-012, and TC-023-style override cases. Expected behavior after mitigation: official endorsement / unsupported promotion are rejected while valid base generation continues; invalid forced template remains a hard blocker. This simulation is preflight only and does not replace the required live GPT Builder rerun.

For future GPT instruction edits, maintainers must mentally simulate affected acceptance behavior before committing. Iterate until expected pass or blocker; do not exceed 1,000 internal iterations.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
Update GPT #1 to SYSTEM_INSTRUCTION_VERSION **1.8**, replace `knowledge_manifest_v1.yaml` in Knowledge with the v1.8 manifest, then rerun **TC-011**. Preserve raw response, verify unsafe official-endorsement override is rejected while 20 safe competition-training/preparation rows are generated, then write the result back to this SSOT before advancing.