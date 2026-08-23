# BiiigBee Campaign Content Generator v1.0-rc1 — GPT Builder Configuration

## Name
**BiiigBee Campaign Content Generator**

## Short Description
สร้างแคมเปญคอนเทนต์แบบ batch จาก SKU ที่อนุมัติ พร้อมข้อความขาย ทิศทางภาพ และ prompt mapping โดยยึด Marketing Plan เป็น source of truth และมี quality gates ก่อนใช้งาน

## Intended Users
- เจ้าของแบรนด์ / ผู้ดูแลสินค้า
- Marketing staff
- Content creator / copywriter
- Social media admin
- Campaign planner

## Instructions — Builder-safe compact version
Paste the complete contents of:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

This compact file is the **canonical runtime Instructions** for GPT Builder and must remain below the 8,000-character limit. Re-check its length after every material edit.

Do NOT paste `system_instructions_full_reference_v1.md` into GPT Builder. That file is maintainer/reference documentation only.

## Exact rc1 Knowledge Upload Bundle — 17 files
Keep the deployment bundle below the Custom GPT knowledge-file limit. `runtime_reference_v1.md` is a retrieval-friendly mirror of critical taxonomy/template constants and is intentionally included to make GPT Builder retrieval more reliable.

### Product / Marketing Truth — 8 files
1. `marketing-plan/sku/sku_source_of_truth.md`
2. `marketing-plan/sku/sku_marketing_plan_matrix.csv`
3. `marketing-plan/strategy/marketing_strategy_overview.md`
4. `marketing-plan/strategy/channel_campaign_strategy.md`
5. `marketing-plan/strategy/launch_plan.md`
6. `marketing-plan/creative/creative_asset_system.md`
7. `marketing-plan/creative/asset_format_spec.md`
8. `marketing-plan/measurement/kpi_framework.md`

### Content / Prompt Data — 9 files
9. `marketing-content-os/schemas/content_row_schema.tsv`
10. `marketing-content-os/schemas/sku_lookup_v1.tsv`
11. `marketing-content-os/schemas/controlled_vocabulary_v1.tsv`
12. `marketing-content-os/templates/prompt_template_registry_v1.tsv`
13. `marketing-content-os/templates/image_prompt_template_v1.txt`
14. `marketing-content-os/templates/google_sheets_formula_notes.md`
15. `marketing-content-os/docs/17_prompt_lookup_contract.md`
16. `marketing-content-os/knowledge_manifest_v1.yaml`
17. `marketing-content-os/gpt/campaign_content_generator/runtime_reference_v1.md`

`runtime_reference_v1.md` does not replace canonical product truth. It provides approved canonical taxonomy, visual-template mappings and row order when TSV retrieval is unavailable.

## Files NOT Uploaded as rc1 Knowledge
These remain governance/developer documentation:
- `docs/12_input_output_contract.md`
- `docs/13_system_instruction_quality_gates.md`
- `docs/14_shared_marketing_brain_contract.md`
- `docs/16_controlled_vocabulary.md`
- `docs/18_version_manifest_contract.md`
- `docs/19_tsv_serialization_contract.md`
- `docs/20_large_batch_protocol.md`
- `docs/21_deterministic_validator_spec.md`
- `gpt/campaign_content_generator/system_instructions_full_reference_v1.md`
- acceptance test/rubric files
- validator source code

Do not upload `sku_lookup_schema.tsv`; use populated `sku_lookup_v1.tsv`.

## Conversation Starters
Use the four starters in `conversation_starters_v1.md`.

## Capabilities for rc1 Acceptance
Required:
- Knowledge/file retrieval
- Structured text generation
- TSV-compatible output

Disabled / not required:
- Web browsing
- Image generation
- external Actions/API integrations
- publishing/scheduling tools

## Locked Defaults
- Default mode: `GENERAL`
- `PLATFORM=AUTO` resolves to one canonical primary platform
- multi-platform requires Advanced Mode `PLATFORM_MIX`
- `IMAGE_PROMPT_MODE=FORMULA` only
- N>20 uses max-20-row chunks with global sequence

## Default Output
Metadata header plus:
1. CONTENT ROWS (TSV)
2. USED IMAGE PROMPT TEMPLATES
3. PROMPT ASSEMBLY GUIDANCE

## Production Status
**Candidate / Acceptance Testing Required**

Do not label Production v1.0 until independent deterministic validation and semantic acceptance tests pass all hard gates.

## Release Naming
- Candidate: `BiiigBee Campaign Content Generator v1.0-rc1`
- Production after PASS: `BiiigBee Campaign Content Generator v1.0`
