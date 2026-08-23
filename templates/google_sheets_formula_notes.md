# Google Sheets Formula Notes

## หลักการ

คอลัมน์ `IMAGE_PROMPT` ปล่อยว่างจาก GPT

ผู้ใช้ใส่สูตรใน Google Sheets เพื่อ:

1. อ่าน `PROMPT_TEMPLATE_ID`
2. ดึง template ที่ตรงกัน
3. แทนค่า placeholder ด้วยค่าจาก row
4. คืน prompt เต็มลงใน `IMAGE_PROMPT`

## คำแนะนำ

ช่วง prototype ใช้ `SUBSTITUTE()` ซ้อนได้
เมื่อ placeholder เพิ่มขึ้น ควรใช้ Named ranges, Mapping table, `MAP()`, `REDUCE()` หรือ Google Apps Script

## Validation

หลังประกอบ prompt ต้องไม่มี placeholder ค้าง เช่น `{{VISUAL_SCENE}}`
