# GPT Builder Setup Guide — BiiigBee Marketing Content OS

## GPT #1 — BiiigBee Campaign Content Generator v1.0-rc1

### Name
BiiigBee Campaign Content Generator

### Description
สร้าง campaign content แบบ batch จาก SKU ที่อนุมัติแล้ว พร้อม copy, visual direction, prompt-template mapping และ quality gates โดยยึด Marketing Plan เป็น source of truth

### Instructions
Copy the complete contents of:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

Do not summarize or rewrite the instruction text when creating the rc1 candidate.

### Conversation Starters
Copy the four starters from:
`marketing-content-os/gpt/campaign_content_generator/conversation_starters_v1.md`

### Knowledge Uploads
Upload the exact approved files listed in:
`marketing-content-os/gpt/campaign_content_generator/gpt_builder_config_v1.md`

Critical data files include:
- `marketing-content-os/schemas/sku_lookup_v1.tsv`
- `marketing-content-os/schemas/content_row_schema.tsv`
- `marketing-content-os/schemas/controlled_vocabulary_v1.tsv`
- `marketing-content-os/templates/prompt_template_registry_v1.tsv`
- `marketing-content-os/templates/image_prompt_template_v1.txt`
- `marketing-content-os/knowledge_manifest_v1.yaml`

### Capabilities for rc1
Keep external variability low during acceptance:
- Knowledge/file retrieval: ON
- Web browsing: not required
- Image generation: not required
- Actions/API: not required

### Release Label
Use `v1.0-rc1` / Candidate / Acceptance Testing Required.
Do not label Production v1.0 until TC-001..TC-032 and independent deterministic gates pass.

---

## GPT #2 — BiiigBee Visual Prompt Refiner

### Name
BiiigBee Visual Prompt Refiner

### Description
ปรับ visual direction และ prompt specification จาก approved content row โดยรักษา SKU truth, audience, objective, campaign role และ claim policy เดิม

### Instructions
Copy the complete contents of:
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

### Conversation Starters
Use:
`marketing-content-os/gpt/visual_prompt_refiner/conversation_starters_v1.md`

### Knowledge Uploads
Use the set documented in:
`marketing-content-os/gpt/visual_prompt_refiner/gpt_builder_config_v1.md`

### Release Boundary
Do not publish GPT #2 as production before GPT #1 has a stable accepted row contract.

---

## Change-Control Rule
When an instruction, schema, taxonomy, prompt template, or Marketing Plan source changes:
1. change the owning GitHub source first;
2. update `knowledge_manifest_v1.yaml` / version reference as required;
3. rebuild the GPT knowledge upload set;
4. rerun affected acceptance tests plus regression tests.

The GPT Builder configuration must never become a separate undocumented source of truth.
