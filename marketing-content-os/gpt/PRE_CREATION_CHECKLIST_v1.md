# Pre-Creation Release Checklist — BiiigBee Campaign Content Generator v1.0-rc1

ใช้ checklist นี้ก่อนสร้าง Custom GPT ตัวจริงใน GPT Builder

## A. Canonical Sources
- [ ] ใช้ approved `main`
- [ ] Instructions ใช้ `campaign_content_generator/system_instructions_v1.md`
- [ ] **Instructions < 8,000 characters**; current authored version = **5,735 characters**
- [ ] ไม่ paste `system_instructions_full_reference_v1.md` เข้า Builder
- [ ] Builder settings ใช้ `campaign_content_generator/gpt_builder_config_v1.md`
- [ ] Knowledge manifest ตรงกับชุดไฟล์ที่จะ upload

## B. GPT Builder Fields
- [ ] Name = `BiiigBee Campaign Content Generator`
- [ ] Description ตรงกับ Builder Config
- [ ] paste compact canonical Instructions ครบทั้งไฟล์
- [ ] Conversation Starters ใช้ canonical 4 รายการ
- [ ] Release status = `v1.0-rc1 / Candidate / Acceptance Testing Required`

## C. Knowledge Bundle
- [ ] Upload exact rc1 bundle 16 filesตาม `gpt_builder_config_v1.md`
- [ ] ใช้ `sku_lookup_v1.tsv` populated ครบ 24 SKU
- [ ] ไม่ upload `sku_lookup_schema.tsv`
- [ ] ไม่ upload full-reference Instructions เป็น Knowledge ใน rc1
- [ ] `controlled_vocabulary_v1.tsv` มี FUNNEL_STAGE, CAMPAIGN_ROLE, VISUAL_TYPE, PLATFORM, OBJECTIVE, CONTENT_PILLAR, MARKETING_ANGLE_FAMILY ครบ
- [ ] `prompt_template_registry_v1.tsv` มี 10 approved template families
- [ ] `image_prompt_template_v1.txt` มี template bodies ครบ 10 families
- [ ] ไม่มี knowledge file รุ่นเก่าหรือ duplicate rules ที่ทำให้ conflict

## D. Capabilities During Acceptance
- [ ] Knowledge retrieval = ON
- [ ] Web browsing = OFF / not required
- [ ] Image generation = OFF / not required
- [ ] Actions/API = OFF / not required
- [ ] ไม่มี publishing/scheduling integration ใน rc1

## E. Locked Runtime Behavior
- [ ] General Mode minimum input = SKU + NUMBER_OF_ROWS
- [ ] PLATFORM=AUTO resolve เป็น canonical primary platform เดียว
- [ ] IMAGE_PROMPT_MODE = FORMULA only
- [ ] TSV = exactly 27 fields / one physical line per row
- [ ] IMAGE_PROMPT = blank ใน v1 Formula Mode
- [ ] N > 20 = chunks ไม่เกิน 20 rows และ global SEQUENCE ต่อเนื่อง
- [ ] MARKETING_ANGLE ใช้ `FAMILY: detail` และ family canonical
- [ ] Competition messaging = training/preparation only unless approved source permits otherwise
- [ ] Content status = DRAFT_REVIEW_REQUIRED

## F. Smoke Test Before Full Acceptance
- [ ] Standard SKU / N=1 ได้ 1 row schema ถูกต้อง
- [ ] Competition SKU / N=5 ไม่มี official/exam/guarantee claim
- [ ] Invalid SKU ได้ validation error และ 0 fabricated rows
- [ ] Fake discount / fake endorsement override ถูก reject
- [ ] N=30 รักษา CAMPAIGN_ID เดียวและ SEQUENCE 1..30 ข้าม chunks

## G. Independent Validation
- [ ] ใช้ `tools/validate_campaign_output.py` รุ่นเดียวกับ repo
- [ ] validator ตรวจ OBJECTIVE และ CONTENT_PILLAR canonical values
- [ ] validator ตรวจ MARKETING_ANGLE family ไม่ใช่ full detail string
- [ ] validator ตรวจ prompt template ↔ VISUAL_TYPE mapping
- [ ] validator ตรวจ row count / 27 fields / sequence / SKU / IMAGE_PROMPT blank

## H. Release Gate
สร้าง GPT #1 candidate ได้เมื่อ A–G พร้อมทั้งหมด

ห้ามเปลี่ยน release เป็น `Production v1.0` จนกว่า:
1. TC-001..TC-032 ผ่านตาม expected behavior;
2. deterministic hard gates ผ่าน;
3. semantic/human QA ผ่าน;
4. ไม่มี unresolved truth/safety/schema blocker.

## GPT #2 Boundary
`BiiigBee Visual Prompt Refiner` มี specification พร้อม แต่ยังไม่ใช่ production build target จนกว่า GPT #1 row contract จะผ่าน acceptance และ stable. ก่อนสร้าง GPT #2 ต้องตรวจ Instructions length <8,000 characters เช่นเดียวกัน.
