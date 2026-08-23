# Pre-Creation Release Checklist — BiiigBee Campaign Content Generator v1.0-rc1

## A. Builder
- [ ] ใช้ approved `main`
- [ ] Instructions = `campaign_content_generator/system_instructions_v1.md`
- [ ] Instructions < 8,000 characters
- [ ] Description ตรง Builder Config
- [ ] Conversation Starters = canonical 4 รายการ

## B. Knowledge Bundle
- [ ] Upload exact rc1 bundle **19 files** ตาม `gpt_builder_config_v1.md`
- [ ] `sku_lookup_v1.tsv` ครบ 24 SKU
- [ ] `sku_content_spec_v1.tsv` ครบ 24 SKU
- [ ] `sku_content_reference_v1.md` ถูก upload
- [ ] `runtime_reference_v1.md` ถูก upload
- [ ] `controlled_vocabulary_v1.tsv` และ prompt registry/template library ถูก upload
- [ ] ไม่ upload `sku_lookup_schema.tsv` หรือ full-reference Instructions

## C. Product-detail grounding
- [ ] Grid size มาจาก SKU content spec/reference เท่านั้น
- [ ] `VARIANT_SCOPE` ไม่ถูกตีความว่าเป็น exact composition ของทุก Standard SKU
- [ ] ถ้า `EXACT_COMPOSITION_STATUS=UNSPECIFIED` ห้ามอ้าง named variants, ratios หรือ per-type counts
- [ ] Standard SKU ใช้ approved grid size + generic mixed-Sudoku wording ได้
- [ ] Competition claims คง training/preparation และไม่อ้าง exhaustive official coverage

## D. Locked Runtime
- [ ] General Mode minimum = SKU + NUMBER_OF_ROWS
- [ ] PLATFORM=AUTO resolve เป็น canonical primary platform เดียว
- [ ] IMAGE_PROMPT_MODE=FORMULA only
- [ ] exactly 27 fields; IMAGE_PROMPT blank
- [ ] N>20 chunks <=20 rows และ global sequence ต่อเนื่อง
- [ ] MARKETING_ANGLE family canonical
- [ ] status = DRAFT_REVIEW_REQUIRED

## E. Smoke Tests
- [ ] Standard SKU / N=1: schema + product details grounded
- [ ] Competition SKU / N=5: no official/exam/guarantee claim
- [ ] Invalid SKU: 0 fabricated rows
- [ ] Fake promotion/endorsement: rejected
- [ ] N=30: one CAMPAIGN_ID + sequence 1..30
- [ ] No invented exact composition/counts when source says UNSPECIFIED

## F. Release Gate
Do not label `Production v1.0` until TC-001..TC-032, deterministic hard gates, and semantic/human QA pass with no unresolved truth/safety/schema blocker.

GPT #2 remains on hold until GPT #1 row contract is stable.
