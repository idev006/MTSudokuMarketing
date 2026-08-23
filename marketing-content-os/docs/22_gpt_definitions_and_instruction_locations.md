# 22 — GPT Definitions and Instruction Locations

เอกสารนี้เป็นแผนที่กลางสำหรับค้นหา GPT definitions, Instructions, Builder configuration และ release checklist ของ BiiigBee Marketing Content OS

## GPT #1 — BiiigBee Campaign Content Generator
สถานะ: **v1.0-rc1 / Candidate / Acceptance Testing Required**

### Canonical Instructions
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

ไฟล์นี้คือข้อความ Instructions หลักที่ต้อง copy เข้า GPT Builder โดยตรงสำหรับ rc1 candidate

### Builder Configuration
`marketing-content-os/gpt/campaign_content_generator/gpt_builder_config_v1.md`

ประกอบด้วย:
- Name / Description
- Intended users
- exact rc1 Knowledge Upload Bundle = 16 files
- capabilities สำหรับ acceptance
- default mode
- AUTO platform behavior
- Formula-only image prompt behavior
- release naming/status

### Conversation Starters
`marketing-content-os/gpt/campaign_content_generator/conversation_starters_v1.md`

### Knowledge / Source Mapping
`marketing-content-os/gpt/campaign_content_generator/knowledge_mapping_v1.md`

### General / Advanced Interaction Flow
`marketing-content-os/gpt/campaign_content_generator/interaction_flow_v1.md`

### Pre-Creation Checklist
`marketing-content-os/gpt/PRE_CREATION_CHECKLIST_v1.md`

ใช้ checklist นี้ก่อนนำค่าไปกรอกใน GPT Builder และก่อนเริ่ม smoke test

---

## GPT #2 — BiiigBee Visual Prompt Refiner
สถานะ: **Specification Ready / NOT FOR PRODUCTION YET**

### Canonical Instructions
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

### Builder Configuration
`marketing-content-os/gpt/visual_prompt_refiner/gpt_builder_config_v1.md`

### Conversation Starters
`marketing-content-os/gpt/visual_prompt_refiner/conversation_starters_v1.md`

GPT #2 ใช้ refine visual execution จาก approved content row เท่านั้น ห้ามเปลี่ยน SKU truth, audience, objective, campaign role หรือ claim policy

---

## GPT Builder Setup Guide
`marketing-content-os/gpt/GPT_BUILDER_SETUP_GUIDE.md`

ใช้เป็น step-by-step guide ในการสร้าง Custom GPT จริง

## GPT Documentation Index
`marketing-content-os/gpt/README.md`

## Canonical SKU Lookup
`marketing-content-os/schemas/sku_lookup_v1.tsv`

มีข้อมูล lookup ของ 24 SKU สำหรับ product-owned prompt placeholders และ deterministic validation

## Canonical Machine Taxonomy
`marketing-content-os/schemas/controlled_vocabulary_v1.tsv`

ครอบคลุม FUNNEL_STAGE, CAMPAIGN_ROLE, VISUAL_TYPE, PLATFORM, OBJECTIVE, CONTENT_PILLAR และ MARKETING_ANGLE_FAMILY

## Acceptance / Validation
- `marketing-content-os/tests/campaign_content_generator_acceptance_corpus_v1.tsv`
- `marketing-content-os/tests/acceptance_execution_rubric_v1.md`
- `marketing-content-os/tools/validate_campaign_output.py`

Validator ต้องตรวจ controlled fields ทั้งหมดและนับ marketing-angle concentration จาก canonical family ก่อน `:`

## Governance
GitHub files aboveเป็น documented source สำหรับ GPT configuration. ห้าม maintain undocumented alternative Instructions โดยแก้เฉพาะใน GPT Builder. Material Builder change ต้องเริ่มจาก GitHub, version/rebuild และ retest ก่อนเสมอ
