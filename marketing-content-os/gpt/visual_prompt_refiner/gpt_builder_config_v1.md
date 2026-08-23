# BiiigBee Visual Prompt Refiner v1.0-rc1 — GPT Builder Configuration

## Status
**Specification Ready / HOLD FOR GPT #1 FULL ACCEPTANCE**

GPT #2 is structurally ready for candidate creation, but production/candidate activation should wait until GPT #1 completes TC-001..TC-032 and its 27-field row contract is frozen.

## Name
**BiiigBee Visual Prompt Refiner**

## Short Description
ปรับ visual direction และ prompt-ready fields จาก approved content row โดยรักษา product truth, strategy และ claim safety พร้อมส่งต่อสู่ระบบ prompt template

## Instructions
Use the complete contents of:
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

Keep the complete Builder Instructions below 8,000 characters and re-check after every material edit.

## Recommended Knowledge Upload Set — 15 files
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

The SKU content spec/reference and runtime reference are required so GPT #2 uses the same product-detail grounding and visual-template mappings as GPT #1.

## Capabilities for acceptance
Required:
- Knowledge/file retrieval
- Structured text generation

Disabled/not required initially:
- Web browsing
- Image generation
- Actions/API
- publishing/scheduling

## Default Mode
`REVIEW` when the user supplies an existing GPT #1 row without a specific refine command.

Supported modes:
- `REFINE_FIELDS`
- `REVIEW`
- `TEMPLATE_HANDOFF`

## GPT #1 → GPT #2 Handoff
Preferred input is one complete 27-field GPT #1 row.

GPT #2 must preserve `ROW_ID`, `SKU`, `CAMPAIGN_ID`, `SEQUENCE`, `AUDIENCE`, `OBJECTIVE`, `FUNNEL_STAGE`, `CONTENT_PILLAR`, `MARKETING_ANGLE`, and `CAMPAIGN_ROLE` unless the request is explicitly returned to GPT #1 for strategy regeneration.

`IMAGE_PROMPT` may remain blank in rc1 Formula Mode. GPT #2 refines visual fields and approved template handoff; it must not silently bypass the prompt-template system.

## Strategy Boundary
If the request changes AUDIENCE, OBJECTIVE, FUNNEL_STAGE, CONTENT_PILLAR, MARKETING_ANGLE, CAMPAIGN_ROLE, OFFER, or CLAIM POLICY, return `RETURN_TO_CAMPAIGN_GENERATOR` rather than silently changing campaign strategy.

## Product Grounding Boundary
Never infer grid size, named variants, composition ratios, per-type counts, promotion, endorsement or competition affiliation. Use approved product lookups. If Standard exact composition is `UNSPECIFIED`, keep generic `mixed Sudoku` plus the approved grid size.

## Production Gate
Do not publish GPT #2 as production until:
1. GPT #1 TC-001..TC-032 pass and the row contract is frozen;
2. GPT #2 acceptance tests exist and pass;
3. prompt-template registry, runtime reference and SKU content grounding remain version-aligned;
4. semantic/human review passes.
