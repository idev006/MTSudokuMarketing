# GPT Builder Setup Guide — BiiigBee Marketing Content OS

## GPT #1 — BiiigBee Campaign Content Generator v1.0-rc1

### Name
BiiigBee Campaign Content Generator

### Description
สร้างแคมเปญคอนเทนต์แบบ batch จาก SKU ที่อนุมัติ พร้อมข้อความขาย ทิศทางภาพ และ prompt mapping โดยยึด Marketing Plan เป็น source of truth และมี quality gates ก่อนใช้งาน

### Instructions
Copy the complete contents of:
`marketing-content-os/gpt/campaign_content_generator/system_instructions_v1.md`

This is the compact canonical Builder version and must remain below 8,000 characters. Do not paste `system_instructions_full_reference_v1.md` into Instructions.

### Conversation Starters
Copy the four starters from:
`marketing-content-os/gpt/campaign_content_generator/conversation_starters_v1.md`

### Knowledge Uploads — exact rc1 bundle
Upload exactly the **19 files** listed in:
`marketing-content-os/gpt/campaign_content_generator/gpt_builder_config_v1.md`

Critical grounding files include:
- `sku_lookup_v1.tsv`
- `sku_content_spec_v1.tsv`
- `controlled_vocabulary_v1.tsv`
- `prompt_template_registry_v1.tsv`
- `runtime_reference_v1.md`
- `sku_content_reference_v1.md`

Product-detail rule: grid size, named variants, composition, ratios and type counts must be grounded in approved SKU content sources. If exact composition is unspecified, use only approved grid size + generic mixed-Sudoku wording.

### Capabilities for rc1 Acceptance
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
1. valid Standard SKU + 1 row
2. valid Competition SKU + 5 rows
3. invalid SKU -> zero fabricated rows
4. fake discount/official endorsement -> reject unsafe override
5. 30 rows -> one CAMPAIGN_ID and global SEQUENCE 1..30 across chunks
6. Standard SKU copy/visual must not invent named variant membership/counts when composition is unspecified

If any hard truth/schema/safety test fails, fix GitHub source first, rebuild the GPT candidate, then retest.

### Release Label
Use `v1.0-rc1` / Candidate / Acceptance Testing Required.
Do not label Production v1.0 until TC-001..TC-032 and independent deterministic + semantic gates pass.

---

## GPT #2 — BiiigBee Visual Prompt Refiner
Keep GPT #2 on hold until GPT #1 row contract is accepted and stable.

## Change-Control Rule
Whenever Instructions/knowledge change: update GitHub source first, verify Instructions <8,000 characters, rebuild GPT knowledge, and rerun affected acceptance/regression tests.
