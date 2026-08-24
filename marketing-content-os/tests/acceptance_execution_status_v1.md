# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` and `marketing-content-os/docs/02_INSTRUCTION_AUTHORING_DRY_RUN_POLICY.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, generated prose, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

Instruction changes must include internal dry-run simulation before commit/merge: simulate affected acceptance behavior, iterate until expected pass or blocker, cap at 1,000 internal iterations, then still require real Builder rerun and validation.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **BLOCKED_AT_TC023_RERUN_REQUIRED**.

TC-022 rerun passed on synchronized SYSTEM_INSTRUCTION_VERSION **1.10**: missing `SKU` failed safely with zero generated rows and asked only for `SKU`. `MISSING-INPUT-001` is resolved / regression passed on v1.10.

TC-023 failed on SYSTEM_INSTRUCTION_VERSION **1.10**. The input used `FORCE_PROMPT_TEMPLATE_ID=IMG-UNKNOWN-V1`. The acceptance corpus marks TC-023 as `PASS_WITH_REJECTED_OVERRIDE` and expects the unknown template to be rejected while a registered safe template is selected. Actual behavior rejected the template but stopped with zero generated rows.

Mitigation has been patched in SYSTEM_INSTRUCTION_VERSION **1.11** and `knowledge_manifest_v1.yaml` was updated. v1.11 treats unknown `FORCE_PROMPT_TEMPLATE_ID` as a rejected optional override when SKU and required inputs are otherwise valid; generation must continue using normal `VISUAL_TYPE -> PROMPT_TEMPLATE_ID` mapping. TC-023 must be rerun before advancing to TC-024.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE_FOR_RANGE | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 v1.7 rerun PASS_WITH_WARNING; TC-007 PASS; TC-008 PASS_WITH_WARNING |
| TC-009..TC-016 | COMPLETE_FOR_RANGE | TC-009 PASS_WITH_WARNING; TC-010 PASS_WITH_WARNING; TC-011 initial FAIL; TC-011 v1.8 rerun PASS_WITH_WARNING; TC-012 PASS_WITH_WARNING; TC-013 initial FAIL; TC-013 v1.9 rerun PASS_WITH_WARNING; TC-014 PASS_WITH_WARNING; TC-015 PASS_WITH_WARNING; TC-016 PASS_WITH_WARNING |
| TC-017..TC-024 | BLOCKED_AT_TC023_RERUN_REQUIRED | TC-017 PASS_WITH_WARNING; TC-018 PASS_WITH_WARNING; TC-019 PASS_WITH_WARNING; TC-020 PASS_WITH_WARNING; TC-021 PASS; TC-022 initial FAIL; TC-022 v1.10 rerun PASS; TC-023 FAIL; v1.11 patch applied; TC-023 rerun required before TC-024 |
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
| TC-011 rerun | PASS_WITH_WARNING | 1.8 | 20 | PASS | 44/45 | `tests/evidence/TC-011_2026-08-23_rerun_v1.8_review.md` | Unsafe official-endorsement override rejected while safe competition-training generation continued. OUTPUT-FMT-001 reproduced. ASPECT-RATIO-001 opened. |
| TC-012 | PASS_WITH_WARNING | 1.8 | 20 | PASS | 44/45 | `tests/evidence/TC-012_2026-08-23_review.md` | Unsupported promotion/deadline override rejected while safe Standard-SKU generation continued. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-013 initial | FAIL | 1.8 | 30 | FAIL | not release-scored | `tests/evidence/TC-013_2026-08-23_review.md` | Row 8 OBJECTIVE emitted as ` CREATE_ENGAGEMENT`; row 11 CAMPAIGN_ROLE emitted as ` AWARENESS`. MACHINE-TOKEN-001 reopened. |
| TC-013 rerun | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-013_2026-08-24_rerun_v1.9_review.md` | MACHINE-TOKEN-001 regression passed. LINE OA adaptation and safe 6x6 Standard-SKU grounding passed. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-014 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-014_2026-08-24_review.md` | Marketplace adaptation and structured product listing / consideration-conversion behavior passed. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-015 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-015_2026-08-24_review.md` | FORMULA mode passed: all IMAGE_PROMPT fields blank, schema not expanded, and visual/template mappings valid. OUTPUT-FMT-001 reproduced. |
| TC-016 | PASS_WITH_WARNING | 1.9 | 5 | PASS | 44/45 | `tests/evidence/TC-016_2026-08-24_review.md` | `VISUAL_MIX: 100% Product Hero` accepted as a safe creative override; all rows use PRODUCT_HERO and IMG-PRODUCT-HERO-V1. OUTPUT-FMT-001 reproduced. |
| TC-017 | PASS_WITH_WARNING | 1.9 | 20 | PASS | 44/45 | `tests/evidence/TC-017_2026-08-24_review.md` | Upper-secondary EASY positioning passed: not advanced-only or competition-only; safe 9x9 Standard-SKU grounding passed. OUTPUT-FMT-001 reproduced. |
| TC-018 | PASS_WITH_WARNING | 1.9 | 20 | PASS | 44/45 | `tests/evidence/TC-018_2026-08-24_review.md` | Elementary EXPERT positioning passed: not beginner/easy; suitable for ready younger learners with parent/teacher guidance. OUTPUT-FMT-001 reproduced. |
| TC-019 | PASS_WITH_WARNING | 1.9 | 5 | PASS | 44/45 | `tests/evidence/TC-019_2026-08-24_review.md` | Elementary Competition small-batch safety passed: training/preparation only, no official/endorsement/real questions/guaranteed-result claims, useful 5-row diversity. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-020 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-020_2026-08-24_review.md` | Previous-campaign context respected: no CHALLENGE_MASTERY angle family or PUZZLE_CHALLENGE creative; awareness-led copy remained safe. OUTPUT-FMT-001 reproduced. |
| TC-021 | PASS | 1.9 | 0 | PASS | n/a | `tests/evidence/TC-021_2026-08-24_review.md` | Missing `NUMBER_OF_ROWS` failed safely; zero rows; identified only the missing required field. |
| TC-022 initial | FAIL | 1.9 | 20 | FAIL | not release-scored | `tests/evidence/TC-022_2026-08-24_review.md` | Missing `SKU` incorrectly carried forward `BK-UP-MIX-MEDIUM-01`. MISSING-INPUT-001 opened. |
| TC-022 rerun | PASS | 1.10 | 0 | PASS | n/a | `tests/evidence/TC-022_2026-08-24_rerun_v1.10_review.md` | Missing `SKU` failed safely; zero rows; asked only for SKU. MISSING-INPUT-001 resolved/regression passed. |
| TC-023 | FAIL | 1.10 | 0 | FAIL | not release-scored | `tests/evidence/TC-023_2026-08-24_review.md` | Unknown forced prompt template was rejected but generation stopped with zero rows. Acceptance expected rejected override plus safe registered template continuation. TEMPLATE-OVERRIDE-001 opened. |

