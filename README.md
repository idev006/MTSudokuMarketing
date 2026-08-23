# BiiigBee Marketing Content OS — Design Workspace

สถานะ: Design Draft v0.1  
แบรนด์: BiiigBee Easy Maths

โฟลเดอร์นี้รวบรวมเอกสารออกแบบระบบที่เรากำลังพัฒนาร่วมกัน เพื่อให้การทำการตลาดและประชาสัมพันธ์ของแต่ละ SKU มีความต่อเนื่อง เป็นมืออาชีพ และสามารถเตรียม content ล่วงหน้าเป็นรายเดือนในครั้งเดียวได้

## เป้าหมายหลัก

- รองรับผู้ใช้ที่ไม่มีพื้นฐานการตลาด
- General Mode ที่ใช้งานง่ายมาก
- Advanced Mode สำหรับผู้ใช้ที่ต้องการควบคุมรายละเอียด
- สร้างหลาย content rows ในครั้งเดียว
- วาง campaign sequence และ diversity rules
- สร้าง visual parameters ต่อ row
- ใช้ Prompt Template + Placeholder
- ปล่อย `IMAGE_PROMPT` ว่างไว้ให้ Google Sheets formula ประกอบภายหลัง
- รองรับ prompt ภาพที่ยาวและซับซ้อนได้
- รองรับ review / approve / schedule / publish / measure

## โครงสร้างเอกสาร

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
- `schemas/content_row_schema.tsv`
- `templates/image_prompt_template_v1.txt`
- `templates/google_sheets_formula_notes.md`
- `examples/sample_campaign_output_structure.txt`

## สถานะปัจจุบัน

ยังอยู่ในขั้น **ออกแบบก่อนสร้าง GPTs จริง** ตามที่ตกลงกัน
