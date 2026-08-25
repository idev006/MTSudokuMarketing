# Desktop Pipeline UI/UX Review

Status: ACTIVE UX REVIEW
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## 1. Review role

This review is written from the perspective of a UI/UX Designer supporting a document-driven, process-engineered production workflow.

The app is not only a Python tool. It is the operator cockpit for moving GPT1 raw output into clean, validated, GPT2-ready handoff files.

## 2. User request

The user requested:

- panels that let the operator resize the window and working areas;
- easier UI/UX;
- lower cognitive load;
- output that remains correct, efficient, and easy to continue downstream.

## 3. Screenshot review findings

The prior UI had the correct workflow logic, but the layout created avoidable operator friction:

| Area | Finding | UX risk |
|---|---|---|
| Top workflow | Steps were visible but occupied a full-width strip | OK, but needed stronger panel separation |
| Setup area | N input, GPT1 prompt, folder, and buttons were visually crowded | User may not know where to start |
| Empty space | Large blank regions appeared before results existed | Feels unfinished and wastes vertical space |
| Results/preview | Table and preview had fixed-feeling proportions | User cannot resize based on task |
| Actions | Some actions were visible before useful context existed | More cognitive load |
| Window resizing | Layout did not expose clear resizable work panels | User has less control on different monitors |

## 4. UX design decision

The app should use a panel-based cockpit:

```text
Header + stage flow
Resizable top splitter:
  Left panel: Setup
  Right panel: Workflow coach + metrics
Resizable middle panel:
  Batch results table
Resizable bottom panel:
  Selected rows, prompt preview, and actions
```

This design keeps the main user journey visible while letting the operator resize work areas depending on the current task.

## 5. Implemented UI/UX changes

- Rebuilt the main window around `QSplitter` panels.
- Added a horizontal splitter between Setup and Workflow Coach.
- Added a vertical splitter between top workflow, results table, and preview/action panel.
- Wrapped top panels in scroll areas so smaller screens remain usable.
- Moved actions into the bottom output panel where they belong contextually.
- Improved table column behavior with `QHeaderView` sizing.
- Kept one primary action button: `Clean All Files + Prepare N GPT2 Prompts`.
- Preserved safe gating: GPT2 actions remain disabled until a PASS result is selected.
- Preserved dynamic N flow: `1 <= N <= 60`.

## 6. Updated layout contract

The UI should communicate the workflow as:

```text
1. Setup N and GPT1 prompt
2. Choose raw folder
3. Clean + validate
4. Use generated GPT2 prompts
5. Image generation + human review
```

The UI must continue to answer:

```text
What should I do now?
```

## 7. Expected operator feeling

The intended operator feeling is:

```text
I can see the process.
I can resize the work areas.
I know where to start.
I know which files passed.
I know what to copy into GPT2.
The program prevents unsafe handoff.
```

## 8. Review result

The updated UI is better aligned with the project's Level 3 operator-cockpit goal.

The app now supports:

- resizable panels;
- clearer setup vs. status separation;
- better table and output visibility;
- lower cognitive load;
- more professional workflow control;
- continued document-driven process compliance.

## 9. Remaining improvement backlog

These are not blockers, but are good next UX upgrades:

1. Add persistent window geometry and splitter positions.
2. Add a compact mode for laptop screens.
3. Add a paste-from-clipboard raw capture helper.
4. Add SKU auto-detection summary from clean rows.
5. Add batch progress per file instead of only final summary.
6. Add a dedicated post-package tracker view after GPT2 completion.
