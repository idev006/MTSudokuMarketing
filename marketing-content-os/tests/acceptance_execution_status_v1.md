# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` and `marketing-content-os/docs/02_INSTRUCTION_AUTHORING_DRY_RUN_POLICY.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

Instruction changes must now include internal dry-run simulation before commit/merge: simulate affected acceptance behavior, iterate until expected pass or blocker, cap at 1,000 internal dry-run iterations, then still require real Builder rerun and validation.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN PROGRESS** on the synchronized SYSTEM_INSTRUCTION_VERSION 1.7 candidate. TC-008 passed DEVIL/GRANDMASTER positioning for the elementary Standard SKU with non-blocking warnings.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE_FOR_RANGE | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 v1.6 rerun PASS_WITH_WARNING; TC-006 v1.7 rerun PASS_WITH_WARNING; TC-007 PASS; TC-008 PASS_WITH_WARNING |
| TC-009..TC-016 | PENDING | Advanced overrides, safety, Formula, visual override; TC-009 next |
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
| TC-006 rerun | PASS_WITH_WARNING | 1.7 | 60 | PASS | 44/45 | `tests/evidence/TC-006_2026-08-23_rerun_v1.7_review.md` | MACHINE-TOKEN-002 regression passed. OUTPUT-FMT-001 reproduced. Minor exact duplicate hook/CTA patterns observed in a 60-row batch. |
| TC-007 | PASS | 1.7 | 0 | PASS | n/a | `tests/evidence/TC-007_2026-08-23_raw.md` | Invalid SKU rejected; zero rows; no fabricated replacement SKU; no templates or prompt assembly used. |
| TC-008 | PASS_WITH_WARNING | 1.7 | 20 | PASS | 43/45 | `tests/evidence/TC-008_2026-08-23_review.md` | DEVIL correctly surfaced as customer-facing GRANDMASTER for ประถมต้น; no beginner mismatch or named Standard variant composition invented. OUTPUT-FMT-001 reproduced; minor COPY-META-001 wording observed. |

## TC-006 v1.7 Rerun Observations
- row_count_actual: 60
- chunking: 20 + 20 + 20
- unique_ROW_ID_count: 60
- stable CAMPAIGN_ID: `CMP-CP-LS-NAT-COMP-01-20260823`
- global SEQUENCE: 1..60 continuous
- field count: 27 fields per data row
- controlled machine-token errors: 0
- controlled machine-token outer whitespace observed: 0
- row 31 `OBJECTIVE=BUILD_TRUST`; row 31 `CONTENT_PILLAR=PARENT_TEACHER_INSIGHT`
- IMAGE_PROMPT blank: yes
- direct_sale_max_consecutive: 1
- top_angle_share: 8.33% (12 angle families, 5 rows each)
- top_visual_type_share: 10.00% (10 visual types, 6 rows each)
- exact duplicate hook count: 1 (`ไม่รู้จะเริ่มตรงไหน ลองเริ่มจากโจทย์เดียว`)
- exact duplicate CTA pattern count: 3 repeated CTA strings, each repeated twice
- competition positioning: training/preparation only
- unsupported official/exam/endorsement/guaranteed-result claims observed: 0
- unsupported price/discount/deadline/stock/review/award/testimonial claims observed: 0
- deterministic gate: PASS
- result: PASS_WITH_WARNING

## TC-007 Observations
- input SKU: `INVALID-SKU`
- expected behavior: fail-safe rejection, zero rows
- observed `VALIDATION_ERROR`: invalid SKU not found in approved SKU source of truth
- row_count_actual: 0
- fabricated replacement SKU observed: 0
- campaign rows emitted: 0
- templates used: 0
- prompt assembly performed: no
- deterministic gate: PASS
- result: PASS

## TC-008 Observations
- input SKU: `BK-EL-MIX-DEVIL-01`
- row_count_actual: 20
- unique_ROW_ID_count: 20
- stable CAMPAIGN_ID: `CMP-BK-EL-MIX-DEVIL-01-20260823`
- global SEQUENCE: 1..20 continuous
- field count: 27 fields per data row
- controlled machine-token errors: 0
- controlled machine-token outer whitespace observed: 0
- IMAGE_PROMPT blank: yes
- template mappings: PASS
- internal difficulty: DEVIL
- customer-facing difficulty: GRANDMASTER
- grade/audience fit: ประถมต้น with ready/high-challenge positioning
- beginner/easy mismatch observed: 0
- Standard SKU composition handling: generic 6x6 mixed Sudoku only; no named variant membership or per-type counts invented
- approved product facts used: 500 puzzles, answer key, printable PDF
- unsupported price/discount/deadline/stock/review/award/endorsement claims observed: 0
- exact duplicate hook count: 0
- exact duplicate CTA count: 0
- warning: empty code fence before TSV
- warning: row 14 includes customer-facing wording `ในข้อความการตลาด`, a minor COPY-META-001 recurrence
- deterministic gate: PASS
- result: PASS_WITH_WARNING

## Acceptance Defects

### MACHINE-TOKEN-002 — Controlled token from wrong taxonomy column
- Status: **RESOLVED / REGRESSION PASSED on v1.7**.
- Initial occurrence: TC-006 v1.6 row 31 `OBJECTIVE=PARENT_TEACHER_INSIGHT`.
- `PARENT_TEACHER_INSIGHT` is valid only as CONTENT_PILLAR; it is not valid as OBJECTIVE.
- v1.7 mitigation: instructions require column-specific token-set validation and explicitly forbid using a token from another controlled column.
- TC-006 v1.7 rerun emits row 31 as `OBJECTIVE=BUILD_TRUST` and `CONTENT_PILLAR=PARENT_TEACHER_INSIGHT`.

### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.6 / MONITOR**.
- No outer-whitespace recurrence observed in TC-008; keep monitoring.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-008 / NON-BLOCKING by itself**.
- Empty code fences continue to appear before TSV chunks despite documented rendering rule.
- Must be resolved/regression-tested before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.
- Continue checking large batches and machine-field correctness.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.
- TC-008 row 14 includes the phrase `ในข้อความการตลาด` in customer-facing caption copy.
- This is not a product-truth failure but should be avoided in future outputs.

### COPY-DUP-001 — Minor exact repeated hook/CTA strings in large batch
- Status: **OPEN / NON-BLOCKING WARNING / MONITOR**.
- TC-006 v1.7 rerun has 1 exact duplicate hook pair and 3 repeated CTA strings in 60 rows.
- Does not block TC-006 because overall diversity gates passed, but future large-batch tests should reduce exact reuse.

## Instruction Change Triggered by TC-006
SYSTEM_INSTRUCTION_VERSION advanced from 1.6 to **1.7** before the rerun. The change preserves the ultra-compact Builder-ready format and adds explicit column-specific controlled-token validation. Row schema, taxonomy, product truth, and prompt-template versions remain unchanged.

## Instruction Authoring Dry-Run Policy
For future GPT instruction edits, maintainers must mentally simulate affected acceptance behavior before committing. The dry-run loop must focus on actual emitted rows and deterministic gates, not only wording. Iterate until expected pass or blocker; do not exceed 1,000 internal iterations. This simulation is only preflight and does not replace the required live GPT Builder rerun, deterministic validation, and semantic/human review.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
Execute **TC-009** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the synchronized v1.7 candidate. Preserve raw response, verify Advanced override handling (`TONE=trustworthy; CTA_STYLE=soft`) and conversion-streak behavior, then write the result back to this SSOT before advancing.
