# 17 — Prompt Lookup & Placeholder Resolution Contract v1

## Goal
Final image prompts are assembled from three sources without bloating the 27-field content-row schema:

`Content Row + SKU Lookup + Prompt Template -> IMAGE_PROMPT`

## Resolution Layers
### A. Content Row fields
Use row values for campaign/creative variables such as:
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

### B. SKU Lookup fields
Resolve stable product fields by SKU:
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

The canonical lookup source is approved data from `marketing-plan/sku/`. Do not duplicate these fields into every content row.

### C. Prompt Template
Resolve `PROMPT_TEMPLATE_ID` only from the approved prompt-template registry/library.

## Placeholder Precedence
1. Row field when placeholder is explicitly row-owned
2. SKU Lookup when placeholder is product-owned
3. stable template constant when explicitly defined by the template
4. otherwise FAIL validation

Never infer a missing product-owned placeholder from model memory.

## Required Validation
Prompt assembly must fail if:
- SKU lookup returns zero or multiple conflicting records
- PROMPT_TEMPLATE_ID is unknown
- any required placeholder has no value
- any `{{PLACEHOLDER}}` remains after assembly
- a product-owned value conflicts with source of truth

## Google Sheets Model
Recommended sheets/tables:
- `CONTENT_ROWS`
- `SKU_LOOKUP`
- `PROMPT_TEMPLATES`
- `PROMPT_MAPPING` (optional explicit placeholder-to-column mapping)

Formula/App Script should lookup SKU metadata first, then substitute both row and SKU values into the selected template.

## Schema Boundary
The 27-field content-row schema remains unchanged in v1. Product metadata required only for prompt assembly belongs to SKU_LOOKUP, not the row dataset.
