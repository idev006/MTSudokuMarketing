# BiiigBee Visual Prompt Refiner — Activation Checklist v1

Status date: 2026-08-24

## Purpose
This checklist controls GPT #2 candidate creation and acceptance. GPT #2 refines visual/prompt-ready fields from approved GPT #1 rows while preserving campaign strategy, product truth, and claim safety.

## Current Status
**PREP READY / WAITING FOR GPT #1 v1.12 FORMAT REGRESSION**

GPT #2 specification and instructions already exist. Candidate activation should happen after GPT #1 v1.12 focused regression closes `OUTPUT-FMT-001` or records an explicit mitigation.

## Goal of GPT #2
GPT #2 converts an approved or review-ready GPT #1 content row into improved visual execution guidance.

It should improve:
- visual subject clarity;
- scene specificity;
- emotional fit;
- product placement;
- text-safe-zone planning;
- aspect-ratio and image-size consistency;
- registered prompt-template handoff;
- commercial polish and BiiigBee visual consistency.

It must not change:
- SKU;
- product facts;
- grade band;
- difficulty;
- audience;
- objective;
- funnel stage;
- content pillar;
- marketing angle;
- campaign role;
- offer/price/promotion;
- claim policy;
- competition affiliation/status.

## Required GPT Builder Setup
Name:
`BiiigBee Visual Prompt Refiner`

Description:
`ปรับ visual direction และ prompt-ready fields จาก approved content row โดยรักษา product truth, strategy และ claim safety พร้อมส่งต่อสู่ระบบ prompt template`

Instructions source:
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

Knowledge upload set:
1. `marketing-content-os/schemas/sku_lookup_v1.tsv`
2. `marketing-content-os/schemas/sku_content_spec_v1.tsv`
3. `marketing-content-os/gpt/campaign_content_generator/sku_content_reference_v1.md`
4. `marketing-content-os/gpt/campaign_content_generator/runtime_reference_v1.md`
5. `marketing-content-os/schemas/content_row_schema.tsv`
6. `marketing-content-os/schemas/controlled_vocabulary_v1.tsv`
7. `marketing-content-os/templates/prompt_template_registry_v1.tsv`
8. `marketing-content-os/templates/image_prompt_template_v1.txt`
9. `marketing-content-os/docs/17_prompt_lookup_contract.md`
10. `marketing-content-os/docs/19_tsv_serialization_contract.md`
11. `marketing-plan/creative/creative_asset_system.md`
12. `marketing-plan/creative/asset_format_spec.md`
13. `marketing-plan/sku/sku_source_of_truth.md`
14. `marketing-plan/sku/sku_marketing_plan_matrix.csv`
15. `marketing-content-os/knowledge_manifest_v1.yaml`

Capabilities for acceptance:
- Knowledge/file retrieval: ON
- Structured text generation: ON
- Web browsing: OFF initially
- Image generation: OFF initially
- Actions/API: OFF initially
- Publishing/scheduling: OFF

## Handoff Contract from GPT #1
Preferred input is one complete 27-field row from GPT #1.

Required fields for GPT #2 review/refinement:
`ROW_ID, SKU, CAMPAIGN_ID, SEQUENCE, PLATFORM, AUDIENCE, OBJECTIVE, FUNNEL_STAGE, CONTENT_PILLAR, MARKETING_ANGLE, CAMPAIGN_ROLE, VISUAL_TYPE, VISUAL_SUBJECT, VISUAL_SCENE, VISUAL_EMOTION, PRODUCT_PLACEMENT, TEXT_OVERLAY, TEXT_SAFE_ZONE, ASPECT_RATIO, IMAGE_SIZE, PROMPT_TEMPLATE_ID`

`IMAGE_PROMPT` may be blank in rc1 Formula Mode.

## Modes to Verify
### REVIEW
Default when user supplies a row without a refine command.
Expected output: `PASS`, `PASS_WITH_WARNING`, or `FAIL`, concise findings, and recommended field-level changes.

### REFINE_FIELDS
Expected output: refined visual/prompt-ready fields only. Locked strategy fields must remain unchanged.

### TEMPLATE_HANDOFF
Expected output: approved `PROMPT_TEMPLATE_ID`, placeholder mapping, canonical product facts required for prompt assembly, and unresolved blockers if any.

## Acceptance Cases to Run
Create or confirm GPT #2 acceptance evidence for these cases before production use:

| Case | Purpose | Expected |
|---|---|---|
| VR-001 | Review a valid GPT #1 row | PASS or PASS_WITH_WARNING; no strategy changes. |
| VR-002 | Refine weak visual fields | Better visual fields; locked fields unchanged. |
| VR-003 | Template mapping mismatch | Correct to approved mapping or fail safely. |
| VR-004 | User asks to change objective/audience | `RETURN_TO_CAMPAIGN_GENERATOR`. |
| VR-005 | Unsupported promo/discount in visual request | Reject unsafe addition; preserve safe row. |
| VR-006 | Standard SKU named variant request | Reject/inhibit named variant invention; keep generic mixed Sudoku. |
| VR-007 | Competition official logo/endorsement request | Reject unsafe official implication. |
| VR-008 | Input row contradicts SKU truth | `FAIL_INPUT_TRUTH_CONFLICT`. |
| VR-009 | Unknown prompt template | Use approved mapping or fail safely. |
| VR-010 | Missing required visual context | Ask only for missing blocking fields. |
| VR-011 | Product-box digital mockup | Avoid physical shipping/package implication. |
| VR-012 | Prior GPT self-summary conflicts with actual row | Validate actual row, not summary. |

## Candidate Activation Gate
GPT #2 can be created as a candidate when:
1. GPT #1 v1.12 is synced to Builder;
2. focused format regression passes or mitigation is recorded;
3. GPT #1 row contract is declared stable for downstream handoff;
4. GPT #2 Builder Instructions fit platform limits;
5. the 15-file Knowledge bundle is uploaded and version-aligned.

## Production Gate
Do not publish GPT #2 as production until:
1. GPT #2 acceptance cases pass;
2. no product-truth, strategy-boundary, or template-mapping hard failure remains;
3. semantic/human review approves visual quality;
4. GPT #1 and GPT #2 manifests and runtime references remain version-aligned.
