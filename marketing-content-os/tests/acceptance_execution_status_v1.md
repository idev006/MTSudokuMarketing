# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 is **IN PROGRESS**. TC-003 hard failure was corrected and the v1.3 regression rerun passed deterministic/batch gates with a non-blocking rendering warning.

Before each acceptance run, verify the live GPT candidate remains synchronized with the latest documented Instructions, manifest, Knowledge bundle, and acceptance-time capabilities.

## Smoke Evidence
- Smoke #1 Standard SKU / N=1: PASS
- Smoke #2 Competition SKU / N=5: PASS
- Smoke #3 Invalid SKU: PASS
- Smoke #4 Unsupported promotion/endorsement override: PASS
- Smoke #5 N=30 chunking: PASS_WITH_MINOR_WARNING

## Full Acceptance Status
| Test range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | IN_PROGRESS | TC-001 PASS_WITH_WARNING; TC-002 PASS_WITH_WARNING; TC-003 v1.3 rerun PASS_WITH_WARNING; TC-004 next |
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
| TC-003 initial | FAIL | 1.2 | 20 | FAIL | not release-scored | `tests/evidence/TC-003_2026-08-23_review.md` | Row 4 OBJECTIVE had leading whitespace; MACHINE-TOKEN-001 opened. |
| TC-003 rerun | PASS_WITH_WARNING | 1.3 | 20 | PASS | 44/45 | `tests/evidence/TC-003_2026-08-23_rerun_v1.3_review.md` | Exact canonical controlled tokens, 20/20 rows, batch diversity within limits, no unsafe/fabricated claims. OUTPUT-FMT-001 still reproduced. |

## TC-003 v1.3 Batch Audit
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
- row 4 OBJECTIVE: exact `CREATE_ENGAGEMENT`
- IMAGE_PROMPT blank for all rows: yes

## TC-003 v1.3 Diagnostic Score
- Product Truth Accuracy: 5/5
- Audience/Difficulty Fit: 5/5
- Campaign Coherence: 5/5
- Copy Quality: 5/5
- Diversity: 5/5
- Visual Direction Quality: 5/5
- Claim Safety: 5/5
- Schema/Determinism: 5/5
- Human Usability: 4/5 (empty-code-fence presentation defect)
- Total: 44/45; average 4.89/5

## Acceptance Defects
### MACHINE-TOKEN-001 — Controlled field emitted with outer whitespace
- Status: **RESOLVED / REGRESSION PASSED on v1.3**.
- v1.3 rerun emits exact canonical `CREATE_ENGAGEMENT` and no post-hoc correction is needed.

### OUTPUT-FMT-001 — Empty Markdown code fence
- Status: OPEN / REPRODUCED THROUGH TC-003 v1.3 / NON-BLOCKING by itself.
- Impact: presentation clutter and parser friction.
- Closure rule: later synchronized regression run must show no empty fence before Production v1.0.

### SELF-CHECK-001 — Self-check/post-output correction weakness
- Status: MITIGATED / MONITOR.
- v1.3 TC-003 rerun did not use post-hoc prose correction of a machine field. Continue monitoring on later large-batch tests.

## Release Rule
Do not freeze GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no unresolved hard failures and complete evidence.

GPT #2 remains HOLD until GPT #1 acceptance/freeze is complete and GPT #2's own acceptance corpus passes.

## Immediate Next Action
Execute **TC-004** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the synchronized v1.3 candidate. Preserve raw response, validate all 30 rows across chunks, verify stable CAMPAIGN_ID/global SEQUENCE/full-batch diversity/product truth, and write the result back to this SSOT before advancing to TC-005.