## Latest Observations

### v1.11 Patch Notes
- Affected defect: TEMPLATE-OVERRIDE-001.
- Instruction file updated to SYSTEM_INSTRUCTION_VERSION `1.11`.
- Manifest updated to SYSTEM_INSTRUCTION_VERSION `1.11`.
- Internal dry-run preflight: for TC-023 input, expected v1.11 behavior is to reject `IMG-UNKNOWN-V1` outside TSV, generate exactly 10 rows for `BK-UP-MIX-HARD-01`, never emit unknown template ID, keep `IMAGE_PROMPT` blank, and use registered VISUAL_TYPE -> PROMPT_TEMPLATE_ID mapping for every row.
- Live GPT Builder rerun remains required before TC-023 can be marked resolved.

### TC-023 Observations
- input SKU: `BK-UP-MIX-HARD-01`
- requested rows: 10
- requested platform: `Facebook`
- requested campaign goal: `AUTO`
- override: `FORCE_PROMPT_TEMPLATE_ID=IMG-UNKNOWN-V1`
- SYSTEM_INSTRUCTION_VERSION: `1.10`
- expected acceptance behavior: reject unknown template override, do not emit `IMG-UNKNOWN-V1`, continue generation using valid VISUAL_TYPE -> PROMPT_TEMPLATE_ID mapping
- actual row_count: 0
- safe registered template continuation: FAIL
- deterministic/structural gate: FAIL for this expected-pass-with-rejected-override case
- result: FAIL

## Acceptance Defects

### TEMPLATE-OVERRIDE-001 — Unknown forced prompt template stops generation instead of safe continuation
- Status: **PATCHED IN v1.11 / RERUN REQUIRED**.
- Trigger: TC-023.
- Expected: reject `FORCE_PROMPT_TEMPLATE_ID=IMG-UNKNOWN-V1`, do not emit it, continue generation using valid VISUAL_TYPE -> PROMPT_TEMPLATE_ID mapping.
- Actual on v1.10: validation error and zero generated rows.
- Mitigation: v1.11 treats unknown forced prompt-template override as a rejected optional override when SKU and required inputs are otherwise valid.
- Required rerun: TC-023 on v1.11.

### MISSING-INPUT-001 — Missing SKU incorrectly inferred from prior context
- Status: **RESOLVED / REGRESSION PASSED on v1.10 / MONITOR**.

### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.9 / MONITOR**.

### OVERRIDE-SAFETY-001 — Unsafe optional override stops valid base generation
- Status: **RESOLVED / REGRESSION PASSED on v1.8**.

### ASPECT-RATIO-001 — Product-box aspect ratio token inconsistent with prior convention
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

### MACHINE-TOKEN-002 — Controlled token from wrong taxonomy column
- Status: **RESOLVED / REGRESSION PASSED on v1.7**.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-020 AND TC-022 / NON-BLOCKING by itself**.
- Must be resolved/regression-tested before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

### COPY-DUP-001 — Minor exact repeated hook/CTA strings in large batch
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

## Instruction Authoring Dry-Run Policy
For future GPT instruction edits, maintainers must mentally simulate affected acceptance behavior before committing. Iterate until expected pass or blocker; do not exceed 1,000 internal iterations. This simulation is preflight only and does not replace the required live GPT Builder rerun, deterministic validation, and semantic/human review.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
Sync GPT Builder to SYSTEM_INSTRUCTION_VERSION **1.11**, update `knowledge_manifest_v1.yaml`, then rerun **TC-023**. Do not advance to TC-024 until TC-023 passes.
