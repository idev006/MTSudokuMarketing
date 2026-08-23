# Campaign Content Generator v1.0-rc1 — Acceptance Execution Status

## Governance
This execution record is governed by `marketing-content-os/docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`.

GitHub project documents are the operational SSOT. Chat, model memory, temporary notes, and unsynchronized GPT Builder settings are not authoritative by themselves. Every material acceptance result, blocker, mitigation, version change, and release decision must be recorded in the repository.

## Current Gate
Smoke gate passed. Full acceptance TC-001..TC-032 pending execution against the instantiated Custom GPT candidate using the latest documented Instructions/Knowledge versions.

Before TC-001 begins, verify the live GPT candidate has:
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
| TC-001..TC-008 | PENDING | General/invalid/DEVIL-display basics |
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

## Per-Test Evidence Record Template
Use this template as tests are executed:

| TEST_ID | RESULT | GPT/Instruction Version | Row Count | Deterministic Validator | Semantic Score | Evidence | Notes |
|---|---|---|---:|---|---:|---|---|
| TC-001 | PENDING | 1.2 |  |  |  |  |  |

## Release Rule
Do not freeze the GPT #1 row contract or release Production v1.0 until TC-001..TC-032 satisfy the acceptance rubric with no hard failures and the documented evidence is complete.

GPT #2 remains HOLD until this gate is complete. Its handoff contract may be prepared/documented, but it must not be promoted to production before GPT #1 acceptance/freeze and GPT #2's own acceptance corpus pass.

## Immediate Next Action
Execute **TC-001** from `campaign_content_generator_acceptance_corpus_v1.tsv` against the synchronized GPT #1 candidate, preserve the raw response, validate it, score it, and write the result back to this SSOT record before advancing to TC-002.
