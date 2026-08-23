# BiiigBee Campaign Content Generator v1.0-rc1 — Conversation Starters

Use starters that demonstrate the easiest path first and expose Advanced Mode only when needed.

## Recommended ChatGPT Conversation Starters
1. **สร้างคอนเทนต์ 30 โพสต์ให้ SKU นี้**
2. **วางแคมเปญ Facebook 1 เดือนสำหรับสินค้า Sudoku**
3. **สร้าง 20 content rows แบบ General Mode**
4. **สร้างแคมเปญแบบ Advanced Mode**

## General Mode Quick Form
```text
SKU: <required>
NUMBER_OF_ROWS: <required>
PLATFORM: AUTO
CAMPAIGN_DURATION: AUTO
CAMPAIGN_GOAL: AUTO
IMAGE_PROMPT_MODE: FORMULA
```

## Advanced Mode Quick Form
```text
MODE: ADVANCED
SKU: <required>
NUMBER_OF_ROWS: <required>
PLATFORM / PLATFORM_MIX: <optional>
CAMPAIGN_DURATION: <optional>
CAMPAIGN_GOAL: <optional>
CAMPAIGN_THEME: <optional>
AUDIENCE_MIX: <optional>
FUNNEL_MIX: <optional>
CONTENT_PILLAR_MIX: <optional>
MARKETING_ANGLE_PREFERENCES: <optional>
FORBIDDEN_ANGLES: <optional>
CTA_STYLE: <optional>
PROMOTION: <optional; never invent commercial terms>
VISUAL_MIX: <optional>
TONE: <optional>
POSTING_CADENCE: <optional>
ASPECT_RATIO: <optional>
PREVIOUS_CAMPAIGN_CONTEXT: <optional>
IMAGE_PROMPT_MODE: FORMULA
```

## UX Rules
- General Mode users do not need to understand funnels, pillars, CTA distribution or visual mix.
- If SKU and row count are present, start unless a true blocking ambiguity exists.
- `AUTO` is preferable to unnecessary clarification.
- `PLATFORM=AUTO` resolves to one primary platform; use Advanced `PLATFORM_MIX` for multiple platforms.
- Do not infer duration as one row per day.
- If an Advanced override conflicts with source of truth, explain the conflict and use the safe value.
- v1 does not expose PRECOMPILED or BOTH image-prompt modes.
- For N>20, explain that output will be delivered in globally continuous chunks of at most 20 rows.
