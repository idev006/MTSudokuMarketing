# Generated Output Rebuild Before Rerun — Done

Status: DONE
Date: 2026-08-25

## Objective

Make reruns deterministic and prevent stale generated artifacts from surviving a second validation run.

## Problem

The operator correctly identified that when a SKU is processed again, generated folders should not merely be overwritten partially. If `_cleaned/` or `_ready_for_gpt2/` contains files from a previous run, stale files can remain when:

- raw filenames change;
- prompt counts change;
- a previously passing SKU later fails;
- a run is interrupted;
- failed-only rerun processes only a subset of SKU workspaces.

In production, this could make the UI or summary show old GPT2-ready files that no longer correspond to the current raw validation result.

## Implemented Behavior

For every SKU job that is actually processed, the desktop backend now clears generated outputs first:

```text
<SKU>/_cleaned/
<SKU>/_ready_for_gpt2/
```

Then it rebuilds outputs from the preserved source:

```text
<SKU>/raw/
```

The backend never deletes:

```text
<SKU>/raw/
<SKU>/GPT1_REQUEST.txt
```

## Mode Behavior

### Full rerun

`run_mode="all"` clears and rebuilds generated outputs for every discovered SKU workspace.

### Failed-only rerun

`run_mode="failed_only"` clears and rebuilds generated outputs only for SKU workspaces that were selected for rerun, then merges those fresh results back into the previous full workspace summary.

Previously passing SKU workspaces are not touched during failed-only rerun.

## Safety Outcome

- No stale `_cleaned/` output remains for a processed SKU.
- No stale `_ready_for_gpt2/` package remains when a processed SKU fails.
- Raw GPT1 source files remain preserved.
- Full reruns are deterministic rebuilds from raw.
- Failed-only reruns are targeted rebuilds plus full-summary merge.
