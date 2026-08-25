# BiiigBee Social Content Pipeline Desktop App

Status: PILOT TOOL V3 — DOCUMENT-DRIVEN N WORKFLOW

This PySide6 desktop app is a local operator cockpit for the BiiigBee Sudoku Marketing pipeline.

It is not a GPT. It supports the process after GPT1 and before GPT2. It manages deterministic workflow so the operator does not need to understand TSV internals.

## Document-driven rule

This app must follow the project documents.

The controlling workflow rule is:

```text
1 <= N <= 60
GPT1 creates NUMBER_OF_ROWS=N
Desktop app validates N rows
Desktop app prepares N selected rows
Desktop app generates N GPT2 prompts
```

If code and documentation disagree, documentation must be updated first and code must be changed to follow the approved document.

## UX goal

The operator should not need to remember the pipeline.

The app should answer one question at all times:

```text
What should I do now?
```

The app does this by:

- showing a guided flow;
- using one coach card as the primary navigation instruction;
- letting the operator set `N` from `1` to `60`;
- showing the exact GPT1 prompt skeleton using `NUMBER_OF_ROWS=N`;
- hiding advanced options by default;
- disabling unsafe buttons until the file is ready;
- running folder-level cleansing for all raw files;
- generating clean TSV, reports, selected N-row TSV, and GPT2 prompt files;
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
<selected-folder>/_cleaned/selected/<raw_file_name>_selected_<N>.tsv
<selected-folder>/_cleaned/handoff/<raw_file_name>/<order>_<ROW_ID>_gpt2_prompt.txt
<selected-folder>/_cleaned/handoff/<raw_file_name>_handoff_index.tsv
<selected-folder>/_cleaned/pipeline_batch_summary.json
```

## Process engineering pipeline

```text
1. Operator chooses N where 1 <= N <= 60
2. GPT1 creates NUMBER_OF_ROWS=N raw output
3. Operator saves GPT1 output as .md / .txt / .text
4. Desktop app discovers all raw files in selected folder
5. Desktop app cleans and validates exactly N rows per file
6. Desktop app prepares N selected rows per PASS file
7. Desktop app generates N GPT2 TEMPLATE_HANDOFF prompt files
8. Operator pastes prompt files into GPT2
9. Image generation
10. Human review
11. Post-ready package
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

1. Set `Post count N` in the app. Default is `10`.
2. Use the GPT1 prompt skeleton shown in the app.
3. In GPT1, replace `<SKU>` and run the request.
4. Save GPT1 raw output as `.md` or `.txt` in one folder.
5. Click `1. Choose Folder`.
6. Click `2. Clean All Files + Prepare N GPT2 Prompts`.
7. The app runs cleansing, validation, selected-row generation, prompt generation, and summary generation.
8. The app shows `PASS`, `FAIL`, row count, selected row count, GPT2 prompt count, and next action.
9. Select a `PASS` file, or use the first auto-selected `PASS` file.
10. Click `3. Copy First GPT2 Prompt` or open the GPT2 prompts folder.
11. Paste prompts into GPT2 Visual Prompt Refiner.
12. Use GPT2 output for image generation and human review.

## Output quality rules

Output must be easy to use downstream:

- clean TSV contains only validated canonical rows;
- report JSON explains validation outcome;
- selected TSV contains exactly the rows prepared for GPT2 when available;
- GPT2 prompt files are one prompt per file;
- handoff index lists prompt order, ROW_ID, SKU, VISUAL_TYPE, prompt path, and next action;
- batch summary gives run-level PASS / FAIL and file paths.

## What the app handles for the operator

- N setting from `1` to `60`.
- GPT1 prompt skeleton.
- Folder discovery.
- Raw file discovery.
- Batch cleansing.
- Validator execution.
- PASS / FAIL classification.
- Clean TSV generation.
- Report JSON generation.
- Selected N-row TSV generation.
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
