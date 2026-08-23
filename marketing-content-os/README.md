# BiiigBee Marketing Content OS — Design & Build Workspace

สถานะ: **GPT #1 Candidate Created + Smoke Gate Passed — Full Acceptance TC-001..TC-032 Pending**  
แบรนด์: **BiiigBee Easy Maths**

โฟลเดอร์นี้เก็บระบบออกแบบ ข้อกำหนด implementation package และ production-readiness contracts สำหรับ Marketing Content OS ซึ่งเปลี่ยน Marketing Plan / SKU source of truth ให้เป็น campaign content แบบ batch ที่ต่อเนื่อง ตรวจสอบได้ และพร้อมเข้าสู่ acceptance testing จริง

## Project Governance — Mandatory
โครงการนี้เป็น **Document-Driven Project** และใช้เอกสารที่อนุมัติแล้วใน GitHub เป็น **Source of Truth (SSOT)**

กติกาหลักอยู่ที่ `docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md` และมีผลบังคับกับการพัฒนา GPT, schema, taxonomy, code, test, acceptance, release และ production workflow ทั้งหมด

Chat, model memory, GPT Builder configuration ที่ไม่ได้ sync กลับ GitHub, temporary notes และ assumptions ไม่ใช่ SSOT โดยตัวมันเอง หากมีการตัดสินใจสำคัญหรือการเปลี่ยน behavior ต้องบันทึกในเอกสารโครงการและปรับ dependent artifacts ให้ตรงกัน

## System Boundary
- **Marketing Plan = Product/Marketing Truth** — SKU, product facts, target, purpose, positioning, channels, claim restrictions
- **Marketing Content OS = Execution** — campaign sequence, content rows, copy variation, visual parameters, template selection, serialization, chunking, validation
- **GitHub Documents = Operational SSOT** — governing contracts, versions, acceptance status, change decisions and release state

## GPT Architecture
1. **BiiigBee Campaign Content Generator v1.0-rc1** — instantiated candidate exists; Smoke Tests #1..#5 passed; next gate is TC-001..TC-032 full acceptance.
2. **BiiigBee Visual Prompt Refiner** — handoff contract aligned with GPT #1 and VR-001..VR-012 acceptance corpus exists, but **HOLD / NOT FOR PRODUCTION** until GPT #1 row contract is accepted and frozen.

## Where GPTs / Instructions Live
- GPT documentation index: `gpt/README.md`
- GPT Builder setup guide: `gpt/GPT_BUILDER_SETUP_GUIDE.md`
- Central location map: `docs/22_gpt_definitions_and_instruction_locations.md`
- Campaign Generator Instructions: `gpt/campaign_content_generator/system_instructions_v1.md`
- Campaign Generator Builder Config: `gpt/campaign_content_generator/gpt_builder_config_v1.md`
- Visual Prompt Refiner Instructions: `gpt/visual_prompt_refiner/system_instructions_v1.md`
- Visual Prompt Refiner Builder Config: `gpt/visual_prompt_refiner/gpt_builder_config_v1.md`

## v1 Locked Decisions
- General Mode minimum input = SKU + NUMBER_OF_ROWS
- `PLATFORM=AUTO` resolves to one primary platform
- Advanced Mode uses same engine + safe overrides
- `IMAGE_PROMPT_MODE=FORMULA` only in v1
- exact 27-field content-row schema remains unchanged
- controlled vocabulary for machine-meaningful fields
- 10 approved image-prompt template families
- product-detail claims use canonical SKU content grounding; Standard exact composition may remain `UNSPECIFIED`
- final prompt = Content Row + SKU Lookup + Approved Template
- explicit knowledge/version manifest
- one physical TSV line per content row
- N>20 uses globally continuous chunks of max 20 rows
- GPT self-check is not sufficient for production; independent deterministic validation is required
- human review before publish

## Core Governance / Production-Readiness Documents
- `docs/00_DOCUMENT_DRIVEN_SSOT_GOVERNANCE.md`
- `docs/16_controlled_vocabulary.md`
- `docs/17_prompt_lookup_contract.md`
- `docs/18_version_manifest_contract.md`
- `docs/19_tsv_serialization_contract.md`
- `docs/20_large_batch_protocol.md`
- `docs/21_deterministic_validator_spec.md`
- `docs/22_gpt_definitions_and_instruction_locations.md`

## Schemas / Prompt Infrastructure
- `schemas/content_row_schema.tsv`
- `schemas/sku_lookup_schema.tsv` — schema only
- `schemas/sku_lookup_v1.tsv` — populated canonical 24-SKU lookup
- `schemas/sku_content_spec_v1.tsv` — grid/content-claim grounding
- `schemas/controlled_vocabulary_v1.tsv`
- `templates/prompt_template_registry_v1.tsv`
- `templates/image_prompt_template_v1.txt`
- `templates/google_sheets_formula_notes.md`
- `knowledge_manifest_v1.yaml`

## Acceptance
- `tests/campaign_content_generator_acceptance_corpus_v1.tsv` — TC-001..TC-032
- `tests/acceptance_execution_rubric_v1.md`
- `tests/acceptance_execution_status_v1.md` — live execution status/evidence index
- `tools/extract_tsv_from_markdown.py`
- `tools/validate_campaign_output.py`
- `tools/audit_campaign_batch.py`
- `docs/15_acceptance_test_plan.md`

## Current Decision / Next Gate
**Do not create new production behavior from chat alone. First keep GitHub documents current, then execute from the documented plan.**

Immediate next action:
1. ensure the instantiated GPT #1 uses the latest `system_instructions_v1.md` and latest `knowledge_manifest_v1.yaml`;
2. execute TC-001..TC-032 against that exact candidate;
3. save raw evidence, extract TSV, run deterministic validator/audit, and score semantic/human quality;
4. record every PASS / PASS_WITH_WARNING / FAIL in `tests/acceptance_execution_status_v1.md`;
5. fix failures via documented change control and rerun affected regression tests;
6. only after all GPT #1 hard gates pass, freeze the row contract and advance GPT #2.

Do not label Production v1.0 until documented deterministic hard gates and semantic/human review pass.
