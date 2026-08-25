# GPT2-Ready Package Review

Status: DONE
Date: 2026-08-25
Scope: Desktop social content pipeline, parallel workspace mode

## Request

The operator asked whether the program can organize files so they are ready to send to GPT2, then asked to proceed.

## Design decision

The canonical deterministic output remains under each SKU workspace's `_cleaned/` folder:

```text
<SKU>/
  _cleaned/
    clean/
    reports/
    selected/
    handoff/
```

For operator convenience, every PASS SKU now also gets a human-friendly package:

```text
<SKU>/
  _ready_for_gpt2/
    README_วิธีใช้.txt
    _gpt2_ready_index.tsv
    01_gpt2_prompt.txt
    02_gpt2_prompt.txt
    ...
```

The operator should use `_ready_for_gpt2/*.txt` as the primary files to copy into GPT2.

## Why this improves the workflow

Before this change, users had to know that GPT2 prompt files lived inside `_cleaned/handoff/<raw_file>/`. That folder is correct for system traceability, but it is not the easiest place for a non-technical operator.

After this change, the operator only needs to open:

```text
<SKU>/_ready_for_gpt2/
```

Then copy files in numeric order.

## Pipeline alignment

This change does not replace the clean TSV, report JSON, selected TSV, handoff folder, or batch summaries. It adds an operator-facing copy package after a SKU passes deterministic validation.

The updated flow is:

```text
GPT1 raw output
-> clean / validate
-> PASS clean TSV
-> selected_N.tsv
-> canonical GPT2 handoff files
-> operator-facing _ready_for_gpt2 package
-> GPT2 Visual Prompt Refiner
-> image generation and human review
```

## Output contract added

For every PASS SKU folder:

```text
_ready_for_gpt2/
  README_วิธีใช้.txt
  _gpt2_ready_index.tsv
  01_gpt2_prompt.txt
  02_gpt2_prompt.txt
  ...
```

Rules:

- The folder is recreated on each successful run to avoid stale prompt files.
- Only PASS prompt files are copied into `_ready_for_gpt2`.
- Files are renumbered in a simple operator sequence: `01`, `02`, `03`, ...
- The index keeps the relationship between the ready prompt file and the original canonical prompt file.
- The workspace parallel summary includes `ready_gpt2_dir` and `ready_prompt_count` for each SKU.

## Review

| Area | Result |
|---|---|
| Keeps canonical `_cleaned` outputs | PASS |
| Adds easier operator-facing GPT2 files | PASS |
| Avoids cross-SKU mixing | PASS |
| Works with parallel SKU processing | PASS |
| Keeps N contract unchanged | PASS |
| Uses relative per-SKU package paths in the index where possible | PASS |

## Operator instruction

After a run, open a SKU folder and use:

```text
_ready_for_gpt2/01_gpt2_prompt.txt
_ready_for_gpt2/02_gpt2_prompt.txt
...
```

Copy each file's whole content into GPT2, one at a time.
