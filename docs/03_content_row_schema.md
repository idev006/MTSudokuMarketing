# 03 — Content Row Schema

แต่ละ row คือ **Marketing Content Unit** ที่สมบูรณ์

## Strategy Fields

- `ROW_ID`
- `SKU`
- `CAMPAIGN_ID`
- `SEQUENCE`
- `PLATFORM`
- `AUDIENCE`
- `OBJECTIVE`
- `FUNNEL_STAGE`
- `CONTENT_PILLAR`
- `MARKETING_ANGLE`
- `CAMPAIGN_ROLE`

## Copy Fields

- `HOOK`
- `HEADLINE`
- `CAPTION`
- `CTA`
- `HASHTAGS`

## Visual Fields

- `VISUAL_TYPE`
- `VISUAL_SUBJECT`
- `VISUAL_SCENE`
- `VISUAL_EMOTION`
- `PRODUCT_PLACEMENT`
- `TEXT_OVERLAY`
- `TEXT_SAFE_ZONE`
- `ASPECT_RATIO`
- `IMAGE_SIZE`

## Prompt Fields

- `PROMPT_TEMPLATE_ID`
- `IMAGE_PROMPT`

## กฎสำหรับ IMAGE_PROMPT

`IMAGE_PROMPT` ต้องอยู่ท้ายสุดและค่าเริ่มต้นเป็นค่าว่าง เพื่อให้ผู้ใช้ใส่ Google Sheets formula ภายหลัง
