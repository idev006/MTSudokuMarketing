# 07 — GPT Architecture

## GPT หลัก

### BiiigBee Campaign Content Generator

หน้าที่:

- รับ SKU และจำนวน rows
- วาง campaign strategy
- สร้าง copy
- สร้าง visual parameters
- เลือก prompt template
- ปล่อย `IMAGE_PROMPT` ว่าง
- คืน output หลาย rows

## GPT Specialist

### BiiigBee Visual Prompt Refiner

ใช้เมื่อต้องการปรับ visual prompt ของ row ใด row หนึ่งแบบเฉพาะเจาะจง

## Shared Marketing Brain

ควรใช้ source of truth ร่วมกัน เช่น:

- brand bible
- product catalog
- SKU composition
- target/purpose
- claim policy
- content pillars
- visual brand system
- campaign memory schema

ไม่ควร copy knowledge คนละเวอร์ชันเข้า GPT หลายตัว เพราะจะเกิด knowledge drift
