# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` and `marketing-content-os/docs/02_INSTRUCTION_AUTHORING_DRY_RUN_POLICY.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, generated prose, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

Instruction changes must include internal dry-run simulation before commit/merge: simulate affected acceptance behavior, iterate until expected pass or blocker, cap at 1,000 internal iterations, then still require real GPT Builder rerun and validation.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN_PROGRESS**.

TC-025 passed with warning on synchronized SYSTEM_INSTRUCTION_VERSION **1.11**. The batch emitted 20 rows, distributed visuals across 9 visual families, and no visual type exceeded 3/20 rows (15%), below the 25% visual concentration ceiling. Product grounding and template mapping passed. OUTPUT-FMT-001 remains reproduced and non-blocking by itself.

Continue to **TC-026**. Do not advance to TC-027 until TC-026 is executed and recorded.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE_FOR_RANGE | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 v1.7 rerun PASS_WITH_WARNING; TC-007 PASS; TC-008 PASS_WITH_WARNING |
| TC-009..TC-016 | COMPLETE_FOR_RANGE | TC-009 PASS_WITH_WARNING; TC-010 PASS_WITH_WARNING; TC-011 initial FAIL; TC-011 v1.8 rerun PASS_WITH_WARNING; TC-012 PASS_WITH_WARNING; TC-013 initial FAIL; TC-013 v1.9 rerun PASS_WITH_WARNING; TC-014 PASS_WITH_WARNING; TC-015 PASS_WITH_WARNING; TC-016 PASS_WITH_WARNING |
| TC-017..TC-024 | COMPLETE_FOR_RANGE | TC-017 PASS_WITH_WARNING; TC-018 PASS_WITH_WARNING; TC-019 PASS_WITH_WARNING; TC-020 PASS_WITH_WARNING; TC-021 PASS; TC-022 initial FAIL; TC-022 v1.10 rerun PASS; TC-023 initial FAIL; TC-023 v1.11 rerun PASS_WITH_WARNING; TC-024 PASS |
| TC-025..TC-032 | IN_PROGRESS | TC-025 PASS_WITH_WARNING; TC-026 next |

