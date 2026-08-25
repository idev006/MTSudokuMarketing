# BiiigBee Social Content Pipeline Desktop App

Status: PILOT TOOL

This PySide6 desktop app is a local operator cockpit for the BiiigBee Sudoku Marketing pipeline.

It is not a GPT. It supports the process between GPT1 and GPT2.

## UX goal

The operator should not need to remember the pipeline.

The app should:

- show the current stage;
- explain the next action in one coach card;
- keep advanced options hidden by default;
- use one obvious primary button per stage;
- auto-select the first `PASS` file after cleansing;
- prepare a GPT2 `MODE: TEMPLATE_HANDOFF` prompt with one click;
- never allow a `FAIL` file to be treated as GPT2-ready.

## Purpose

The app lets an operator select one folder containing raw GPT1 output files and clean/validate every supported file in that folder.

Supported input file types:

```text
.md
.txt
.text
```

For each raw input file, the app creates:

```text
<selected-folder>/_cleaned/clean/<raw_file_name>_clean.tsv
<selected-folder>/_cleaned/reports/<raw_file_name>_clean_report.json
```

## Process engineering pipeline

```text
1. GPT1 raw output files
2. Folder-level deterministic cleansing
3. Clean TSV validation gate
4. Select 5 best rows per SKU
5. GPT2 TEMPLATE_HANDOFF
6. Image generation
7. Human review
8. Post-ready package
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
5. Click `2. Clean All Files`.
6. The app runs folder-level deterministic cleansing.
7. The app shows `PASS`, `FAIL`, row count, and next action.
8. Select a `PASS` file.
9. Click `3. Copy GPT2 Prompt from Selected PASS File`.
10. Paste into GPT2.

## Guided UI behavior

The app has a top coach card. It always tells the operator what to do now.

The expected rows setting defaults to `10`, because the normal production pattern is GPT1 creates `10` rows so the operator can select the best `5` rows.

Advanced concentration options are hidden by default. They should be used only when a reviewer explicitly approves an override.

## Rules

- Raw GPT1 output is evidence only.
- Clean validated TSV is the operational handoff artifact.
- Do not send FAIL rows to GPT2.
- Do not publish without human review.
- Use Arabic numerals in UI, filenames, reports, and operational status values.
