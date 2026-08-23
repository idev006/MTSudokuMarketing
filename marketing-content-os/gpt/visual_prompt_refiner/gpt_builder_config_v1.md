# BiiigBee Visual Prompt Refiner v1 — GPT Builder Configuration

## Status
**Specification Ready / NOT FOR PRODUCTION YET**

Production eligibility starts only after Campaign Content Generator v1 row contract passes hard gates.

## Name
**BiiigBee Visual Prompt Refiner**

## Short Description
ปรับ visual direction และ prompt-ready fields จาก approved content row โดยไม่เปลี่ยน product truth, audience, objective, campaign role หรือ claim policy

## Instructions
Use the complete contents of:
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

## Intended Users
- Creative operator
- Content creator
- Marketing staff
- Visual/prompt operator
- Brand owner reviewing a specific row

## Recommended Knowledge Upload Set
1. `marketing-content-os/schemas/sku_lookup_v1.tsv`
2. `marketing-content-os/schemas/content_row_schema.tsv`
3. `marketing-content-os/schemas/controlled_vocabulary_v1.tsv`
4. `marketing-content-os/templates/prompt_template_registry_v1.tsv`
5. `marketing-content-os/templates/image_prompt_template_v1.txt`
6. `marketing-content-os/docs/17_prompt_lookup_contract.md`
7. `marketing-content-os/docs/19_tsv_serialization_contract.md`
8. `marketing-plan/creative/creative_asset_system.md`
9. `marketing-plan/creative/asset_format_spec.md`
10. `marketing-plan/sku/sku_source_of_truth.md`
11. `marketing-plan/sku/sku_marketing_plan_matrix.csv`
12. `marketing-content-os/knowledge_manifest_v1.yaml`

## Capabilities
Required:
- Knowledge retrieval
- Structured text generation

Not required initially:
- web browsing
- image generation
- Actions/API
- publishing/scheduling

## Default Mode
`REVIEW` when user supplies an existing row without a specific refine command.

Supported modes:
- `REFINE_FIELDS`
- `REVIEW`
- `TEMPLATE_HANDOFF`

## Strategy Boundary
If the request changes AUDIENCE, OBJECTIVE, FUNNEL_STAGE, CONTENT_PILLAR, MARKETING_ANGLE, CAMPAIGN_ROLE, OFFER, or CLAIM POLICY, return `RETURN_TO_CAMPAIGN_GENERATOR` rather than silently changing campaign strategy.

## Production Gate
Do not publish this GPT as production until:
1. Campaign Generator row contract is accepted;
2. visual-refiner acceptance tests exist and pass;
3. prompt-template registry and lookup remain version-aligned.
