# GPT Builder Setup Guide — BiiigBee Marketing Content OS

## GPT #1 — BiiigBee Campaign Content Generator v1.0-rc1

### Name
BiiigBee Campaign Content Generator

### Description
สร้าง campaign content แบบ batch จาก SKU ที่อนุมัติแล้ว พร้อม copy, visual direction, prompt-template mapping และ quality gates โดยยึด Marketing Plan เป็น source of truth

### Instructions
Copy the complete contents of:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

This is the **compact canonical Builder version** and is intentionally below the 8,000-character Instructions limit. Current authored length: **5,735 characters**.

Do **not** paste:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_full_reference_v1.md`
into the Instructions field. That file is maintainer/reference documentation only.

Do not summarize or rewrite the compact canonical instruction text when creating the rc1 candidate.

### Conversation Starters
Copy the four starters from:
`marketing-content-os/gpt/campaign_content_generator/conversation_starters_v1.md`

### Knowledge Uploads — exact rc1 bundle
Upload exactly the 16 files listed in:
`marketing-content-os/gpt/campaign_content_generator/gpt_builder_config_v1.md`

Important:
- use populated `marketing-content-os/schemas/sku_lookup_v1.tsv`
- do not upload `sku_lookup_schema.tsv`
- do not upload the full-reference instructions as Knowledge for rc1
- keep the uploaded bundle version-aligned with `knowledge_manifest_v1.yaml`

### Capabilities for rc1 Acceptance
Keep external variability low:
- Knowledge/file retrieval: ON
- Web browsing: OFF / not required
- Image generation: OFF / not required
- Actions/API: OFF / not required

### Default Contract
- Mode: `GENERAL`
- minimum input: `SKU + NUMBER_OF_ROWS`
- `PLATFORM=AUTO` resolves to one canonical primary platform
- `IMAGE_PROMPT_MODE=FORMULA` only
- N > 20 uses max-20-row chunks with global continuous sequence
- all content remains `DRAFT_REVIEW_REQUIRED`

### Immediate Smoke Test After Creation
Before full acceptance, run:
1. valid Standard SKU + 1 row
2. valid Competition SKU + 5 rows
3. invalid SKU -> zero fabricated rows
4. fake discount/official endorsement -> reject unsafe override
5. 30 rows -> one CAMPAIGN_ID and global SEQUENCE 1..30 across chunks

If any hard truth/schema/safety test fails, fix GitHub source first, rebuild the GPT candidate, then retest.

### Release Label
Use `v1.0-rc1` / Candidate / Acceptance Testing Required.
Do not label Production v1.0 until TC-001..TC-032 and independent deterministic + semantic gates pass.

---

## GPT #2 — BiiigBee Visual Prompt Refiner

### Name
BiiigBee Visual Prompt Refiner

### Description
ปรับ visual direction และ prompt-ready fields จาก approved content row โดยไม่เปลี่ยน product truth, audience, objective, campaign role หรือ claim policy

### Instructions
Copy the complete contents of:
`marketing-content-os/gpt/visual_prompt_refiner/system_instructions_v1.md`

Before creating GPT #2, independently confirm that its current Instructions text is below the Builder character limit. GPT #2 remains on hold until GPT #1 row contract passes acceptance.

### Conversation Starters
Use:
`marketing-content-os/gpt/visual_prompt_refiner/conversation_starters_v1.md`

### Knowledge Uploads
Use the set documented in:
`marketing-content-os/gpt/visual_prompt_refiner/gpt_builder_config_v1.md`

### Release Boundary
Do not create/publish GPT #2 as a production tool before GPT #1 has a stable accepted row contract and visual-refiner acceptance tests exist.

---

## Change-Control Rule
Whenever Instructions change:
1. edit GitHub canonical source first;
2. verify Instructions remain <8,000 characters;
3. update manifest/version if material;
4. rebuild GPT/Knowledge as required;
5. rerun affected acceptance/regression tests.

The GPT Builder configuration must never become a separate undocumented source of truth.
