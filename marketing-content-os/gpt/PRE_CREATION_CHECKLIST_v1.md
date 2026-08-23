# Pre-Creation Release Checklist — BiiigBee Campaign Content Generator v1.0-rc1

ใช้ checklist นี้ก่อนสร้าง Custom GPT ตัวจริงใน GPT Builder

## A. Canonical Sources
- [ ] GitHub branch/source ที่ใช้คือ approved `main`
- [ ] System Instructions ใช้ไฟล์ `campaign_content_generator/system_instructions_v1.md` แบบเต็ม ไม่สรุปใหม่
- [ ] Builder settings ใช้ `campaign_content_generator/gpt_builder_config_v1.md`
- [ ] Knowledge manifest เป็นเวอร์ชันเดียวกับชุดไฟล์ที่จะ upload

## B. GPT Builder Fields
- [ ] Name = `BiiigBee Campaign Content Generator`
- [ ] Description ตรงกับ Builder Config
- [ ] Instructions ถูก paste ครบทั้งไฟล์ canonical
- [ ] Conversation Starters ใช้ชุด canonical 4 รายการ
- [ ] Release status ถือเป็น `v1.0-rc1 / Candidate / Acceptance Testing Required`

## C. Knowledge Bundle
- [ ] Upload exact rc1 bundle 16 filesตาม `gpt_builder_config_v1.md`
- [ ] ใช้ `sku_lookup_v1.tsv` ที่ populated ครบ 24 SKU
- [ ] ไม่ upload `sku_lookup_schema.tsv`
- [ ] `controlled_vocabulary_v1.tsv` มี FUNNEL_STAGE, CAMPAIGN_ROLE, VISUAL_TYPE, PLATFORM, OBJECTIVE, CONTENT_PILLAR, MARKETING_ANGLE_FAMILY ครบ
- [ ] `prompt_template_registry_v1.tsv` มี 10 approved template families
- [ ] `image_prompt_template_v1.txt` มี template bodies ครบทั้ง 10 families
- [ ] ไม่มี knowledge file รุ่นเก่าหรือ duplicate rules ที่ทำให้ source conflict

## D. Capabilities During Acceptance
- [ ] Knowledge retrieval = ON
- [ ] Web browsing = OFF / not required
- [ ] Image generation = OFF / not required
- [ ] Actions/API = OFF / not required
- [ ] ไม่มี publishing/scheduling integration ใน rc1

## E. Locked Runtime Behavior
- [ ] General Mode minimum input = SKU + NUMBER_OF_ROWS
- [ ] PLATFORM=AUTO ต้อง resolve เป็น canonical primary platform เดียว
- [ ] IMAGE_PROMPT_MODE = FORMULA only
- [ ] TSV = exactly 27 fields / one physical line per row
- [ ] IMAGE_PROMPT = blank ใน v1 formula mode
- [ ] N > 20 = chunks ไม่เกิน 20 rows แต่ global SEQUENCE ต้องต่อเนื่อง
- [ ] MARKETING_ANGLE ใช้ `FAMILY: detail` และ family ต้อง canonical
- [ ] Competition messaging อยู่ใน training/preparation territory
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

ห้ามเปลี่ยนชื่อ release เป็น `Production v1.0` จนกว่า:
1. TC-001..TC-032 ผ่านตาม expected behavior;
2. deterministic hard gates ผ่าน;
3. semantic/human QA ผ่าน;
4. ไม่มี unresolved truth/safety/schema blocker.

## GPT #2 Boundary
`BiiigBee Visual Prompt Refiner` มี specification พร้อม แต่ยังไม่ใช่ production build target จนกว่า GPT #1 row contract จะผ่าน acceptance และ stable.
