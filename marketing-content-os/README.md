# BiiigBee Marketing Content OS — Design & Build Workspace

สถานะ: **v1 Contract Review Complete — Ready to Build Campaign Content Generator**  
แบรนด์: **BiiigBee Easy Maths**

โฟลเดอร์นี้เก็บระบบออกแบบและข้อกำหนดสำหรับ Marketing Content OS ซึ่งเปลี่ยนข้อมูลจาก Marketing Plan / SKU source of truth ให้เป็น campaign content แบบ batch ที่ต่อเนื่อง ตรวจสอบได้ และพร้อมเข้าสู่ workflow การผลิตจริง

## System Boundary

- **Marketing Plan = Truth** — เจ้าของ SKU, product facts, target, purpose, positioning, channels และ claim restrictions
- **Marketing Content OS = Execution** — เจ้าของ campaign sequence, content rows, copy variation, visual parameters, prompt-template selection และ batch quality gates

## GPT Architecture

1. **BiiigBee Campaign Content Generator** — GPT หลัก; ต้องสร้างและผ่าน acceptance test ก่อน
2. **BiiigBee Visual Prompt Refiner** — specialist; สร้างหลัง row contract ของ GPT หลัก stable แล้ว

## v1 Design Goals

- ใช้งานง่ายสำหรับผู้ไม่มีพื้นฐานการตลาด
- General Mode ใช้ input ขั้นต่ำ
- Advanced Mode = engine เดียวกัน + overrides
- สร้าง N content rows แบบ campaign ไม่ใช่โพสต์สุ่ม
- ควบคุม diversity / selling frequency / claim safety
- สร้าง copy + visual parameters + prompt template ID
- `IMAGE_PROMPT` เป็น field สุดท้ายและว่างโดย default ใน formula mode
- รองรับ TSV / Google Sheets และขยาย CSV/JSON ในอนาคต
- Human review ก่อน publish

## Core Documents

### Foundation
- `docs/01_system_vision.md`
- `docs/02_general_and_advanced_modes.md`
- `docs/03_content_row_schema.md`
- `docs/04_image_prompt_template_architecture.md`
- `docs/05_campaign_strategy_and_diversity.md`
- `docs/06_workflow_and_process_engineering.md`
- `docs/07_gpt_architecture.md`
- `docs/08_output_file_spec.md`
- `docs/09_design_review_and_recommendations.md`
- `docs/10_implementation_roadmap.md`

### v1 Production Contracts
- `docs/11_gpt_product_requirements.md`
- `docs/12_input_output_contract.md`
- `docs/13_system_instruction_quality_gates.md`
- `docs/14_shared_marketing_brain_contract.md`
- `docs/15_acceptance_test_plan.md`

### Schemas / Templates / Examples
- `schemas/content_row_schema.tsv`
- `templates/image_prompt_template_v1.txt`
- `templates/google_sheets_formula_notes.md`
- `examples/sample_campaign_output_structure.txt`

## Current Decision

**พร้อมเข้าสู่การสร้าง BiiigBee Campaign Content Generator v1.0** หลังจาก v1 contracts ข้างต้นได้รับการ merge เป็น source of truth ของ Content OS
