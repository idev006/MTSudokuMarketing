# Google Sheets Formula Notes — v1

## v1 Rule
`IMAGE_PROMPT_MODE = FORMULA` only.

The GPT leaves `IMAGE_PROMPT` blank. Google Sheets or Apps Script assembles the final prompt from:

`CONTENT_ROWS + SKU_LOOKUP + PROMPT_TEMPLATES`

## Recommended Tables
- `CONTENT_ROWS` — 27-field campaign rows
- `SKU_LOOKUP` — stable product-owned placeholder values keyed by SKU
- `PROMPT_TEMPLATES` — approved template ID + template text
- `PROMPT_MAPPING` — optional explicit placeholder mapping

## Assembly Sequence
1. Read `PROMPT_TEMPLATE_ID` from the content row.
2. Validate the template ID exists in the approved registry.
3. Lookup SKU metadata from `SKU_LOOKUP`.
4. Substitute row-owned placeholders.
5. Substitute SKU-owned placeholders.
6. Return the complete prompt into `IMAGE_PROMPT`.
7. Validate no unresolved `{{PLACEHOLDER}}` remains.

## Row-Owned Examples
- SKU
- PLATFORM
- AUDIENCE
- OBJECTIVE
- MARKETING_ANGLE
- VISUAL_TYPE
- VISUAL_SUBJECT
- VISUAL_SCENE
- VISUAL_EMOTION
- PRODUCT_PLACEMENT
- TEXT_OVERLAY
- TEXT_SAFE_ZONE
- ASPECT_RATIO
- IMAGE_SIZE

## SKU-Owned Examples
- BRAND_NAME
- PRODUCT_NAME
- THAI_NAME
- GRADE_BAND
- INTERNAL_DIFFICULTY
- DISPLAY_DIFFICULTY
- PRODUCT_FORMAT
- PUZZLE_COUNT
- ANSWER_KEY_STATUS
- OFFER_TYPE
- CLAIM_POLICY_CLASS

## Formula Direction
For a small prototype, nested `SUBSTITUTE()` is acceptable. For the full placeholder set, prefer named ranges plus `XLOOKUP`/`INDEX-MATCH`, `MAP()`, `REDUCE()`, or Apps Script rather than deeply nested manual formulas.

## Hard Validation
Prompt assembly fails if:
- SKU lookup is missing/ambiguous
- template ID is unknown
- required product-owned data is missing
- unresolved placeholders remain
- prompt product facts conflict with approved lookup values

Never have the formula invent a missing product value.
