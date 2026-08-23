# BiiigBee Campaign Content Generator v1.0 — Knowledge Mapping

## Objective
Map GPT knowledge files to clear ownership and precedence so product truth is not duplicated inside GPT instructions.

## Required Knowledge Sources

### Tier 1 — Product Truth
Load from `marketing-plan/sku/`:
- `sku_source_of_truth.md`
- `sku_marketing_plan_matrix.csv`

Use for:
- valid SKU
- grade band
- internal difficulty
- customer-facing difficulty label
- target audience
- purpose / job-to-be-done
- positioning
- offer type
- launch phase/priority
- claim restrictions
- fixed product facts represented in approved plan data

### Tier 2 — Marketing Strategy
Load from `marketing-plan/strategy/`:
- `marketing_strategy_overview.md`
- `channel_campaign_strategy.md`
- `launch_plan.md`

Use for:
- portfolio strategy
- buyer/user distinctions
- channel intent
- campaign defaults
- launch sequencing
- value-first balance

### Tier 3 — Creative Rules
Load from `marketing-plan/creative/`:
- `creative_asset_system.md`
- `asset_format_spec.md`

Use for:
- visual communication rules
- product-box constraints
- social format defaults
- POD/print distinctions
- text-safe/readability principles

### Tier 4 — Measurement
Load from `marketing-plan/measurement/`:
- `kpi_framework.md`

Use for:
- KPI vocabulary
- performance feedback categories
- future campaign learning inputs

### Tier 5 — Content OS Contracts
Load from `marketing-content-os/docs/` and `marketing-content-os/schemas/`:
- `11_gpt_product_requirements.md`
- `12_input_output_contract.md`
- `13_system_instruction_quality_gates.md`
- `14_shared_marketing_brain_contract.md`
- `15_acceptance_test_plan.md`
- `schemas/content_row_schema.tsv`

Use for:
- behavior contract
- schema
- validation
- failure handling
- acceptance rules

### Tier 6 — Prompt System
Load from `marketing-content-os/templates/`:
- `image_prompt_template_v1.txt`
- `google_sheets_formula_notes.md`

Use for:
- approved prompt template IDs
- placeholder conventions
- formula-mode assembly

## Data Ownership Rule
Do not copy SKU-specific facts into `system_instructions_v1.md` except stable global rules. The GPT must resolve changing facts from knowledge sources.

## Conflict Resolution
When data conflicts, follow:
1. `marketing-plan/sku/sku_source_of_truth.md`
2. `marketing-plan/sku/sku_marketing_plan_matrix.csv`
3. approved Marketing Plan documents
4. Content OS contracts/defaults
5. user override where safe
6. model assumption

If Tier 1 conflicts internally, treat it as a source-data error and do not silently select a value.

## Minimum Knowledge Bundle for GPT Builder
For a practical v1 Custom GPT upload/knowledge set, include at minimum:
- SKU source-of-truth document
- SKU marketing matrix
- marketing strategy overview
- channel/campaign strategy
- creative asset rules/spec
- system instructions
- input/output contract
- shared-brain contract
- row schema
- prompt template library

## Version Traceability
Each production test should record:
- GPT/system-instruction version
- row-schema version
- prompt-template version
- Marketing Plan commit/reference used

This is required for reproducibility when product or marketing rules change.
