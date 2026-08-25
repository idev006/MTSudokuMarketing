# Idempotent Rerun and Auto-fix Process — Done

Status: DONE
Date: 2026-08-25

## Objective

Prevent recoverable GPT1 formatting defects from blocking production and make repeated workspace checks safe, explainable, and non-destructive.

## Problem Observed

A batch run over `_operator_workspace` processed 24 SKU workspaces. The pipeline passed 23 jobs and failed 1 job. Diagnostic review found that the failing SKU had 10 extracted rows, but validation failed because one controlled-vocabulary value had leading whitespace:

```text
OBJECTIVE=' CREATE_ENGAGEMENT'
```

This is a recoverable formatting defect. It should not require the operator to regenerate GPT1 output.

## Process Design

The GPT1 validation process now follows this sequence:

```text
GPT1 raw output
  ↓
archive/preserve raw source
  ↓
extract canonical TSV rows
  ↓
safe whitespace normalizer
  ↓
write clean TSV
  ↓
deterministic validator
  ↓
classified result and diagnosis
  ↓
GPT2-ready package generation
```

## Implemented Controls

### 1. Safe whitespace auto-fix

`clean_validate_campaign_markdown.py` now applies conservative normalization before validation:

- trims leading/trailing whitespace around each TSV field;
- preserves internal copy text and product claims;
- does not map taxonomy values semantically;
- does not infer missing fields;
- logs every fix in the report.

A field such as:

```text
 CREATE_ENGAGEMENT
```

is normalized to:

```text
CREATE_ENGAGEMENT
```

and the report records the exact row, field, before value, after value, and fix type.

### 2. PASS_WITH_AUTOFIX

When validation passes after safe normalization, the report result becomes:

```text
PASS_WITH_AUTOFIX
```

The process still exits with code 0 because production can continue safely.

### 3. Workspace diagnosis

`workspace_parallel_service.py` now reads per-file cleaner reports and writes human-readable diagnosis data to `_workspace_parallel_summary.json`, including:

- `result_label`
- `auto_fix_count`
- `diagnosis`
- `next_action`
- non-empty `error_message` for failures

### 4. Idempotent rerun support

`process_workspace_parallel()` now accepts:

```python
run_mode="all"
run_mode="failed_only"
```

The default remains `all` for backward compatibility. `failed_only` uses the previous `_workspace_parallel_summary.json` to rerun only SKU workspaces that previously failed.

### 5. Safe generated-output cleanup

A new backend function is available:

```python
cleanup_generated_outputs(selected_root)
```

It deletes only generated outputs:

```text
_cleaned/
_ready_for_gpt2/
_workspace_parallel_summary.json
```

It preserves:

```text
raw/
GPT1_REQUEST.txt
```

### 6. Diagnostic ZIP export

A new backend function is available:

```python
export_diagnostic_zip(selected_root, sku=None)
```

It exports a compact diagnostic bundle containing raw source files, cleaner reports, batch summaries, and GPT2-ready indexes when available.

## Expected Result

The previously observed whitespace-only defect should no longer produce a production-blocking fail. Expected rerun outcome for that batch after this change:

```text
24 pass jobs
0 fail jobs
240 GPT2-ready prompts
```

If a real schema, taxonomy, product-truth, or claim-safety issue remains, the workspace summary should now report a human-readable diagnosis instead of an empty error message.

## Follow-up UI Work

Backend support is in place. The next UI pass should add buttons for:

- rerun failed only;
- safe cleanup generated outputs only;
- export diagnostic ZIP;
- show PASS_WITH_AUTOFIX count in dashboard;
- show diagnosis and next action in the SKU results table.
