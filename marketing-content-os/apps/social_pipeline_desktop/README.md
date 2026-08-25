# BiiigBee Social Content Pipeline Desktop App

Status: PILOT TOOL V2

This PySide6 desktop app is a local operator cockpit for the BiiigBee Sudoku Marketing pipeline.

It is not a GPT. It supports the process between GPT1 and GPT2 and manages as much deterministic workflow as possible for the operator.

## UX goal

The operator should not need to remember the pipeline.

The app should answer one question at all times:

```text
What should I do now?
```

The app does this by:

- showing a 5-stage guided flow;
- using one coach card as the primary navigation instruction;
- hiding advanced options by default;
- disabling unsafe buttons until the file is ready;
- running folder-level cleansing for all raw files;
- automatically selecting 5 recommended rows per passing SKU file;
- automatically generating GPT2 `MODE: TEMPLATE_HANDOFF` prompt files;
- auto-selecting the first `PASS` file after processing;
- blocking failed files from GPT2 handoff.

## Purpose

The app lets an operator select one folder containing raw GPT1 output files and process every supported file in that folder.

Supported input file types:

```text
.md
.txt
.text
```

For each raw input file, the app creates a full `_cleaned` workspace:

```text
<selected-folder>/_cleaned/clean/<raw_file_name>_clean.tsv
<selected-folder>/_cleaned/reports/<raw_file_name>_clean_report.json
<selected-folder>/_cleaned/selected/<raw_file_name>_selected_5.tsv
<selected-folder>/_cleaned/handoff/<raw_file_name>/<order>_<ROW_ID>_gpt2_prompt.txt
<selected-folder>/_cleaned/handoff/<raw_file_name>_handoff_index.tsv
<selected-folder>/_cleaned/pipeline_batch_summary.json
```

## Process engineering pipeline

```text
1. GPT1 raw output files
2. Folder-level deterministic cleansing
3. Clean TSV validation gate
4. Auto-select 5 recommended rows per PASS file
5. Auto-generate GPT2 TEMPLATE_HANDOFF prompts
6. Operator pastes prompts into GPT2
7. Image generation
8. Human review
9. Post-ready package
```

## Install

From repository root:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Recommended launcher from repository root:

```cmd
marketing-content-os\tools\run_social_pipeline_desktop.bat
```

Direct file launch also works:

```cmd
.venv\Scripts\python.exe marketing-content-os\apps\social_pipeline_desktop\main.py
```

## Operator flow

1. Put GPT1 raw output files in one folder.
2. Open the app.
3. Click `1. Choose Folder`.
4. The app counts raw files and tells the operator whether it is ready.
5. Click `2. Clean All Files + Prepare GPT2 Prompts`.
6. The app runs cleansing, validation, selected-row generation, prompt generation, and summary generation.
7. The app shows `PASS`, `FAIL`, row count, selected row count, GPT2 prompt count, and next action.
8. Select a `PASS` file, or use the first auto-selected `PASS` file.
9. Click `3. Copy First GPT2 Prompt`.
10. Paste into GPT2 Visual Prompt Refiner.
11. Use GPT2 output for image generation and human review.

## Guided UI behavior

The app has a top coach card. It always tells the operator what to do now.

The expected rows setting defaults to `10`, because the normal production pattern is GPT1 creates `10` rows so the system can select a balanced `5` rows.

Advanced concentration options are hidden by default. They should be used only when a reviewer explicitly approves an override.

## What the app now handles for the operator

- Folder discovery.
- Raw file discovery.
- Batch cleansing.
- Validator execution.
- PASS / FAIL classification.
- Clean TSV generation.
- Report JSON generation.
- Recommended 5-row selection.
- GPT2 prompt file generation.
- Batch summary generation.
- Next-action navigation.

## What still requires human control

- Running GPT1.
- Running GPT2.
- Final claim-safety and visual review.
- Image generation review.
- Publishing approval.

## Rules

- Raw GPT1 output is evidence only.
- Clean validated TSV is the operational handoff artifact.
- Do not send FAIL rows to GPT2.
- Do not publish without human review.
- Use Arabic numerals in UI, filenames, reports, and operational status values.
