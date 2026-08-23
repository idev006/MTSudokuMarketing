# 22 — GPT Definitions and Instruction Locations

เอกสารนี้เป็นแผนที่กลางสำหรับค้นหา GPT definitions, Instructions และ Builder configuration ของ BiiigBee Marketing Content OS

## GPT #1 — BiiigBee Campaign Content Generator
สถานะ: **v1.0-rc1 / Candidate / Acceptance Testing Required**

### Canonical Instructions
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

ไฟล์นี้คือข้อความ Instructions หลักที่ต้อง copy เข้า GPT Builder โดยตรงสำหรับ rc1 candidate

### Builder Configuration
`marketing-content-os/gpt/campaign_content_generator/gpt_builder_config_v1.md`

ประกอบด้วย:
- Name
- Description
- Intended users
- Required knowledge upload files
- capabilities
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

---

## GPT #2 — BiiigBee Visual Prompt Refiner
สถานะ: **Specification Ready / NOT FOR PRODUCTION YET**

### Canonical Instructions
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

### Builder Configuration
`marketing-content-os/gpt/visual_prompt_refiner/gpt_builder_config_v1.md`

### Conversation Starters
`marketing-content-os/gpt/visual_prompt_refiner/conversation_starters_v1.md`

GPT #2 ใช้สำหรับ refine visual execution จาก approved content row เท่านั้น ห้ามเปลี่ยน SKU truth, audience, objective, campaign role หรือ claim policy

---

## GPT Builder Setup Guide
`marketing-content-os/gpt/GPT_BUILDER_SETUP_GUIDE.md`

ใช้เป็น checklist ในการสร้าง Custom GPT จริง รวมถึงไฟล์ knowledge ที่ต้อง upload

## GPT Documentation Index
`marketing-content-os/gpt/README.md`

## Canonical SKU Lookup
`marketing-content-os/schemas/sku_lookup_v1.tsv`

มีข้อมูล lookup ของ 24 SKU สำหรับ product-owned prompt placeholders และ deterministic validation

## Acceptance / Validation
- `marketing-content-os/tests/campaign_content_generator_acceptance_corpus_v1.tsv`
- `marketing-content-os/tests/acceptance_execution_rubric_v1.md`
- `marketing-content-os/tools/validate_campaign_output.py`

## Governance
GitHub files above are the documented source for GPT configuration. Do not maintain undocumented alternative Instructions directly in GPT Builder. Any material Builder change must first be reflected in GitHub and versioned/retested.
