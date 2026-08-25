# Desktop Pipeline UI Polish — Path Manager + SVG Icons Done

Status: DONE
Date: 2026-08-25

## Goal
Improve the desktop app controls so non-technical users see polished, readable controls while the code avoids OS-specific hard-coded paths.

## Kanban Summary

| Lane | Work Item | Status |
|---|---|---|
| Backlog | Fix checkbox hover disappearance | DONE |
| Backlog | Replace CSS triangle arrows with graphics | DONE |
| Backlog | Add relative path manager for UI assets | DONE |
| Backlog | Improve plus/minus stepper buttons | DONE |
| Backlog | Keep plain-language labels in visible UI | DONE |
| Review | Check that internal GPT tokens remain hidden in dropdown labels | DONE |

## Implementation

### Path Manager
Added `PathManager` in `marketing-content-os/apps/social_pipeline_desktop/main.py`.

All app paths now start from `Path(__file__).resolve().parent` and resolve relative to the repository layout:

- app directory
- Marketing Content OS root
- repository root
- SKU lookup file
- operator workspace
- UI icon directory

This avoids drive-specific paths such as `D:\...` or assumptions tied to one Windows machine.

### SVG Icons
Added UI assets under:

```text
marketing-content-os/apps/social_pipeline_desktop/assets/icons/
```

Files:

```text
chevron-down.svg
check.svg
plus.svg
minus.svg
```

Usage:

- `chevron-down.svg` for combobox dropdown arrows through QSS
- `check.svg` for checkbox checked state through QSS
- `plus.svg` and `minus.svg` for post-count stepper buttons through `QIcon`

### Checkbox States
Checkbox indicator now has explicit states:

- unchecked
- unchecked hover
- checked
- checked hover
- disabled

This prevents the visual indicator from disappearing on hover and improves accessibility.

### User-Facing Labels
Visible controls continue to use Thai plain-language labels. Internal tokens such as `BUILD_AWARENESS`, `FACEBOOK`, and `CONTROLLED_VOCAB_VALIDATION` are kept as hidden values or generated prompt output only, not as dropdown labels.

## Expected User Impact

The operator should feel that the screen is clearer and more stable:

- checkbox remains visible on hover
- dropdown arrows look like deliberate UI graphics
- post count plus/minus buttons look consistent
- UI asset paths are robust across machines
- user-facing labels stay readable for non-technical users

## Intentional Boundary
The generated GPT1 prompt still contains required machine tokens because GPT1 expects exact parameters. The user does not need to type them manually.