## Per-Test Evidence Record
| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Gate | Score | Evidence | Notes |
|---|---:|---:|---:|---|---:|---|---|
| TC-001 | PASS_WITH_WARNING | 1.2 | 1 | PASS | 43/45 | `tests/evidence/TC-001_2026-08-23_raw.md` | OUTPUT-FMT-001 recurred. |
| TC-002 | PASS_WITH_WARNING | 1.2 | 5 | PASS | 44/45 | `tests/evidence/TC-002_2026-08-23_raw.md` | OUTPUT-FMT-001 recurred. |
| TC-003 initial | FAIL | 1.2 | 20 | FAIL | n/a | `tests/evidence/TC-003_2026-08-23_review.md` | MACHINE-TOKEN-001 opened. |
| TC-003 rerun | PASS_WITH_WARNING | 1.3 | 20 | PASS | 44/45 | `tests/evidence/TC-003_2026-08-23_rerun_v1.3_review.md` | MACHINE-TOKEN-001 regression passed. |
| TC-004 | PASS_WITH_WARNING | 1.3 | 30 | PASS | 42/45 | `tests/evidence/TC-004_2026-08-23_raw.md` | Chunking/sequence/diversity/product truth pass. |
| TC-005 initial | FAIL | 1.3 | 30 | FAIL | n/a | `tests/evidence/TC-005_2026-08-23_review.md` | Leading whitespace in CAMPAIGN_ROLE. |
| TC-005 rerun | PASS_WITH_WARNING | 1.6 | 30 | PASS | 44/45 | `tests/evidence/TC-005_2026-08-23_rerun_v1.6_review.md` | Competition safety and machine-token regression passed. |
| TC-006 initial | FAIL | 1.6 | 60 | FAIL | n/a | `tests/evidence/TC-006_2026-08-23_review.md` | Wrong taxonomy-column token. |
| TC-006 rerun | PASS_WITH_WARNING | 1.7 | 60 | PASS | 44/45 | `tests/evidence/TC-006_2026-08-23_rerun_v1.7_review.md` | MACHINE-TOKEN-002 regression passed. |
| TC-007 | PASS | 1.7 | 0 | PASS | n/a | `tests/evidence/TC-007_2026-08-23_raw.md` | Invalid SKU rejected. |
| TC-008 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 43/45 | `tests/evidence/TC-008_2026-08-23_review.md` | DEVIL/GRANDMASTER positioning safe. |
| TC-009 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 44/45 | `tests/evidence/TC-009_2026-08-23_review.md` | Trustworthy/soft conversion override passed. |
| TC-010 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 44/45 | `tests/evidence/TC-010_2026-08-23_review.md` | Competition angles forbidden and absent. |
| TC-011 initial | FAIL | 1.7 | 0 | FAIL | n/a | `tests/evidence/TC-011_2026-08-23_review.md` | OVERRIDE-SAFETY-001 opened. |
| TC-011 rerun | PASS_WITH_WARNING | 1.8 | 20 | PASS | 44/45 | `tests/evidence/TC-011_2026-08-23_rerun_v1.8_review.md` | Unsafe endorsement rejected while generation continued. |
| TC-012 | PASS_WITH_WARNING | 1.8 | 20 | PASS | 44/45 | `tests/evidence/TC-012_2026-08-23_review.md` | Unsupported promotion/deadline rejected while generation continued. |
| TC-013 initial | FAIL | 1.8 | 30 | FAIL | n/a | `tests/evidence/TC-013_2026-08-23_review.md` | MACHINE-TOKEN-001 reopened. |
| TC-013 rerun | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-013_2026-08-24_rerun_v1.9_review.md` | LINE OA adaptation and whitespace regression passed. |
| TC-014 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-014_2026-08-24_review.md` | Marketplace adaptation passed. |
| TC-015 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-015_2026-08-24_review.md` | FORMULA mode passed. |
| TC-016 | PASS_WITH_WARNING | 1.9 | 5 | PASS | 44/45 | `tests/evidence/TC-016_2026-08-24_review.md` | 100% Product Hero override passed. |
| TC-017 | PASS_WITH_WARNING | 1.9 | 20 | PASS | 44/45 | `tests/evidence/TC-017_2026-08-24_review.md` | Upper-secondary EASY positioning passed. |
| TC-018 | PASS_WITH_WARNING | 1.9 | 20 | PASS | 44/45 | `tests/evidence/TC-018_2026-08-24_review.md` | Elementary EXPERT positioning passed. |
| TC-019 | PASS_WITH_WARNING | 1.9 | 5 | PASS | 44/45 | `tests/evidence/TC-019_2026-08-24_review.md` | Competition small-batch safety and diversity passed. |
| TC-020 | PASS_WITH_WARNING | 1.9 | 30 | PASS | 44/45 | `tests/evidence/TC-020_2026-08-24_review.md` | Prior challenge repetition avoided. |
| TC-021 | PASS | 1.9 | 0 | PASS | n/a | `tests/evidence/TC-021_2026-08-24_review.md` | Missing NUMBER_OF_ROWS failed safely. |
| TC-022 initial | FAIL | 1.9 | 20 | FAIL | n/a | `tests/evidence/TC-022_2026-08-24_review.md` | MISSING-INPUT-001 opened. |
| TC-022 rerun | PASS | 1.10 | 0 | PASS | n/a | `tests/evidence/TC-022_2026-08-24_rerun_v1.10_review.md` | Missing SKU failed safely. |
| TC-023 initial | FAIL | 1.10 | 0 | FAIL | n/a | `tests/evidence/TC-023_2026-08-24_review.md` | TEMPLATE-OVERRIDE-001 opened. |
| TC-023 rerun | PASS_WITH_WARNING | 1.11 | 10 | PASS | 44/45 | `tests/evidence/TC-023_2026-08-24_rerun_v1.11_review.md` | Unknown forced prompt template rejected; safe generation continued. |
| TC-024 | PASS | 1.11 | 0 | PASS | n/a | `tests/evidence/TC-024_2026-08-24_review.md` | Simulated Tier-1 conflict failed safely. |
| TC-025 | PASS_WITH_WARNING | 1.11 | 20 | PASS | 44/45 | `tests/evidence/TC-025_2026-08-24_review.md` | 9 visual families; max visual type 3/20 = 15%; OUTPUT-FMT-001 reproduced. |

## Latest Observations

### TC-025 Observations
- input SKU: `BK-LS-MIX-HARD-01`
- requested rows: 20
- requested platform: `Facebook`
- requested campaign goal: `AUTO`
- override: `REQUIRE_VISUAL_FAMILY_DIVERSITY`
- SYSTEM_INSTRUCTION_VERSION: `1.11`
- visual families observed: PRODUCT_HERO, STUDENT_ACTIVITY, PARENT_CHILD, INFOGRAPHIC, LIFESTYLE, TEACHER_CLASSROOM, PUZZLE_CHALLENGE, BENEFIT, PRODUCT_BOX
- visual_family_count: 9
- maximum single visual type frequency: 3/20 = 15%
- visual diversity requirement: PASS
- template mappings: PASS
- IMAGE_PROMPT blank: PASS
- Standard-SKU product grounding: PASS; approved `9x9 mixed Sudoku` scope only, no named variant membership or per-type counts
- deterministic/structural gate: PASS
- warning: OUTPUT-FMT-001 reproduced
- result: PASS_WITH_WARNING

## Acceptance Defects

### TEMPLATE-OVERRIDE-001 — Unknown forced prompt template stops generation instead of safe continuation
- Status: **RESOLVED / REGRESSION PASSED on v1.11 / MONITOR**.

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
- Status: **OPEN / REPRODUCED THROUGH TC-025 / NON-BLOCKING by itself**.
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
Execute **TC-026** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the synchronized v1.11 candidate. Preserve raw response, verify one physical TSV line per row, exactly 27 fields, and correct tab/newline escaping, then write the result back to this SSOT before advancing.
