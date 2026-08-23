# BiiigBee Marketing Content OS — Design & Build Workspace

สถานะ: **Production Readiness Hardening Complete — Ready for GPT Builder Candidate + Acceptance Run**  
แบรนด์: **BiiigBee Easy Maths**

โฟลเดอร์นี้เก็บระบบออกแบบ ข้อกำหนด implementation package และ production-readiness contracts สำหรับ Marketing Content OS ซึ่งเปลี่ยน Marketing Plan / SKU source of truth ให้เป็น campaign content แบบ batch ที่ต่อเนื่อง ตรวจสอบได้ และพร้อมเข้าสู่ acceptance testing จริง

## System Boundary
- **Marketing Plan = Truth** — SKU, product facts, target, purpose, positioning, channels, claim restrictions
- **Marketing Content OS = Execution** — campaign sequence, content rows, copy variation, visual parameters, template selection, serialization, chunking, validation

## GPT Architecture
1. **BiiigBee Campaign Content Generator v1.0-rc1** — next action: create GPT Builder candidate and run acceptance corpus
2. **BiiigBee Visual Prompt Refiner** — build only after Generator hard gates and row contract stabilize

## v1 Locked Decisions
- General Mode minimum input = SKU + NUMBER_OF_ROWS
- `PLATFORM=AUTO` resolves to one primary platform
- Advanced Mode uses same engine + safe overrides
- `IMAGE_PROMPT_MODE=FORMULA` only in v1
- exact 27-field content-row schema remains unchanged
- controlled vocabulary for machine-meaningful fields
- 10 approved image-prompt template families
- final prompt = Content Row + SKU Lookup + Approved Template
- explicit knowledge/version manifest
- one physical TSV line per content row
- N>20 uses globally continuous chunks of max 20 rows
- GPT self-check is not sufficient for production; independent deterministic validation is required
- human review before publish

## Core Production-Readiness Documents
- `docs/16_controlled_vocabulary.md`
- `docs/17_prompt_lookup_contract.md`
- `docs/18_version_manifest_contract.md`
- `docs/19_tsv_serialization_contract.md`
- `docs/20_large_batch_protocol.md`
- `docs/21_deterministic_validator_spec.md`

## Generator Implementation
- `gpt/campaign_content_generator/system_instructions_v1.md`
- `gpt/campaign_content_generator/gpt_builder_config_v1.md`
- `gpt/campaign_content_generator/conversation_starters_v1.md`
- `gpt/campaign_content_generator/knowledge_mapping_v1.md`
- `gpt/campaign_content_generator/interaction_flow_v1.md`

## Schemas / Prompt Infrastructure
- `schemas/content_row_schema.tsv`
- `schemas/sku_lookup_schema.tsv`
- `schemas/controlled_vocabulary_v1.tsv`
- `templates/prompt_template_registry_v1.tsv`
- `templates/image_prompt_template_v1.txt`
- `templates/google_sheets_formula_notes.md`
- `knowledge_manifest_v1.yaml`

## Acceptance
- `tests/campaign_content_generator_acceptance_corpus_v1.tsv` — TC-001..TC-032
- `tests/acceptance_execution_rubric_v1.md`
- `docs/15_acceptance_test_plan.md`

## Current Decision
**Architecture is frozen for the v1 candidate. Ready to create `BiiigBee Campaign Content Generator v1.0-rc1` in GPT Builder and execute acceptance testing.**

Do not label Production v1.0 until independent deterministic hard gates and semantic/human review pass.
