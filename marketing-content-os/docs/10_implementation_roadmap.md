# 10 — Implementation Roadmap

## Phase 1 — Finalize v1 Contracts — COMPLETE
Locked product requirements, system boundary, modes, row schema, output contract, integrity/quality gates, Shared Marketing Brain and acceptance philosophy.

## Phase 2 — Build Campaign Content Generator Implementation Package — COMPLETE
Created production instructions, GPT Builder config, conversation starters, knowledge mapping, interaction flows and initial acceptance assets.

## Phase 3 — Production Readiness Hardening — COMPLETE
Completed:
- 10 approved image-prompt template families + registry
- canonical controlled vocabulary / machine-readable taxonomy
- v1 `IMAGE_PROMPT_MODE=FORMULA` lock
- SKU Lookup / placeholder resolution contract
- explicit knowledge/version manifest
- TSV serialization/escaping contract
- large-batch chunking protocol
- expanded acceptance corpus TC-001..TC-032
- independent deterministic validator specification

Architecture for the v1 candidate is now frozen unless acceptance testing reveals a defect.

## Phase 4 — Create GPT Builder Candidate — NEXT
Build **BiiigBee Campaign Content Generator v1.0-rc1** using the approved system instructions, knowledge bundle, schemas, registries, prompt library and manifest.

Do not enable unnecessary web/image/actions integrations for the initial acceptance candidate.

## Phase 5 — Acceptance Testing — NEXT
Execute TC-001..TC-032 across Standard + Competition SKUs, small/medium/large batches, invalid/missing inputs, unsafe overrides, controlled vocabulary, prompt lookup, TSV serialization, provenance and chunking.

Validation requires:
- independent deterministic hard-gate checks
- semantic/human review

## Phase 6 — Fix / Re-test Loop
Classify failures by owning source: Marketing Plan data, instruction, schema/taxonomy, prompt template, serialization/chunking, or semantic generation quality. Fix the source, not individual output rows, then rerun affected tests + regression set.

## Phase 7 — Google Sheets Prompt Assembly Implementation
Implement SKU lookup + approved template lookup + placeholder substitution + unresolved-placeholder validation for Formula Mode.

## Phase 8 — Build Visual Prompt Refiner
Only after Generator row contract and hard gates are stable. The specialist may refine creative execution but may not redefine product truth, audience, objective, campaign role, offer or claim policy.

## Phase 9 — Pilot Campaign
Run at least one representative ~30-row campaign through human review and prompt assembly.

## Phase 10 — Portfolio Scale
Expand production use across all 24 SKUs while retaining Marketing Plan as truth and Marketing Content OS as execution.

## Release Rule
**Contracts → Generator Implementation → Production Hardening → GPT Candidate → Acceptance → Fix/Re-test → Prompt Assembly → Visual Refiner → Pilot → 24-SKU Scale**

Production v1.0 requires all hard gates to pass. Before that, use the RC label.
