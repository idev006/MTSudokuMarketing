# Software Engineering Follow-ups — Done

Status: DONE
Date: 2026-08-25

## Objective

Complete the next engineering follow-ups identified after the Social Content Production Cockpit hardening pass, before the operator pulls the repository again.

## Completed Work

### 1. Automated tests for raw discovery hardening

Added:

```text
marketing-content-os/tests/test_pipeline_service.py
```

Coverage:

- `discover_raw_files()` accepts GPT1 raw `.md/.txt/.text` files.
- Generated/system folders are ignored:
  - `_cleaned/`
  - `_ready_for_gpt2/`
  - `_diagnostics/`
  - `_runs/`
  - `.git/`
  - `.venv/`
  - `__pycache__/`
- `validate_post_count()` enforces the supported `1..60` range.

### 2. Automated tests for failed-only rerun merge behavior

Added:

```text
marketing-content-os/tests/test_workspace_parallel_service.py
```

Coverage:

- A previous full summary containing both pass and fail SKU results is loaded.
- `run_mode="failed_only"` reruns only the failed SKU.
- The rerun result is merged back into the full workspace summary.
- The final summary still contains all SKUs instead of shrinking to only the rerun subset.

Expected behavior:

```text
before: 2 SKU / 1 pass / 1 fail
failed-only rerun processes only the failed SKU
final: 2 SKU / 2 pass / 0 fail
```

### 3. Workspace health-check command

Added:

```text
marketing-content-os/tools/workspace_health_check.py
marketing-content-os/tools/run_workspace_health_check.bat
```

The health checker validates the relationship between files on disk and `_workspace_parallel_summary.json`:

- actual SKU workspace count;
- actual raw GPT1 file count;
- actual `_ready_for_gpt2/*_gpt2_prompt.txt` count;
- per-SKU raw count;
- per-SKU ready prompt count;
- PASS SKU with missing ready prompts;
- stale output where raw is newer than ready GPT2 output.

It also computes a raw digest per SKU. If a previous `_workspace_health_check.json` exists, it flags raw files that changed since the last health check.

Usage:

```cmd
marketing-content-os\tools\run_workspace_health_check.bat
```

or with an explicit workspace:

```cmd
marketing-content-os\tools\run_workspace_health_check.bat F:\programming\GPT\MTSudokuMarketing\_operator_workspace
```

The command writes:

```text
_operator_workspace/_workspace_health_check.json
```

and exits with:

```text
0 = PASS
2 = FAIL
```

### 4. Test runner

Added:

```text
marketing-content-os/tools/run_desktop_pipeline_tests.bat
```

Usage:

```cmd
marketing-content-os\tools\run_desktop_pipeline_tests.bat
```

The test runner uses the repo `.venv` Python when available, otherwise falls back to `python`.

## Updated Engineering Process

The cockpit should now be operated with these checks:

```text
1. Run or rerun GPT1 validation from raw/
2. Confirm workspace summary in the UI
3. Run workspace health check
4. If health check PASS, proceed to GPT2 queue
5. If health check FAIL, inspect _workspace_health_check.json and rerun affected SKU(s)
```

## Acceptance Criteria

A healthy 24-SKU workspace should produce:

```text
_workspace_parallel_summary.json:
  job_count = 24
  pass_job_count = 24
  fail_job_count = 0
  raw_file_count = 24
  ready_prompt_file_count = 240

_workspace_health_check.json:
  health_status = PASS
  error_count = 0
```

## Pull-and-verify Commands

```cmd
cd /d F:\programming\GPT\MTSudokuMarketing
git pull origin main
marketing-content-os\tools\run_desktop_pipeline_tests.bat
marketing-content-os\tools\run_workspace_health_check.bat
marketing-content-os\tools\run_social_pipeline_desktop.bat
```

## Remaining Future Improvements

The core follow-ups are now implemented. Future improvements can focus on convenience rather than correctness:

1. show `_workspace_health_check.json` results directly inside the desktop UI;
2. add a one-click UI button for health check;
3. add raw digest directly into `_workspace_parallel_summary.json` on every run;
4. add publish-status tracking after GPT2 and image generation.
