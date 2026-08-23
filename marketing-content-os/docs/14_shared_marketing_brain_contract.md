# 14 — Shared Marketing Brain / Knowledge Contract

## Purpose
กำหนดขอบเขตข้อมูลที่ GPT ทุกตัวต้องใช้ร่วมกัน เพื่อลด knowledge drift และไม่ให้ GPT แต่ละตัวมี product truth คนละเวอร์ชัน

## Source-of-Truth Boundary
Marketing Content OS ไม่เป็นเจ้าของข้อเท็จจริงของสินค้า

ข้อเท็จจริงเชิงสินค้าและกลยุทธ์ต้องมาจาก `marketing-plan/` หรือแหล่งข้อมูลที่ได้รับการแต่งตั้งเป็น source of truth เท่านั้น

## Required Knowledge Domains
1. Brand identity and voice
2. Product portfolio / valid SKU catalog
3. SKU grade band and difficulty
4. Product format and fixed product facts
5. Target audience by SKU/difficulty
6. Purpose / job-to-be-done by SKU/difficulty
7. Positioning and core hook
8. Competition-claim policy
9. Channel strategy
10. Campaign defaults
11. Creative/visual rules
12. KPI and feedback-loop definitions

## Data Ownership
### Marketing Plan owns
- SKU validity
- product facts
- audience
- purpose
- positioning
- offer type
- launch priority
- claim restrictions
- channel strategy

### Marketing Content OS owns
- campaign sequencing
- content-row generation
- copy variation
- content diversity
- visual parameter generation
- prompt-template selection
- output schema
- batch validation

## Precedence Rule
When two sources disagree:
1. `marketing-plan/sku/sku_source_of_truth.md`
2. approved structured SKU data under `marketing-plan/sku/`
3. approved Marketing Plan strategy documents
4. Content OS defaults
5. model assumptions

Model assumptions must never overwrite levels 1–3.

## Update Rule
When product truth changes, update Marketing Plan first. Content OS should consume the new truth rather than duplicating or manually rewriting product facts in multiple GPT instructions.

## Specialist GPT Rule
BiiigBee Visual Prompt Refiner receives the approved row context and may refine only creative execution. It may not redefine campaign objective, audience, product facts, offer, or claim status.

## Knowledge Versioning
Production GPT configurations should record:
- `CONTENT_OS_VERSION`
- `ROW_SCHEMA_VERSION`
- `PROMPT_TEMPLATE_VERSION`
- `MARKETING_PLAN_VERSION` or commit/reference

This allows outputs to be traced back to the rules and product truth used at generation time.
