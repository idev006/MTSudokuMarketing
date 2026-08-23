# BiiigBee Campaign Content Generator v1.0 — GPT Builder Configuration

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
Use the complete contents of:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

Do not manually duplicate SKU-specific facts inside GPT Instructions.

## Recommended Knowledge Upload Set
1. `marketing-plan/sku/sku_source_of_truth.md`
2. `marketing-plan/sku/sku_marketing_plan_matrix.csv`
3. `marketing-plan/strategy/marketing_strategy_overview.md`
4. `marketing-plan/strategy/channel_campaign_strategy.md`
5. `marketing-plan/strategy/launch_plan.md`
6. `marketing-plan/creative/creative_asset_system.md`
7. `marketing-plan/creative/asset_format_spec.md`
8. `marketing-plan/measurement/kpi_framework.md`
9. `marketing-content-os/docs/12_input_output_contract.md`
10. `marketing-content-os/docs/13_system_instruction_quality_gates.md`
11. `marketing-content-os/docs/14_shared_marketing_brain_contract.md`
12. `marketing-content-os/schemas/content_row_schema.tsv`
13. `marketing-content-os/templates/image_prompt_template_v1.txt`
14. `marketing-content-os/templates/google_sheets_formula_notes.md`

## Conversation Starters
Use the four starters in `conversation_starters_v1.md`.

## Capabilities
### Required for v1
- Knowledge/file retrieval from uploaded approved files
- Structured text generation
- TSV-compatible output

### Optional / Not Required for Initial v1
- Web browsing
- Image generation
- external Actions/API integrations
- scheduling/publishing tools

Reason: v1 should first prove deterministic campaign generation against fixed knowledge and acceptance tests. External actions add variability and should be introduced only after core acceptance passes.

## Default Operating Mode
`GENERAL`

## Default IMAGE_PROMPT_MODE
`FORMULA`

## Default Output
Three-section text package:
1. CONTENT ROWS (TSV)
2. USED IMAGE PROMPT TEMPLATES
3. PROMPT ASSEMBLY GUIDANCE

## Production Status
Initial GPT build status must be labeled:
**Candidate / Acceptance Testing Required**

Do not label Production v1.0 until the acceptance corpus passes all hard gates.

## Release Naming
- Candidate: `BiiigBee Campaign Content Generator v1.0-rc1`
- Production after PASS: `BiiigBee Campaign Content Generator v1.0`
