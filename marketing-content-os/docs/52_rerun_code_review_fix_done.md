# Rerun Code Review Fix — Done

Status: DONE
Date: 2026-08-25

## Review Context

After the desktop UI exposed two GPT1 validation modes:

1. ตรวจใหม่ทั้งหมดจาก raw เดิม
2. ตรวจซ้ำเฉพาะที่ไม่ผ่าน

we reviewed the backend behavior behind `run_mode="failed_only"`.

## Issue Found

The backend already supported `failed_only`, but the first implementation processed only the previously failing SKU workspaces and then wrote a new `_workspace_parallel_summary.json` containing only those rerun jobs.

That behavior was technically functional, but it was not correct for operator workflow because a second-run summary should still represent the whole production workspace, not only the subset that was rerun.

Example risk:

```text
Previous full run: 24 SKU, 23 pass, 1 fail
Failed-only rerun: 1 SKU rerun and pass
Wrong summary risk: 1 SKU, 1 pass, 0 fail
Correct summary: 24 SKU, 24 pass, 0 fail
```

## Fix Implemented

`workspace_parallel_service.py` now treats failed-only reruns as an idempotent workspace update:

```text
read previous workspace summary
  ↓
identify previously failed SKUs
  ↓
rerun only those failed SKUs
  ↓
merge new rerun results back into the previous full result set
  ↓
write a new full workspace summary
```

## Additional Hardening

The code review also hardened selected-folder handling:

- if the operator selects a `raw/` folder, summaries and diagnostics now resolve to the SKU workspace root instead of being written inside `raw/`;
- diagnostic ZIP arc names now use safe relative names even when files are outside the selected folder boundary;
- if `failed_only` is used when nothing previously failed, the backend returns the previous full summary instead of destroying the operator's full dashboard context;
- if no previous summary exists, `failed_only` now gives a clear instruction to run the full validation first.

## Expected Behavior

### Full rerun

```text
run_mode="all"
```

Processes every discovered raw workspace and writes a full summary.

### Failed-only rerun

```text
run_mode="failed_only"
```

Processes only previously failed workspaces, then writes a merged full summary that preserves all previous passing workspaces.

### No failed workspaces

If the previous summary already has 0 failed workspaces, failed-only rerun returns the existing full workspace summary with a new run id, instead of failing or replacing the summary with an empty result set.

## Files Changed

- `marketing-content-os/apps/social_pipeline_desktop/workspace_parallel_service.py`

## Commit

- `df6b51dc9a380258f2051f5666a9c274192cd4d5` — `app: make failed-only reruns preserve full workspace summary`
