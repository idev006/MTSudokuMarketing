# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 pending execution against the instantiated Custom GPT candidate.

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
| TC-001..TC-008 | PENDING | General/invalid/DEVIL-display basics |
| TC-009..TC-016 | PENDING | Advanced overrides, safety, Formula, visual override |
| TC-017..TC-024 | PENDING | audience fit, missing inputs, invalid template, Tier-1 conflict |
| TC-025..TC-032 | PENDING | diversity, TSV escaping, large batches, AUTO, taxonomy, lookup, manifest |

## Execution Method
For each GPT answer:
1. Save raw GPT response as Markdown/text evidence.
2. Extract logical TSV with `tools/extract_tsv_from_markdown.py`.
3. Run `tools/validate_campaign_output.py` with the expected row count and canonical lookup/taxonomy/template files.
4. For N>=20, run `tools/audit_campaign_batch.py` and record metrics from actual rows.
5. Apply `acceptance_execution_rubric_v1.md` for semantic/human scoring and claim/product-truth review.
6. Record PASS / PASS_WITH_WARNING / FAIL plus evidence path.

## Release Rule
Do not freeze the GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no hard failures. GPT #2 remains HOLD until this gate is complete.
