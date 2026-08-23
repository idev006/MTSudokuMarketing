# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN PROGRESS** on the synchronized SYSTEM_INSTRUCTION_VERSION 1.3 candidate.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | IN_PROGRESS | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 rerun PASS_WITH_WARNING; TC-004 PASS_WITH_WARNING; TC-005 next |
| TC-009..TC-016 | PENDING | Advanced overrides, safety, Formula, visual override |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict |
| TC-025..TC-032 | PENDING | diversity, TSV escaping, large batches, AUTO, taxonomy, lookup, manifest |

## Execution Method
For each GPT answer:
1. Save durable evidence.
2. Record test ID, candidate/instruction version, execution date, and evidence path.
3. Extract logical TSV when rows are expected.
4. Run deterministic validation against canonical lookup/taxonomy/template contracts.
5. For N>=20, run batch audit metrics from actual rows.
6. Apply semantic/human rubric.
7. Record PASS / PASS_WITH_WARNING / FAIL plus evidence and key metrics.
8. On FAIL, update governing documents/config/code first, rerun affected tests, and record regression evidence before advancing.

## Per-Test Evidence Record
| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Deterministic/Structural Gate | Semantic Score | Evidence | Notes |
|---|---|---|---:|---|---:|---|---|
| TC-001 | PASS_WITH_WARNING | 1.2 | 1 | PASS | 43/45 | `tests/evidence/TC-001_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-002 | PASS_WITH_WARNING | 1.2 | 5 | PASS | 44/45 | `tests/evidence/TC-002_2026-08-23_raw.md` | Hard gates pass; OUTPUT-FMT-001 recurred. |
| TC-003 initial | FAIL | 1.2 | 20 | FAIL | not release-scored | `tests/evidence/TC-003_2026-08-23_review.md` | Row 4 OBJECTIVE had leading whitespace; MACHINE-TOKEN-001 opened. |
| TC-003 rerun | PASS_WITH_WARNING | 1.3 | 20 | PASS | 44/45 | `tests/evidence/TC-003_2026-08-23_rerun_v1.3_review.md` | MACHINE-TOKEN-001 resolved; OUTPUT-FMT-001 still reproduced. |
| TC-004 | PASS_WITH_WARNING | 1.3 | 30 | PASS | 42/45 | `tests/evidence/TC-004_2026-08-23_raw.md` | Correct 20+10 chunking, stable CAMPAIGN_ID, global SEQUENCE 1..30, 30 unique ROW_ID, 27 fields per row, blank IMAGE_PROMPT, safe 9x9 mixed-Sudoku grounding, no fabricated facts. OUTPUT-FMT-001 reproduced in both parts. Row 7 exposes internal governance/meta-language in customer-facing copy; non-blocking but lowers copy quality/human usability. |

## TC-004 Batch Audit
- row_count_actual: 30
- chunking: 20 + 10
- unique_row_id_count: 30
- sequence_min/max: 1/30 continuous globally
- stable CAMPAIGN_ID: yes (`CMP-BK-US-MIX-EXPERT-01-20260823`)
- direct_sale_max_consecutive: 1
- top_angle_share: 13.33% (4/30; tie: CHALLENGE_MASTERY, TEACHER_UTILITY, PRINTABLE_CONVENIENCE)
- top_visual_type_share: 13.33% (4/30; tie: PUZZLE_CHALLENGE, TEACHER_CLASSROOM, BENEFIT)
- IMAGE_PROMPT blank: 30/30
- unsupported/fabricated claim count observed: 0
- Standard composition grounding: `9x9 mixed Sudoku` only; no named-variant composition/count assertions

## TC-004 Diagnostic Score
- Product Truth Accuracy: 5/5
- Audience/Difficulty Fit: 5/5
- Campaign Coherence: 5/5
- Copy Quality: 4/5 (row 7 uses internal policy/meta-language rather than customer-facing marketing language)
- Diversity: 5/5
- Visual Direction Quality: 5/5
- Claim Safety: 5/5
- Schema/Determinism: 5/5
- Human Usability: 3/5 (empty code fences recur in both chunks; one row exposes internal governance wording)
- Total: 42/45; average 4.67/5

## Acceptance Defects
### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.3**.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: **OPEN / REPRODUCED THROUGH TC-004 / NON-BLOCKING by itself**.
- TC-004 reproduces the empty fence in both Part 1 and Part 2.
- Closure rule: synchronized regression must show no empty fence before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: **MITIGATED / MONITOR**.
- No unverified statistical self-summary or post-hoc machine-field correction observed in TC-004.

### COPY-META-001 — Internal governance language exposed in marketing copy
- Status: **OPEN / NON-BLOCKING / FIRST OBSERVED TC-004 ROW 7**.
- Example pattern: customer-facing hook/caption explains that the system must not claim unapproved variant composition.
- Product truth remains correct, but this reduces commercial polish and exposes internal policy language.
- Monitor recurrence; if repeated, add an instruction-level rule that internal grounding/policy rationale must stay outside customer-facing row copy.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence. GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
Execute **TC-005** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the same synchronized v1.3 candidate. Preserve raw response, validate according to the corpus expectation, and write the result back to this SSOT before advancing.