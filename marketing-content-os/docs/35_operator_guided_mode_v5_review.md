# Operator Guided Mode V5 UI/UX Review

Status: ACTIVE UI/UX REVIEW
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## 1. UX principle

A production operator should not need to memorize SKU codes, folder paths, hidden sequencing rules, or file naming conventions. The app must convert project knowledge into selectable controls and guided actions.

## 2. User review input

The user identified that SKU should not be a free-text field. A better UI presents human-readable product names in a selector while preserving the SKU as the machine value.

## 3. Implemented V5 changes

- Replaced manual SKU typing with a product `QComboBox`.
- Product options are loaded from `marketing-content-os/schemas/sku_lookup_v1.tsv`.
- ComboBox display text uses the human-readable Thai product name plus SKU.
- ComboBox value is the canonical SKU used in the GPT1 prompt.
- Added a product detail card showing product name, SKU, grade band, difficulty, puzzle count, answer key status, and claim class.
- Added N preset buttons: `10`, `20`, `30`, `60`.
- Added a prominent `Next:` action banner.
- Added `Create/Open SKU Raw Folder`, which creates `_operator_workspace/<SKU>/raw` and opens it for the operator.
- Added `_operator_workspace/` to `.gitignore` because it contains local operator files and generated output.

## 4. Expected operator experience

The operator should now experience the workflow as:

```text
1. Choose product by readable name.
2. Choose N with presets or +/-.
3. Copy GPT1 prompt.
4. Paste into GPT1.
5. Save GPT1 output into the SKU raw folder.
6. Run pipeline.
7. Continue with generated GPT2 prompts.
```

The operator no longer needs to remember a SKU code or manually create a folder path.

## 5. Process engineering control

This change reduces variation at the input stage. It prevents SKU typos, improves product truth visibility, and keeps deterministic pipeline gates unchanged.

GPT1 remains the first generative step. The desktop app still performs deterministic cleansing, validation, selected row creation, GPT2 prompt file generation, and safe handoff gating. GPT2, image generation, and human review remain controlled downstream gates.

## 6. Review result

Operator Guided Mode V5 is a material usability improvement. The app now better follows the principle that users should choose from governed project truth instead of typing or remembering operational codes.
