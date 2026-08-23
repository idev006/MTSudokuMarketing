# 11 — GPT Product Requirements (PRD)

## Product
**BiiigBee Marketing Content OS**

## Goal
เปลี่ยนข้อมูลสินค้าและ Marketing Plan ที่เป็น source of truth ให้เป็น campaign content แบบ batch ที่สอดคล้องกัน ใช้งานได้จริง และตรวจสอบได้

## Business Objectives
1. ลดเวลาวางแผนและผลิต content รายเดือน
2. ทำให้ผู้ใช้ที่ไม่มีพื้นฐานการตลาดสามารถสร้าง campaign ที่มีโครงสร้างได้
3. รักษาความถูกต้องของ SKU, target, purpose, positioning และ claims
4. ลด content ซ้ำ การขายตรงมากเกินไป และ visual ที่จำเจ
5. รองรับการขยายจาก 1 SKU ไปสู่หลาย SKU และหลาย platform
6. รองรับ workflow: Generate → Review → Approve → Visual → Schedule → Publish → Measure → Learn

## Primary GPT
### BiiigBee Campaign Content Generator
หน้าที่หลัก:
- รับ SKU + campaign request
- อ่าน product/marketing truth
- วาง campaign arc
- สร้าง N content rows
- สร้าง copy และ visual parameters
- เลือก prompt template
- ตรวจ quality gates ก่อนส่ง output
- ปล่อย IMAGE_PROMPT ว่างโดย default เพื่อประกอบด้วย formula/template ภายหลัง

## Specialist GPT
### BiiigBee Visual Prompt Refiner
หน้าที่:
- รับ content row ที่ผ่าน intent แล้ว
- refine visual concept และ image prompt
- ห้ามเปลี่ยน SKU fact, objective, target, campaign role หรือ claim policy

## Users
### Primary User
เจ้าของแบรนด์ / ผู้ดูแลสินค้า ที่ไม่จำเป็นต้องมีความรู้การตลาดลึก

### Secondary Users
- Marketing staff
- Content creator / copywriter
- Social media admin
- Campaign planner
- Creative / visual operator

## Non-Goals
ระบบนี้ไม่ใช่:
- product catalog generator
- pricing engine
- ad bidding engine
- publishing scheduler โดยตรง
- social proof/testimonial generator
- เครื่องมือสร้างข้อมูลสินค้าใหม่จากการเดา

## Core Principle
**Marketing Plan = Truth**

**Marketing Content OS = Execution**

หากข้อมูลระหว่าง GPT output กับ source of truth ขัดกัน ให้ source of truth ชนะเสมอ

## Version Target
v1.0 ต้องทำ Campaign Content Generator ให้ผ่าน acceptance test ก่อน จึงค่อยเปิดใช้ Visual Prompt Refiner เป็น production specialist
