# Desktop Social Content Pipeline — Process Engineering Design

Status: PILOT IMPLEMENTATION
Date: 2026-08-24
Scope: BiiigBee Sudoku Marketing social content production

## 1. Objective

Create a repeatable local desktop workflow that reduces operator complexity while preserving the approved GPT1 → Cleaner → GPT2 → Image → Human Review pipeline.

The app is designed for folder-level cleansing: the operator selects a folder, and the program cleans every supported raw GPT1 output file in that folder.

## 2. Design principles

1. Keep GPT count at 2:
   - GPT1: Campaign Content Generator.
   - GPT2: Visual Prompt Refiner.
2. Keep the Cleaner deterministic and local.
3. Treat raw GPT1 Markdown as evidence only.
4. Treat clean validated TSV as the operational handoff artifact.
5. Use Arabic numerals in UI, filenames, logs, status values, and process steps.
6. Avoid OS-specific application logic. Use `pathlib`, Python, and Qt services.
7. Make every stage observable: input, output, report, pass/fail, and next action.

## 3. SIPOC

| SIPOC | Definition |
|---|---|
| Supplier | Human operator, GPT1 Campaign Content Generator |
| Input | Folder of raw `.md`, `.txt`, `.text` GPT1 outputs |
| Process | Discover files → clean rows → validate TSV → write reports → surface next action |
| Output | Clean TSV files, JSON reports, PASS/FAIL table, GPT2 handoff prompt |
| Customer | Human operator, GPT2 Visual Prompt Refiner, social post production process |

## 4. Process map

```text
1. Prepare raw GPT1 files
2. Select folder in desktop app
3. Run folder-level cleansing
4. For each file:
   4.1 Extract canonical ROW-* records
   4.2 Write clean TSV
   4.3 Run deterministic validator
   4.4 Write JSON report
   4.5 Mark PASS or FAIL
5. Operator selects PASS file
6. Operator selects 5 best rows per SKU
7. Operator sends one clean row at a time to GPT2
8. GPT2 returns final copy + image-generation handoff
9. Image generated
10. Human review before publish
```

## 5. Stage gates

| Gate | Name | Pass condition | Failure action |
|---|---|---|---|
| G1 | Input folder selected | Folder exists | Select valid folder |
| G2 | Raw files found | At least 1 `.md`, `.txt`, or `.text` file | Add GPT1 raw output files |
| G3 | Extraction | Expected row count found | Open report / rerun GPT1 |
| G4 | Validation | Validator exit code is `0` | Do not send to GPT2 |
| G5 | GPT2 handoff | Only clean validated row used | Reject raw Markdown handoff |
| G6 | Publish | Human review approved | Do not publish |

## 6. Error-proofing

- The app ignores output folders such as `_cleaned`, `clean`, `reports`, `selected`, `handoff`, `images`, and `final` during raw file discovery.
- The app writes clean files and reports into `_cleaned` under the selected folder by default.
- The app shows `PASS` or `FAIL` per file.
- The app blocks GPT2 prompt copy for failed files.
- The app uses the existing deterministic cleaner and validator rather than reimplementing validation rules.

## 7. Standard folder output

For a selected folder:

```text
selected-folder/
  raw_file_1.md
  raw_file_2.md
  _cleaned/
    clean/
      raw_file_1_clean.tsv
      raw_file_2_clean.tsv
    reports/
      raw_file_1_clean_report.json
      raw_file_2_clean_report.json
```

## 8. Operator experience

The intended operator flow is:

```text
1. Choose Folder
2. Clean All Files
3. Review PASS/FAIL table
4. Open clean TSV
5. Select 5 rows
6. Copy GPT2 prompt
7. Continue in GPT2
```

## 9. KPI impact

This tool directly supports:

- cleaner execution time reduction;
- fewer command-line errors;
- higher clean handoff compliance;
- faster row selection;
- fewer accidental raw Markdown handoffs to GPT2.

## 10. Non-goals

This version does not auto-publish social posts.
This version does not call GPT1 or GPT2 automatically.
This version does not generate images automatically.
This version does not replace human review.

## 11. Implementation files

```text
requirements.txt
marketing-content-os/apps/social_pipeline_desktop/main.py
marketing-content-os/apps/social_pipeline_desktop/pipeline_service.py
marketing-content-os/apps/social_pipeline_desktop/README.md
marketing-content-os/tools/run_social_pipeline_desktop.bat
```
