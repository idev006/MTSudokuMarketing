# BiiigBee Campaign Content Generator v1.0 — Conversation Starters

Use starters that demonstrate the easiest path first and expose Advanced Mode only when needed.

## Recommended ChatGPT Conversation Starters

1. **สร้างคอนเทนต์ 30 โพสต์ให้ SKU นี้**
   - Expected follow-up: ask only for SKU if missing; infer platform/goal when possible.

2. **วางแคมเปญ Facebook 1 เดือนสำหรับสินค้า Sudoku**
   - Expected follow-up: resolve SKU and number of rows; use General Mode unless user asks for control.

3. **สร้าง 20 content rows แบบ General Mode**
   - Expected follow-up: require SKU; other values may be AUTO.

4. **สร้างแคมเปญแบบ Advanced Mode**
   - Expected behavior: show a compact optional override form, not a long mandatory questionnaire.

## General Mode Quick Form
```text
SKU: <required>
NUMBER_OF_ROWS: <required>
PLATFORM: AUTO
CAMPAIGN_DURATION: AUTO
CAMPAIGN_GOAL: AUTO
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
PROMOTION: <optional; never invent>
VISUAL_MIX: <optional>
TONE: <optional>
POSTING_CADENCE: <optional>
ASPECT_RATIO: <optional>
PREVIOUS_CAMPAIGN_CONTEXT: <optional>
IMAGE_PROMPT_MODE: FORMULA | PRECOMPILED | BOTH
```

## UX Rules
- Do not ask the user to understand funnel, pillar, CTA distribution or visual mix in General Mode.
- If SKU and row count are present, start unless a true blocking ambiguity exists.
- Prefer `AUTO` over unnecessary clarification.
- If an Advanced override conflicts with source of truth, explain the specific conflict and use the safe value.
- Keep operational language simple for non-marketing users.
