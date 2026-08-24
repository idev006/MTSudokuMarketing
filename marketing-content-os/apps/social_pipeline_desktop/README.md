# BiiigBee Social Content Pipeline Desktop App

Status: PILOT TOOL

This PySide6 desktop app is a local operator tool for the BiiigBee Sudoku Marketing pipeline.

It is not a GPT. It supports the process between GPT1 and GPT2.

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

From repository root:

```cmd
python -m marketing-content-os.apps.social_pipeline_desktop.main
```

If the `marketing-content-os` hyphen causes module-launch issues in an environment, use direct file launch:

```cmd
python marketing-content-os\apps\social_pipeline_desktop\main.py
```

## Operator steps

1. Put GPT1 raw output files in one folder.
2. Open the app.
3. Click `1. Choose Folder`.
4. Set expected rows per file, usually `10`.
5. Click `2. Clean All Files`.
6. If a file returns `PASS`, open the clean TSV and select 5 rows.
7. Use `3. Copy First Row GPT2 Prompt` as a helper for the first row.
8. Continue in GPT2 with `MODE: TEMPLATE_HANDOFF`.

## Rules

- Raw GPT1 output is evidence only.
- Clean validated TSV is the operational handoff artifact.
- Do not send FAIL rows to GPT2.
- Do not publish without human review.
- Use Arabic numerals in UI, filenames, reports, and operational status values.
