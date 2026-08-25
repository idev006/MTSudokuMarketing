# Relative PathManager Icon References — Done

Status: DONE
Date: 2026-08-25
Scope: desktop social content pipeline UI

## Request

Use relative paths through `PathManager` for UI asset references, especially combobox and stepper icons.

## Changes

The desktop app now keeps all icon references behind `PathManager`:

```text
PathManager.icon_path(name)      -> resolved internal Path object
PathManager.repo_relative(path)  -> repo-relative string
PathManager.icon_ref(name)       -> repo-relative icon string
PathManager.qss_icon_url(name)   -> repo-relative QSS icon string
```

QSS no longer receives a drive-specific absolute path such as `F:/...` for the combobox arrow. It receives a repository-relative asset reference such as:

```text
marketing-content-os/apps/social_pipeline_desktop/assets/icons/chevron-down.svg
```

The plus/minus stepper buttons also use `PathManager.icon_ref()` when creating `QIcon` objects.

## Review

- No hard-coded Windows drive path in app code: PASS
- Icon references routed through `PathManager`: PASS
- Combobox chevron path is repo-relative: PASS
- Plus/minus icon references are repo-relative: PASS
- Existing pipeline behavior preserved: PASS

## Note

The launcher sets the working directory to repository root before starting the app, so repository-relative icon references resolve consistently on the operator machine.
