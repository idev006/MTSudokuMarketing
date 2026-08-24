# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` and `marketing-content-os/docs/02_INSTRUCTION_AUTHORING_DRY_RUN_POLICY.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, generated prose, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

Instruction changes must include internal dry-run simulation before commit/merge: simulate affected acceptance behavior, iterate until expected pass or blocker, cap at 1,000 internal iterations, then still require real GPT Builder rerun and validation.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **EXECUTED_COMPLETE_WITH_WARNINGS**.

GPT #1 remains **CANDIDATE / NOT PRODUCTION** until v1.12 focused regression is run and recorded. The 27-field row contract is stable for GPT #2 preparation, but production freeze waits for format cleanup.

## Current Version Position
- Last accepted live GPT Builder version: **SYSTEM_INSTRUCTION_VERSION 1.11**.
- Patch prepared in repo: **SYSTEM_INSTRUCTION_VERSION 1.12**.
- v1.12 purpose: close `OUTPUT-FMT-001` by forbidding empty/generic/placeholder code fences and requiring exactly one fenced `tsv` block per part.
- v1.12 live rerun status: **REQUIRED**.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE_FOR_RANGE | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 v1.7 rerun PASS_WITH_WARNING; TC-007 PASS; TC-008 PASS_WITH_WARNING |
| TC-009..TC-016 | COMPLETE_FOR_RANGE | TC-009 PASS_WITH_WARNING; TC-010 PASS_WITH_WARNING; TC-011 initial FAIL; TC-011 v1.8 rerun PASS_WITH_WARNING; TC-012 PASS_WITH_WARNING; TC-013 initial FAIL; TC-013 v1.9 rerun PASS_WITH_WARNING; TC-014 PASS_WITH_WARNING; TC-015 PASS_WITH_WARNING; TC-016 PASS_WITH_WARNING |
| TC-017..TC-024 | COMPLETE_FOR_RANGE | TC-017 PASS_WITH_WARNING; TC-018 PASS_WITH_WARNING; TC-019 PASS_WITH_WARNING; TC-020 PASS_WITH_WARNING; TC-021 PASS; TC-022 initial FAIL; TC-022 v1.10 rerun PASS; TC-023 initial FAIL; TC-023 v1.11 rerun PASS_WITH_WARNING; TC-024 PASS |
| TC-025..TC-032 | COMPLETE_FOR_RANGE | TC-025 PASS_WITH_WARNING; TC-026 PASS_WITH_WARNING; TC-027 PASS_WITH_WARNING; TC-028 PASS_WITH_WARNING; TC-029 PASS_WITH_WARNING; TC-030 PASS_WITH_WARNING; TC-031 PASS_WITH_WARNING; TC-032 PASS_WITH_WARNING |

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
| TC-026 | PASS_WITH_WARNING | 1.11 | 5 | PASS | 44/45 | `tests/evidence/TC-026_2026-08-24_review.md` | TSV escaping passed. OUTPUT-FMT-001 reproduced. |
| TC-027 | PASS_WITH_WARNING | 1.11 | 60 | PASS | 44/45 | `tests/evidence/TC-027_2026-08-24_review.md` | Large batch passed. OUTPUT-FMT-001 reproduced. |
| TC-028 | PASS_WITH_WARNING | 1.11 | 20 | PASS | 44/45 | `tests/evidence/TC-028_2026-08-24_review.md` | AUTO platform resolution passed: all rows `FACEBOOK`, no row kept `AUTO`. OUTPUT-FMT-001 reproduced. |
| TC-029 | PASS_WITH_WARNING | 1.11 | 30 | PASS | 44/45 | `tests/evidence/TC-029_2026-08-24_review.md` | CAMPAIGN_DURATION=AUTO inferred campaign arc, not 30 rows = 30 days. OUTPUT-FMT-001 reproduced. |
| TC-030 | PASS_WITH_WARNING | 1.11 | 10 | PASS | 44/45 | `tests/evidence/TC-030_2026-08-24_review.md` | Controlled vocabulary validation passed. OUTPUT-FMT-001 reproduced. |
| TC-031 | PASS_WITH_WARNING | 1.11 | 10 | PASS | 44/45 | `tests/evidence/TC-031_2026-08-24_review.md` | SKU lookup prompt assembly passed. OUTPUT-FMT-001 reproduced. |
| TC-032 | PASS_WITH_WARNING | 1.11 | 10 | PASS | 44/45 | `tests/evidence/TC-032_2026-08-24_review.md` | Knowledge manifest requirement passed. OUTPUT-FMT-001 reproduced. |

## Latest Observations

### Final TC-001..TC-032 Rollup
- All acceptance tests TC-001..TC-032 have been executed.
- No unresolved hard failure remains in the 27-field row contract.
- Product grounding passed with Standard-SKU exact composition kept UNSPECIFIED and expressed only as approved grid + generic `mixed Sudoku`.
- Competition safety passed after unsafe official/endorsement claims were rejected or avoided.
- Formula Mode passed: `IMAGE_PROMPT` remained blank and prompt assembly was deferred to content row + SKU lookup + registered template.
- Missing input isolation passed after v1.10.
- Unknown forced template override passed after v1.11.
- `OUTPUT-FMT-001` remains the main release cleanup item.

### v1.12 Patch Notes
- Affected defect: OUTPUT-FMT-001.
- Patch type: format-only instruction cleanup.
- Product truth impact: none.
- Row schema impact: none.
- Template mapping impact: none.
- Required live rerun: focused format regression before Production v1.0.

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
- Status: **OPEN / PATCHED IN v1.12 / LIVE REGRESSION REQUIRED / RELEASE-BLOCKING CLEANUP**.
- Reproduced through TC-032 on v1.11.
- v1.12 adds a strict no-empty-fence rule.
- Must be resolved/regression-tested before Production v1.0 unless a deterministic post-processor mitigation is approved.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

### COPY-DUP-001 — Minor exact repeated hook/CTA strings in large batch
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.

## v1.12 Focused Regression Plan
Run after syncing GPT Builder Instructions and manifest to v1.12.

### FMT-R001
```text
SKU: BK-EL-MIX-EASY-01
NUMBER_OF_ROWS: 1
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```
Expected: 1 row, one `tsv` block, no empty code fence.

### FMT-R002
```text
SKU: BK-US-MIX-EXPERT-01
NUMBER_OF_ROWS: 60
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
LARGE_BATCH_PROTOCOL
```
Expected: 60 rows, 3 parts, one `tsv` block per part, no empty code fence before any part.

### FMT-R003
```text
SKU: BK-UP-MIX-MEDIUM-01
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
KNOWLEDGE_MANIFEST_REQUIRED
```
Expected: manifest metadata preserved, 10 rows, no empty code fence.

## GPT #2 Status
GPT #2 remains **PREP READY / WAITING FOR GPT #1 v1.12 FORMAT REGRESSION**.

GPT #2 activation checklist: `marketing-content-os/gpt/visual_prompt_refiner/activation_checklist_v1.md`.

## Release Rule
Do not freeze GPT #1 as Production v1.0 until TC-001..TC-032 evidence is complete, v1.12 focused regression is recorded, and `OUTPUT-FMT-001` is closed or explicitly mitigated. GPT #2 can be prepared as a candidate after v1.12 focused regression passes, then must pass its own acceptance corpus before production.

## Immediate Next Action
Sync GPT Builder to SYSTEM_INSTRUCTION_VERSION **1.12**, replace `knowledge_manifest_v1.yaml` with the v1.12 manifest, then run **FMT-R001** first. Preserve raw response and record evidence before running FMT-R002.
