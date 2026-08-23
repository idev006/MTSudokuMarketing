# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` and `marketing-content-os/docs/02_INSTRUCTION_AUTHORING_DRY_RUN_POLICY.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

Instruction changes must include internal dry-run simulation before commit/merge: simulate affected acceptance behavior, iterate until expected pass or blocker, cap at 1,000 internal iterations, then still require real Builder rerun and validation.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN_PROGRESS**. TC-016 passed on synchronized SYSTEM_INSTRUCTION_VERSION **1.9**: the `VISUAL_MIX: 100% Product Hero` override was accepted safely, all 5 rows used `PRODUCT_HERO` with `IMG-PRODUCT-HERO-V1`, and deterministic schema/template behavior passed. TC-009..TC-016 is now **COMPLETE_FOR_RANGE**. Continue to **TC-017**.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE_FOR_RANGE | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 v1.7 rerun PASS_WITH_WARNING; TC-007 PASS; TC-008 PASS_WITH_WARNING |
| TC-009..TC-016 | COMPLETE_FOR_RANGE | TC-009 PASS_WITH_WARNING; TC-010 PASS_WITH_WARNING; TC-011 initial FAIL; TC-011 v1.8 rerun PASS_WITH_WARNING; TC-012 PASS_WITH_WARNING; TC-013 initial FAIL; TC-013 v1.9 rerun PASS_WITH_WARNING; TC-014 PASS_WITH_WARNING; TC-015 PASS_WITH_WARNING; TC-016 PASS_WITH_WARNING |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict; TC-017 next |
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
| TC-011 rerun | PASS_WITH_WARNING | 1.8 | 20 | PASS | 44/45 | `tests/evidence/TC-011_2026-08-23_rerun_v1.8_review.md` | Unsafe official-endorsement override rejected while safe competition-training generation continued. OUTPUT-FMT-001 reproduced. ASPECT-RATIO-001 opened as non-blocking monitor warning. |
| TC-012 | PASS_WITH_WARNING | 1.8 | 20 | PASS | 44/45 | `tests/evidence/TC-012_2026-08-23_review.md` | Unsupported promotion/deadline override rejected while safe Standard-SKU generation continued. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-013 initial | FAIL | 1.8 | 30 | FAIL | not release-scored | `tests/evidence/TC-013_2026-08-23_review.md` | Row 8 OBJECTIVE emitted as ` CREATE_ENGAGEMENT`; row 11 CAMPAIGN_ROLE emitted as ` AWARENESS`. MACHINE-TOKEN-001 reopened. |
| TC-013 rerun | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-013_2026-08-24_rerun_v1.9_review.md` | MACHINE-TOKEN-001 regression passed. LINE OA adaptation and safe 6x6 Standard-SKU grounding passed. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-014 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-014_2026-08-24_review.md` | Marketplace adaptation and structured product listing / consideration-conversion behavior passed. Safe 9x9 Standard-SKU grounding passed. OUTPUT-FMT-001 and ASPECT-RATIO-001 reproduced. |
| TC-015 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-015_2026-08-24_review.md` | FORMULA mode passed: all IMAGE_PROMPT fields blank, schema not expanded, and visual/template mappings valid. OUTPUT-FMT-001 reproduced. |
| TC-016 | PASS_WITH_WARNING | 1.9 | 5 | PASS | 44/45 | `tests/evidence/TC-016_2026-08-24_review.md` | `VISUAL_MIX: 100% Product Hero` accepted as a safe creative override; all rows use PRODUCT_HERO and IMG-PRODUCT-HERO-V1. OUTPUT-FMT-001 reproduced. |

## Latest Observations

### TC-016 Observations
- input SKU: `BK-UP-MIX-EXPERT-01`
- requested platform: `Facebook`
- requested `VISUAL_MIX: 100% Product Hero`
- SYSTEM_INSTRUCTION_VERSION: `1.9`
- row_count_actual: 5
- unique_ROW_ID_count: 5
- stable CAMPAIGN_ID: `CMP-BK-UP-MIX-EXPERT-01-FACEBOOK-20260824`
- PLATFORM resolved to `FACEBOOK`
- global SEQUENCE: 1..5 continuous
- every emitted row has exactly 27 tab-delimited fields
- controlled machine-token errors: 0
- controlled machine-token outer whitespace observed: 0
- visual override handling: PASS
- VISUAL_TYPE: `PRODUCT_HERO` in all 5 rows
- PROMPT_TEMPLATE_ID: `IMG-PRODUCT-HERO-V1` in all 5 rows
- IMAGE_PROMPT blank: yes, all 5 rows
- schema expansion observed: 0
- template mappings: PASS
- product grounding: 9x9 generic mixed Sudoku, ประถมปลาย, EXPERT, 500 puzzles, answer key, Printable PDF
- named Standard variant composition or per-type count invention observed: 0
- unsupported price/discount/deadline/scarcity/stock/review/award/endorsement/guarantee claims observed: 0
- warning: OUTPUT-FMT-001 reproduced
- visual concentration warning: not applicable because the visual concentration was explicitly requested and allowed by TC-016
- deterministic/structural gate: PASS
- result: PASS_WITH_WARNING

## Acceptance Defects

### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.9 / MONITOR**.
- Earlier recurrence: TC-013 v1.8 row 8 `OBJECTIVE= CREATE_ENGAGEMENT`; row 11 `CAMPAIGN_ROLE= AWARENESS`.
- v1.9 reruns: no leading/trailing whitespace observed in controlled machine-token fields through TC-016.

### OVERRIDE-SAFETY-001 — Unsafe optional override stops valid base generation
- Status: **RESOLVED / REGRESSION PASSED on v1.8**.

### ASPECT-RATIO-001 — Product-box aspect ratio token inconsistent with prior convention
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.
- TC-011, TC-012, TC-013 initial, TC-013 v1.9 rerun, and TC-014 PRODUCT_BOX rows used `1236:2000` in ASPECT_RATIO.
- TC-015 and TC-016 did not newly reproduce this warning because Facebook portrait rows used `4:5` and `1080x1350 px`.

### MACHINE-TOKEN-002 — Controlled token from wrong taxonomy column
- Status: **RESOLVED / REGRESSION PASSED on v1.7**.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-016 / NON-BLOCKING by itself**.
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
Execute **TC-017** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the synchronized v1.9 candidate. Preserve raw response, verify the upper-secondary EASY campaign is not positioned only for advanced/competition audiences, and write the result back to this SSOT before advancing.
