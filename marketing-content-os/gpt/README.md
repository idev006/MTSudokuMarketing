# BiiigBee Marketing Content OS — GPT Documentation Index

เอกสารในโฟลเดอร์นี้เป็นจุดอ้างอิงหลักสำหรับสร้าง Custom GPTs ของ Marketing Content OS

## GPT #1 — BiiigBee Campaign Content Generator
สถานะ: **v1.0-rc1 / Candidate / Acceptance Testing Required**

Canonical files:
- `campaign_content_generator/system_instructions_v1.md` — ข้อความ Instructions ที่นำไปใส่ใน GPT Builder
- `campaign_content_generator/gpt_builder_config_v1.md` — ชื่อ, description, knowledge files, capabilities, defaults
- `campaign_content_generator/conversation_starters_v1.md` — conversation starters
- `campaign_content_generator/knowledge_mapping_v1.md` — source-of-truth ownership / precedence
- `campaign_content_generator/interaction_flow_v1.md` — General / Advanced interaction behavior

GPT #1 ต้องผ่าน deterministic + semantic acceptance gates ก่อนใช้ชื่อ Production v1.0

## GPT #2 — BiiigBee Visual Prompt Refiner
สถานะ: **Design/Implementation Spec Ready — NOT FOR PRODUCTION YET**

Canonical files:
- `visual_prompt_refiner/system_instructions_v1.md`
- `visual_prompt_refiner/gpt_builder_config_v1.md`
- `visual_prompt_refiner/conversation_starters_v1.md`

GPT #2 ต้องไม่เปลี่ยน product truth, campaign objective, audience, campaign role หรือ claim policy ที่ GPT #1 ส่งมา และจะเปิด production หลัง GPT #1 row contract ผ่าน hard gates แล้ว

## GPT Builder Setup
ดูขั้นตอน copy/upload ที่:
- `GPT_BUILDER_SETUP_GUIDE.md`

## Shared Knowledge / Data
สำคัญสำหรับ GPT #1:
- `../schemas/sku_lookup_v1.tsv` — canonical lookup 24 SKU
- `../schemas/content_row_schema.tsv`
- `../schemas/controlled_vocabulary_v1.tsv`
- `../templates/prompt_template_registry_v1.tsv`
- `../templates/image_prompt_template_v1.txt`
- `../knowledge_manifest_v1.yaml`

## Source-of-Truth Rule
**Marketing Plan = Truth**

**Marketing Content OS = Execution**

ห้าม copy หรือแก้ข้อเท็จจริง SKU แบบแยกเวอร์ชันใน GPT instructions ถ้าข้อมูลสินค้าเปลี่ยน ให้แก้ Marketing Plan / canonical lookup ก่อน แล้ว rebuild knowledge bundle
