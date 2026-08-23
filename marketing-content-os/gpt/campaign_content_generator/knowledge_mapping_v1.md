# BiiigBee Campaign Content Generator v1.0-rc1 — Knowledge Mapping

## Objective
Map GPT knowledge sources to clear ownership, precedence, prompt resolution and provenance rules without duplicating product truth inside system instructions.

## Tier 1 — Product Truth
From `marketing-plan/sku/`:
- `sku_source_of_truth.md`
- `sku_marketing_plan_matrix.csv`

Owns valid SKU, grade band, internal/customer-facing difficulty, audience, purpose, positioning, offer/priority, claim restrictions and approved fixed product facts.

## Tier 2 — Marketing Strategy
From `marketing-plan/strategy/`:
- marketing strategy overview
- channel/campaign strategy
- launch plan

Owns portfolio strategy, buyer/user distinctions, channel intent, campaign defaults, launch sequencing and value-first balance.

## Tier 3 — Creative / Measurement
From `marketing-plan/creative/` and `marketing-plan/measurement/`:
- creative asset system
- asset format spec
- KPI framework

Owns visual communication constraints, format rules and KPI vocabulary.

## Tier 4 — Content OS Contracts
Load approved Content OS contracts including:
- input/output contract
- system instruction / quality gates
- shared marketing brain contract
- controlled vocabulary
- prompt lookup contract
- version manifest contract
- TSV serialization contract
- large-batch protocol
- deterministic validator spec
- acceptance test plan

## Tier 5 — Schemas / Registries / Prompt Library
Load:
- `schemas/content_row_schema.tsv`
- `schemas/sku_lookup_schema.tsv`
- `schemas/controlled_vocabulary_v1.tsv`
- `templates/prompt_template_registry_v1.tsv`
- `templates/image_prompt_template_v1.txt`
- `templates/google_sheets_formula_notes.md`

## Tier 6 — Explicit Manifest
Load `knowledge_manifest_v1.yaml` so the GPT/test run has explicit CONTENT_OS, schema, taxonomy, prompt-template and Marketing Plan reference values. Never infer Git commit SHA from uploaded file content.

## Prompt Resolution
Final prompt assembly uses:
`Content Row + SKU Lookup + Approved Template`.

Product-owned placeholders are resolved from SKU data, not duplicated into every content row.

## Conflict Resolution
1. `marketing-plan/sku/sku_source_of_truth.md`
2. approved structured SKU data
3. approved Marketing Plan docs
4. Content OS contracts/defaults
5. safe user override
6. model assumption

If Tier 1 conflicts internally, treat it as a blocking source-data error. Do not silently choose a value.

## Version Traceability
Each acceptance/production run records manifest values plus test/run status. When product truth changes, update Marketing Plan first and rebuild the knowledge manifest/bundle.
