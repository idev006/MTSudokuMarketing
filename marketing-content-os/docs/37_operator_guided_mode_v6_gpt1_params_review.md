# Operator Guided Mode V6 — GPT1 Parameter and Contrast Review

Status: ACTIVE UX REVIEW
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## User feedback

The user reported that the product combo box/control still had a color contrast risk and noted that GPT1 accepts more parameters than only `SKU`, `NUMBER_OF_ROWS`, `PLATFORM`, and `CAMPAIGN_GOAL`.

## UX principle

A good operator UI should reduce memory load and typing. When a value can be selected safely from project source-of-truth data or controlled vocabularies, it should be presented as a control instead of a free text field.

## Implemented changes

### Contrast and control visibility

- Forced high-contrast text/background styling for `QComboBox`, `QLineEdit`, `QTextEdit`, tables, tabs, and disabled states.
- Added explicit `QComboBox QAbstractItemView` styling so dropdown items are dark text on white background with readable blue selection.
- Added a CSS down-arrow indicator for the combo box to avoid a white/blank-looking control in Windows themes.

### Product selection

- Product selection remains a combo box loaded from `marketing-content-os/schemas/sku_lookup_v1.tsv`.
- Display text is product name + SKU.
- Runtime value used in GPT1 prompt is the canonical SKU.
- Product detail card shows product truth fields so the operator can confirm the selection without reading source files.

### GPT1 parameter controls

Added explicit controls for:

- `PLATFORM`: `AUTO`, `FACEBOOK`, `LINE_OA`, `MARKETPLACE`, `LANDING_PAGE`
- `CAMPAIGN_GOAL`: `AUTO`, `BUILD_AWARENESS`, `EDUCATE`, `CREATE_ENGAGEMENT`, `SHOW_PRODUCT_VALUE`, `BUILD_TRUST`, `DRIVE_CONSIDERATION`, `DRIVE_CONVERSION`, `RETENTION_CROSS_SELL`
- `CAMPAIGN_DURATION`: `AUTO`, `7_DAYS`, `14_DAYS`, `30_DAYS`, `60_DAYS`, `90_DAYS`
- `AUTO_PLATFORM_RESOLUTION`
- `CONTROLLED_VOCAB_VALIDATION`
- `SKU_LOOKUP_PROMPT_ASSEMBLY`
- `KNOWLEDGE_MANIFEST_REQUIRED`

The prompt preview updates automatically when these controls change.

## Expected operator feeling

The operator should feel:

```text
I do not need to remember SKU codes.
I do not need to remember platform or campaign goal spelling.
I can see product truth before creating GPT1 prompt.
The controls are readable under Windows themes.
The generated GPT1 prompt is ready to copy.
```

## Remaining backlog

- Confirm the exact complete GPT1 parameter grammar from final GPT1 instructions if more keys are formally supported.
- Add a saved preset profile if operators repeatedly use the same parameter bundle.
- Add a search/filter box for product combo if 24 SKUs grows into a larger catalog.
