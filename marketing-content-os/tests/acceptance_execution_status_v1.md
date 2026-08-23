# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is in progress against the instantiated Custom GPT candidate using the latest documented Instructions/Knowledge versions.

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

Observed non-blocking defects from smoke execution:
- OUTPUT-FMT-001: empty Markdown code fence appeared before TSV blocks.
- SELF-CHECK-001: one batch self-summary misstated maximum visual-type count even though actual rows remained within the 25% gate.

Mitigation in SYSTEM_INSTRUCTION_VERSION 1.2:
- exactly one fenced `tsv` block per displayed part; no empty fences;
- batch statistics may be stated only when calculated from emitted rows; uncertain statistics must be omitted.

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | IN_PROGRESS | TC-001 completed PASS_WITH_WARNING; TC-002 next |
| TC-009..TC-016 | PENDING | Advanced overrides, safety, Formula, visual override |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict |
| TC-025..TC-032 | PENDING | diversity, TSV escaping, large batches, AUTO, taxonomy, lookup, manifest |

## Execution Method
For each GPT answer:
1. Save the raw GPT response as durable Markdown/text evidence.
2. Record the test ID, candidate/version identifiers, execution date, and evidence path.
3. Extract logical TSV with `tools/extract_tsv_from_markdown.py` when rows are expected.
4. Run `tools/validate_campaign_output.py` with the expected row count and canonical lookup/taxonomy/template files.
5. For N>=20, run `tools/audit_campaign_batch.py` and record metrics from actual rows.
6. Apply `acceptance_execution_rubric_v1.md` for semantic/human scoring and claim/product-truth review.
7. Record PASS / PASS_WITH_WARNING / FAIL plus evidence path and key metrics in this document or a linked durable acceptance record.
8. On FAIL, update governing documents/config/code first, rerun affected tests, and record regression evidence before moving the release gate.

## Per-Test Evidence Record
| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Deterministic Validator | Semantic Score | Evidence | Notes |
|---|---|---|---:|---|---:|---|---|
| TC-001 | PASS_WITH_WARNING | 1.2 | 1 | PASS | 43/45 | `tests/evidence/TC-001_2026-08-23_raw.md` | Hard gates pass. Correct approved SKU, FACEBOOK AUTO resolution, canonical taxonomy, EASY/EL audience fit, 6x6 generic mixed-Sudoku grounding, 500 puzzles + answer key truth, approved STUDENT_ACTIVITY→IMG-STUDENT-ACTIVITY-V1 mapping, and blank IMAGE_PROMPT. OUTPUT-FMT-001 recurred: an empty Markdown code fence still appeared before the TSV block despite v1.2 rendering mitigation. Non-blocking for TC-001 but remains an open regression item. |

### TC-001 Diagnostic Score
- Product Truth Accuracy: 5/5
- Audience/Difficulty Fit: 5/5
- Campaign Coherence: 5/5
- Copy Quality: 5/5
- Diversity: 4/5 (N=1; diversity is not meaningfully testable)
- Visual Direction Quality: 5/5
- Claim Safety: 5/5
- Schema/Determinism: 5/5
- Human Usability: 4/5 (empty-code-fence presentation defect)
- Total: 43/45; average 4.78/5

## Open Acceptance Defects
### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: OPEN / NON-BLOCKING for current semantic tests.
- Seen in smoke runs and reproduced in TC-001 after SYSTEM_INSTRUCTION_VERSION 1.2.
- Impact: human presentation clutter and potential parser friction; logical TSV remains extractable and the 27-field record is valid.
- Rule: do not mark this defect resolved until a later regression run demonstrates no empty fence using the live synchronized candidate.

### SELF-CHECK-001 — Unverified batch-summary statistic
- Status: MITIGATED / REGRESSION PENDING.
- No occurrence in TC-001 because N=1 has no batch-statistics summary requirement.
- Recheck on a later N>=20 acceptance case using deterministic batch audit metrics.

## Release Rule
Do not freeze the GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no hard failures and the documented evidence is complete.

GPT #2 remains HOLD until this gate is complete. Its handoff contract may be prepared/documented, but it must not be promoted to production before GPT #1 acceptance/freeze and GPT #2's own acceptance corpus pass.

## Immediate Next Action
Execute **TC-002** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the same synchronized GPT #1 candidate, preserve the raw response, validate it, score it, and write the result back to this SSOT record before advancing to TC-003.
