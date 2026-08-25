# Dynamic N Social Content Pipeline Contract

Status: ACTIVE / MANDATORY
Date: 2026-08-25
Scope: BiiigBee Sudoku Marketing social content production desktop pipeline

## 1. Purpose

This document is the source of truth for the desktop social content pipeline when the operator wants to produce a configurable number of social media content items per SKU.

The project is document-driven. Implementation must follow this document.

## 2. Non-negotiable rule

The operator may choose a post count `N` where:

```text
1 <= N <= 60
```

For each SKU/file run:

```text
GPT1 NUMBER_OF_ROWS=N
Desktop app expected rows=N
Desktop app selected rows target=N
Desktop app GPT2 prompt files target=N
```

The app must not silently change `N`.

## 3. Process map

```text
1. Operator chooses N where 1 <= N <= 60
2. Operator runs GPT1 with NUMBER_OF_ROWS=N
3. Operator saves GPT1 raw output as .md / .txt / .text
4. Desktop app discovers raw files in selected folder
5. Desktop app runs cleaner and validator using expected_rows=N
6. PASS files produce clean TSV
7. PASS files produce selected_<N>.tsv
8. PASS files produce N GPT2 TEMPLATE_HANDOFF prompt files when N rows are available
9. Operator sends prompt files to GPT2
10. GPT2 output goes to image generation and human review
11. Approved result becomes post-ready package
```

## 4. SIPOC

| Element | Definition |
|---|---|
| Supplier | GPT1 Campaign Content Generator, human operator |
| Input | `N`, SKU, GPT1 raw output files |
| Process | discover raw files -> clean -> validate -> select N rows -> generate N prompts -> guide next action |
| Output | clean TSV, report JSON, selected N-row TSV, GPT2 prompt files, handoff index, batch summary |
| Customer | operator, GPT2 Visual Prompt Refiner, image-generation workflow, social content production |

## 5. Stage gates

| Gate | Pass condition | Failure action |
|---|---|---|
| G1 N selected | `1 <= N <= 60` | block run and ask for valid N |
| G2 GPT1 raw files found | at least 1 `.md`, `.txt`, or `.text` file | ask operator to add raw GPT1 output files |
| G3 Row extraction | cleaner extracts canonical rows | open report / rerun GPT1 |
| G4 Row count | extracted row count matches N | do not send to GPT2 |
| G5 Deterministic validation | validator exit code `0` | do not send to GPT2 |
| G6 N prompt generation | prompt files created from PASS clean rows | inspect clean TSV / selected TSV |
| G7 Human review | copy/image approved by reviewer | do not publish |

## 6. Output contract

For each selected folder, the app creates:

```text
_cleaned/
  clean/
    <raw_file>_clean.tsv
  reports/
    <raw_file>_clean_report.json
  selected/
    <raw_file>_selected_<N>.tsv
  handoff/
    <raw_file>/
      01_<ROW_ID>_gpt2_prompt.txt
      ...
      NN_<ROW_ID>_gpt2_prompt.txt
    <raw_file>_handoff_index.tsv
  pipeline_batch_summary.json
```

`NN` is the 2-digit or wider ordered prompt number where possible. For `N <= 60`, two digits are sufficient.

## 7. Downstream usability requirements

The output must be correct, efficient, and easy to continue:

- The clean TSV must remain the operational handoff artifact.
- The report JSON must make failures diagnosable.
- The selected TSV must contain the exact rows that prompt files use.
- Each GPT2 prompt file must contain exactly one `MODE: TEMPLATE_HANDOFF` request and one complete clean TSV row.
- The handoff index must list prompt order, `ROW_ID`, `SKU`, `VISUAL_TYPE`, prompt path, and next action.
- The batch summary must include input folder, output folder, raw count, PASS count, FAIL count, target N, selected row count, prompt count, and output paths.

## 8. UX requirements

The operator should not need to understand internal TSV rules.

The visible user journey is:

```text
1. Set N
2. Copy/run GPT1 prompt skeleton
3. Save GPT1 raw output files
4. Choose folder
5. Clean All Files + Prepare N GPT2 Prompts
6. Copy/open GPT2 prompts
```

The app must always answer:

```text
What should I do now?
```

## 9. Automation boundary

The app automates deterministic work:

- folder discovery;
- raw file discovery;
- clean TSV creation;
- validator execution;
- PASS / FAIL classification;
- selected N-row TSV creation;
- GPT2 prompt file generation;
- handoff index generation;
- batch summary generation;
- next-action guidance.

The app does not automate judgment-heavy work:

- generating GPT1 ideas;
- GPT2 visual review/refinement;
- final copy approval;
- image quality approval;
- publishing.

## 10. Global production planning note

If the catalog has `24` SKUs, total post target is:

```text
24 * N post packages
```

Examples:

```text
N=10 -> 240 post packages
N=20 -> 480 post packages
N=60 -> 1440 post packages
```

This contract controls the local deterministic handoff workflow only. It does not remove the need for GPT2 and human review.
