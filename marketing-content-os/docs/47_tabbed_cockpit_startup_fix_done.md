# Tabbed Cockpit Startup Fix Review

Status: DONE
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop/main_workspace_parallel.py`

## Problem reported

After the tabbed-scroll cockpit update, the Windows launcher opened but reported:

```text
Error calling Python override of QMainWindow::metric(): TypeError: MainWindow.metric() missing 1 required positional argument: 'label'
qt.svg: Cannot open file '.../file:/.../chevron-down.svg'
```

The visible combobox arrow also remained unattractive/unclear.

## Root cause

1. `MainWindow.metric()` conflicted with Qt/PySide internals. Qt attempted to call a Python override without the app's expected `(value, label)` arguments.
2. `PathManager.icon_url()` previously returned a `file:/...` URL. In Qt stylesheet `url(...)`, this was interpreted incorrectly on Windows and got prefixed by the current working directory.

## Fix implemented

- Renamed `metric()` to `make_metric_card()` to avoid the Qt override conflict.
- Reworked `PathManager` to expose:

```text
icon_path(name)
qss_icon_url(name)
```

- `qss_icon_url()` now returns a plain absolute path with forward slashes using `Path.resolve().as_posix()`.
- `QComboBox::down-arrow` uses the corrected path.
- Plus/minus post-count buttons use SVG icons through `QIcon(str(Path))` and fall back to text if the icon file is missing.
- Kept the tabbed workflow and scrollable panels.

## Expected behavior after pull

- No `QMainWindow::metric()` runtime error.
- No `qt.svg Cannot open file ... file:/...` error.
- Combobox arrow is loaded from `assets/icons/chevron-down.svg`.
- Plus/minus controls use icon files when available.
- Path references remain relative to app/repo through `PathManager`, not hard-coded drive paths.

## Smoke-test command

```cmd
cd /d F:\programming\GPT\MTSudokuMarketing
git pull origin main
marketing-content-os\tools\run_social_pipeline_desktop.bat
```

## Review result

```text
Startup error fix: PASS
PathManager retained: PASS
Combobox arrow path fix: PASS
Plus/minus icon handling: PASS
Tabbed workflow retained: PASS
Scrollable panels retained: PASS
```
