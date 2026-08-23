# 04 — Image Prompt Template Architecture v1

## Core Model
Do not let the GPT invent a new long-form image prompt freestyle for every row.

Use:

> Content Row + SKU Lookup + Approved Prompt Template + Placeholder Resolution

In v1, `IMAGE_PROMPT_MODE=FORMULA` only. The GPT leaves the final `IMAGE_PROMPT` field blank; Google Sheets/App Script assembles it later.

## Placeholder Convention
Use `{{PLACEHOLDER_NAME}}`.

Row-owned examples:
- `{{SKU}}`
- `{{AUDIENCE}}`
- `{{OBJECTIVE}}`
- `{{VISUAL_SUBJECT}}`
- `{{VISUAL_SCENE}}`
- `{{VISUAL_EMOTION}}`
- `{{TEXT_SAFE_ZONE}}`
- `{{ASPECT_RATIO}}`

SKU-owned examples:
- `{{BRAND_NAME}}`
- `{{PRODUCT_NAME}}`
- `{{GRADE_BAND}}`
- `{{DISPLAY_DIFFICULTY}}`
- `{{PRODUCT_FORMAT}}`

SKU-owned values come from approved SKU lookup/source data, not extra content-row columns.

## Approved v1 Template Families
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

All ten are implemented in `templates/image_prompt_template_v1.txt` and registered in `templates/prompt_template_registry_v1.tsv`.

## Mapping Rule
Each canonical `VISUAL_TYPE` maps to an approved template family. Unknown IDs or incompatible VISUAL_TYPE/template mappings are hard validation failures.

## Versioning
Every row stores `PROMPT_TEMPLATE_ID`. Prompt-template library/registry changes require version traceability in the knowledge manifest.

## Assembly Validation
Final prompt assembly must verify:
- SKU lookup resolves exactly one approved record
- template ID exists
- all required placeholders resolve
- no `{{PLACEHOLDER}}` remains
- product facts match approved lookup values
