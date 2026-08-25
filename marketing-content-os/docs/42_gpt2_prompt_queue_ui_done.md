# GPT2 Prompt Queue UI Completion Review

Status: DONE
Date: 2026-08-25
Scope: Desktop social content pipeline UI / Step 4 handoff

## 1. Improvement plan

The previous desktop UI backend followed the Dynamic N Social Content Pipeline Contract, but Step 4 displayed selected TSV rows too prominently. That caused operator confusion because the visible task at Step 4 is not to read TSV data; the task is to copy generated GPT2 TEMPLATE_HANDOFF prompts into GPT2 one at a time.

Planned improvement:

1. Keep deterministic backend unchanged.
2. Add a GPT2 prompt queue UI.
3. Show generated prompt files as human-readable items.
4. Show the selected prompt content in a preview pane.
5. Provide explicit actions: copy selected prompt, copy first prompt, next prompt, open prompt folder.
6. Keep selected TSV and clean TSV available as secondary evidence buttons only.
7. Preserve PathManager-relative icon/path handling.

## 2. Implementation summary

Added:

```text
marketing-content-os/apps/social_pipeline_desktop/main_queue.py
```

Updated launcher:

```text
marketing-content-os/tools/run_social_pipeline_desktop.bat
```

The launcher now opens `main_queue.py`.

## 3. Pipeline alignment review

| Pipeline requirement | Result |
|---|---|
| User sets `N` where `1 <= N <= 60` | PASS |
| GPT1 prompt uses `NUMBER_OF_ROWS=N` | PASS |
| App cleans and validates raw GPT1 files | PASS |
| PASS files generate clean TSV | PASS |
| PASS files generate selected N-row TSV | PASS |
| PASS files generate GPT2 prompt files | PASS |
| Step 4 guides operator to GPT2 prompt files | PASS |
| TSV rows hidden from default primary task | PASS |
| Human review remains required | PASS |

## 4. UX review

Before:

```text
Step 4 showed long TSV rows, making the operator ask: what should I copy?
```

After:

```text
Step 4 shows a prompt queue:
- left side: ordered GPT2 prompt list
- right side: selected prompt content
- buttons: copy selected, copy first, next, open prompt folder
```

This better matches the actual work:

```text
PASS clean TSV -> generated GPT2 prompts -> operator copies prompt into GPT2
```

## 5. Remaining notes

The app still does not call GPT2 automatically. This is intentional because GPT2 output and final image/copy quality remain judgment-heavy gates requiring operator and human review.
