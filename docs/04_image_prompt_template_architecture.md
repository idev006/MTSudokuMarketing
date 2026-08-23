# 04 — Image Prompt Template Architecture

## แนวคิดหลัก

ไม่ให้ GPT เขียน image prompt แบบ freestyle ใหม่ทุก row

ใช้:

> Row Parameters + Prompt Template + Placeholder Mapping + Formula

## Placeholder Convention

ใช้รูปแบบ `{{PLACEHOLDER_NAME}}`

ตัวอย่าง:

- `{{SKU}}`
- `{{AUDIENCE}}`
- `{{VISUAL_SUBJECT}}`
- `{{VISUAL_SCENE}}`
- `{{VISUAL_EMOTION}}`
- `{{TEXT_SAFE_ZONE}}`
- `{{ASPECT_RATIO}}`

## Template Library ที่ควรมี

- `IMG-PRODUCT-HERO-V1`
- `IMG-LIFESTYLE-V1`
- `IMG-PARENT-CHILD-V1`
- `IMG-STUDENT-ACTIVITY-V1`
- `IMG-TEACHER-CLASSROOM-V1`
- `IMG-PUZZLE-CHALLENGE-V1`
- `IMG-BENEFIT-V1`
- `IMG-INFOGRAPHIC-V1`
- `IMG-COMPETITION-V1`
- `IMG-PRODUCT-BOX-V1`

## Template Versioning

ทุก row ต้องมี `PROMPT_TEMPLATE_ID` เพื่อ audit และเปลี่ยนเวอร์ชันได้
