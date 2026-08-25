# Parallel Workspace Pipeline Review

Status: DONE / IMPLEMENTED
Date: 2026-08-25
Scope: Desktop Social Content Pipeline

## 1. Request

The operator wants to select the parent `_operator_workspace` folder and have the program process every SKU child folder safely.

The operator also requested parallel processing.

## 2. Design decision

The app now supports these selections:

```text
_operator_workspace/
  BK-EL-MIX-EASY-01/
    raw/
      *.md / *.txt / *.text
  BK-EL-MIX-MEDIUM-01/
    raw/
      *.md / *.txt / *.text
```

When the selected folder contains child SKU folders, each SKU is treated as an independent job.

Outputs are no longer mixed into the root `_operator_workspace/_cleaned` folder. Each SKU writes to its own output root:

```text
_operator_workspace/<SKU>/_cleaned/
  clean/
  reports/
  selected/
  handoff/
  pipeline_batch_summary.json
```

A global run summary is written to:

```text
_operator_workspace/_workspace_parallel_summary.json
```

## 3. Parallel execution

Implementation uses `ThreadPoolExecutor`.

Each SKU folder is submitted as one independent job. The job calls the existing deterministic `clean_folder(...)` workflow with:

```text
input_folder = <SKU>/raw  or <SKU>
output_folder = <SKU>/_cleaned
expected_rows = N
target_posts = N
```

The operator can choose worker count from the UI:

```text
1, 2, 3, 4, 6, 8
```

The service caps workers to the number of discovered jobs and to a maximum of 8.

## 4. Pipeline alignment

The deterministic pipeline remains unchanged per SKU:

```text
GPT1 raw output
-> clean / validate
-> clean TSV
-> selected_<N>.tsv
-> N GPT2 prompt files
-> GPT2 prompt queue
```

The difference is that the app can now run this pipeline for many SKU workspaces in parallel.

## 5. UI changes

The launcher now opens:

```text
marketing-content-os/apps/social_pipeline_desktop/main_workspace_parallel.py
```

The UI focuses on:

- choosing `_operator_workspace` or one SKU folder;
- setting post count N;
- setting parallel worker count;
- running all discovered SKU jobs;
- showing one row per SKU;
- selecting a PASS SKU;
- showing its generated GPT2 prompt queue;
- copying GPT2 prompts one-by-one.

## 6. Safety controls

- Raw discovery ignores output folders such as `_cleaned`, `clean`, `reports`, `selected`, `handoff`, `images`, and `final`.
- Each SKU output is isolated under that SKU folder.
- A single run-wide N is still used, matching the Dynamic N contract.
- PASS SKU jobs expose generated GPT2 prompts.
- FAIL SKU jobs do not expose GPT2 prompt actions.

## 7. Review result

Backend pipeline: PASS

Parallel workspace discovery: PASS

Per-SKU output isolation: PASS

GPT2 prompt queue alignment: PASS

Known limitation: all raw files in one run use the same N. This follows the active Dynamic N Social Content Pipeline Contract. If mixed-N raw files are needed later, that must become a new documented contract before implementation.
