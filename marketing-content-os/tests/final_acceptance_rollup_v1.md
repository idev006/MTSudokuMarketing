# Campaign Content Generator — Final Acceptance Rollup v1

Status date: 2026-08-24

## Scope
This rollup summarizes GPT #1 `BiiigBee Campaign Content Generator` acceptance execution for TC-001..TC-032 under Marketing Content OS `1.0-rc1`.

This document is a project SSOT rollup. Raw/review evidence remains in `marketing-content-os/tests/evidence/` and the rolling status remains in `marketing-content-os/tests/acceptance_execution_status_v1.md`.

## Executive Result
TC-001..TC-032 have been executed and recorded.

Result: **ACCEPTANCE EXECUTION COMPLETE WITH WARNINGS**.

The 27-field campaign row contract passed across the acceptance corpus, including N=1, N=5, N=10, N=20, N=30, and N=60 cases; invalid/missing input cases; unsafe optional overrides; formula-mode prompt handling; large-batch chunking; controlled vocabulary; prompt-template mapping; SKU lookup prompt assembly; and manifest requirements.

## Release Position
GPT #1 is **not Production v1.0 yet**.

The candidate should move through a v1.12 regression pass before production release because `OUTPUT-FMT-001` reproduced through TC-032. The row contract is stable enough for GPT #2 candidate preparation, but production freeze should wait for final format cleanup/regression.

## Row Contract Status
The 27-field row schema is stable as the GPT #1 to GPT #2 handoff contract:

`ROW_ID, SKU, CAMPAIGN_ID, SEQUENCE, PLATFORM, AUDIENCE, OBJECTIVE, FUNNEL_STAGE, CONTENT_PILLAR, MARKETING_ANGLE, CAMPAIGN_ROLE, HOOK, HEADLINE, CAPTION, CTA, HASHTAGS, VISUAL_TYPE, VISUAL_SUBJECT, VISUAL_SCENE, VISUAL_EMOTION, PRODUCT_PLACEMENT, TEXT_OVERLAY, TEXT_SAFE_ZONE, ASPECT_RATIO, IMAGE_SIZE, PROMPT_TEMPLATE_ID, IMAGE_PROMPT`

`IMAGE_PROMPT` remains blank in rc1 Formula Mode. Final image prompts are assembled later from content row + SKU lookup + prompt template registry.

## Acceptance Summary by Range
| Range | Status | Notes |
|---|---|---|
| TC-001..TC-008 | COMPLETE | Core generation, invalid SKU, internal DEVIL/GRANDMASTER handling passed after early fixes. |
| TC-009..TC-016 | COMPLETE | Overrides, unsafe optional override continuation, platform adaptation, formula mode, visual override passed after v1.8/v1.9 fixes. |
| TC-017..TC-024 | COMPLETE | Positioning, missing input isolation, forced-template override, and Tier-1 conflict handling passed after v1.10/v1.11 fixes. |
| TC-025..TC-032 | COMPLETE | Visual diversity, TSV serialization, large batch, AUTO platform, campaign duration, controlled vocab, SKU lookup prompt assembly, and manifest handling passed with warning. |

## Blocking Defects Resolved During Acceptance
| Defect | Status | Resolution |
|---|---|---|
| MACHINE-TOKEN-001 | RESOLVED / MONITOR | Controlled-field whitespace fixed and regression passed on v1.9. |
| MACHINE-TOKEN-002 | RESOLVED / MONITOR | Wrong taxonomy-column token fixed and regression passed on v1.7. |
| OVERRIDE-SAFETY-001 | RESOLVED | Unsafe optional override now rejected while valid base generation continues; regression passed on v1.8. |
| MISSING-INPUT-001 | RESOLVED / MONITOR | Missing SKU no longer carries forward prior context; regression passed on v1.10. |
| TEMPLATE-OVERRIDE-001 | RESOLVED / MONITOR | Unknown forced template rejected while valid generation continues; regression passed on v1.11. |

## Remaining Warnings / Cleanup Items
| Defect | Status | Action |
|---|---|---|
| OUTPUT-FMT-001 | OPEN / RELEASE-BLOCKING CLEANUP | Empty Markdown code fence reproduced through TC-032. Patch v1.12 adds a no-empty-fence rule and requires regression. |
| ASPECT-RATIO-001 | OPEN / NON-BLOCKING WARNING | Product-box aspect ratio convention inconsistency should be normalized or documented before production. |
| COPY-META-001 | OPEN / NON-BLOCKING WARNING | Continue monitoring for internal governance language leaking into customer copy. |
| COPY-DUP-001 | OPEN / NON-BLOCKING WARNING | Continue monitoring repeated hooks/CTAs in large batches. |
| SELF-CHECK-001 | MITIGATED / MONITOR | Keep deterministic validation as the source of truth; do not rely on GPT self-check alone. |

## v1.12 Patch Decision
Patch v1.12 is approved as a format-only candidate cleanup. It does not alter product truth, row schema, controlled vocabulary, SKU lookup behavior, or template mappings.

v1.12 specifically strengthens the response-format contract:
- no generic code fences;
- no placeholder fences;
- no empty code blocks;
- exactly one fenced `tsv` block per part;
- every TSV fence must contain the canonical header and at least one data row;
- final scan must remove/regenerate any empty-code-block pattern before answering.

## Required v1.12 Regression
Run a focused live GPT Builder rerun after syncing v1.12:

1. **FMT-R001 / TC-001-style small batch**
```text
SKU: BK-EL-MIX-EASY-01
NUMBER_OF_ROWS: 1
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```
Expected: 1 row, no empty fence, exactly one TSV block.

2. **FMT-R002 / TC-027-style large batch**
```text
SKU: BK-US-MIX-EXPERT-01
NUMBER_OF_ROWS: 60
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
LARGE_BATCH_PROTOCOL
```
Expected: 60 rows, 3 parts, no empty fence before any part, one `tsv` block per part.

3. **FMT-R003 / TC-032-style manifest**
```text
SKU: BK-UP-MIX-MEDIUM-01
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
KNOWLEDGE_MANIFEST_REQUIRED
```
Expected: manifest metadata preserved, 10 rows, no empty fence.

## GPT #2 Readiness
GPT #2 may proceed to candidate preparation after v1.12 is synced and focused format regression passes.

GPT #2 must use the 27-field GPT #1 row as its input contract and must not change locked strategy or product truth fields.

## Production Gate
Do not label GPT #1 as Production v1.0 until:
- v1.12 regression passes;
- `OUTPUT-FMT-001` is closed or explicitly accepted with a deterministic post-processor mitigation;
- the rolling acceptance status is consolidated;
- GPT #1 row contract is formally frozen for downstream GPT #2 acceptance.
