# BiiigBee Campaign Content Generator v1.0-rc1 — GPT Builder Configuration

## Name
**BiiigBee Campaign Content Generator**

## Short Description
สร้าง campaign content แบบ batch จาก SKU ที่อนุมัติแล้ว พร้อม copy, visual direction, prompt-template mapping และ quality gates โดยยึด Marketing Plan เป็น source of truth

## Intended Users
- เจ้าของแบรนด์ / ผู้ดูแลสินค้า
- Marketing staff
- Content creator / copywriter
- Social media admin
- Campaign planner

## Instructions
Paste the complete contents of:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

This is the canonical instruction text. Do not summarize it and do not duplicate SKU-specific facts inside Instructions.

## Exact rc1 Knowledge Upload Bundle — 16 files
Keep the deployment bundle intentionally below the Custom GPT knowledge-file limit. Behavioral rules already encoded in System Instructions must not be uploaded again merely as duplicate reference files.

### Product / Marketing Truth — 8 files
1. `marketing-plan/sku/sku_source_of_truth.md`
2. `marketing-plan/sku/sku_marketing_plan_matrix.csv`
3. `marketing-plan/strategy/marketing_strategy_overview.md`
4. `marketing-plan/strategy/channel_campaign_strategy.md`
5. `marketing-plan/strategy/launch_plan.md`
6. `marketing-plan/creative/creative_asset_system.md`
7. `marketing-plan/creative/asset_format_spec.md`
8. `marketing-plan/measurement/kpi_framework.md`

### Content / Prompt Data — 8 files
9. `marketing-content-os/schemas/content_row_schema.tsv`
10. `marketing-content-os/schemas/sku_lookup_v1.tsv`
11. `marketing-content-os/schemas/controlled_vocabulary_v1.tsv`
12. `marketing-content-os/templates/prompt_template_registry_v1.tsv`
13. `marketing-content-os/templates/image_prompt_template_v1.txt`
14. `marketing-content-os/templates/google_sheets_formula_notes.md`
15. `marketing-content-os/docs/17_prompt_lookup_contract.md`
16. `marketing-content-os/knowledge_manifest_v1.yaml`

## Files NOT Uploaded as rc1 Knowledge
The following remain governance/developer documentation in GitHub but are not part of the GPT Builder knowledge upload bundle because their runtime behavior is already encoded in the canonical System Instructions:
- `docs/12_input_output_contract.md`
- `docs/13_system_instruction_quality_gates.md`
- `docs/14_shared_marketing_brain_contract.md`
- `docs/16_controlled_vocabulary.md`
- `docs/18_version_manifest_contract.md`
- `docs/19_tsv_serialization_contract.md`
- `docs/20_large_batch_protocol.md`
- `docs/21_deterministic_validator_spec.md`
- acceptance test/rubric files
- validator source code

Do not upload `sku_lookup_schema.tsv`; it documents the shape only. Use populated `sku_lookup_v1.tsv`.

## Conversation Starters
Use the four starters in `conversation_starters_v1.md`.

## Capabilities Required for rc1
- Knowledge/file retrieval from uploaded approved files
- Structured text generation
- TSV-compatible output

## Capabilities Disabled / Not Required for rc1 Acceptance
- Web browsing
- Image generation
- external Actions/API integrations
- scheduling/publishing tools

Keep external variability low until core acceptance passes.

## Default Operating Mode
`GENERAL`

## Platform AUTO Rule
Resolve to one primary canonical platform for a campaign. Multi-platform generation is an Advanced Mode capability using `PLATFORM_MIX`.

## IMAGE_PROMPT_MODE v1
`FORMULA` only.

`PRECOMPILED` and `BOTH` are future-version options and must not be exposed as active rc1 modes.

## Default Output
Metadata header plus:
1. CONTENT ROWS (TSV; chunked at max 20 rows per part when N>20)
2. USED IMAGE PROMPT TEMPLATES
3. PROMPT ASSEMBLY GUIDANCE

## Production Status
Initial GPT build status:
**Candidate / Acceptance Testing Required**

Do not label Production v1.0 until independent deterministic validation and semantic acceptance tests pass all hard gates.

## Release Naming
- Candidate: `BiiigBee Campaign Content Generator v1.0-rc1`
- Production after PASS: `BiiigBee Campaign Content Generator v1.0`
