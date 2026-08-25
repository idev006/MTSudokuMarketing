# Tabbed Scroll Parallel Cockpit Review

Status: DONE
Date: 2026-08-25
Scope: Desktop social content pipeline UI/UX

## 1. Reason for change

The previous cockpit placed GPT1 request creation, workspace selection, parallel validation, result table, and GPT2 prompt queue in one vertical screen. The pipeline was functionally correct, but the UI could overflow on smaller screens and required the operator to visually scan too much at once.

The user requested:

- scroll handling when the UI overflows;
- better panel separation;
- preservation of combobox/spinner arrow treatment;
- preservation of PathManager relative path handling.

## 2. Implementation summary

The app now uses a tabbed workflow with scrollable tab pages:

```text
1. สร้างคำสั่ง GPT1
2. ตรวจคำตอบ GPT1
3. ส่งเข้า GPT2
4. สรุปผล
```

Each tab is wrapped in `QScrollArea`, so smaller screens can scroll without losing access to controls.

## 3. Pipeline coverage

The visible flow now mirrors the production process:

```text
Select product + N
-> copy GPT1 request
-> save GPT1 output into SKU/raw
-> run parallel validation for workspace/SKU folders
-> create _cleaned
-> create _ready_for_gpt2
-> copy ready GPT2 prompt files one by one
```

The app still preserves the deterministic pipeline boundaries. It does not call GPT1, GPT2, generate images, approve copy, or publish posts automatically.

## 4. PathManager

`PathManager` remains the single place for deriving paths from the application file location:

```text
app_dir
content_os_root
repo_root
default_workspace
sku_lookup
icon_dir
sku_workspace(sku)
raw_folder(sku)
icon_path(name)
icon_url(name)
```

No drive-specific path is hard-coded in the application.

## 5. Icons / arrow controls

The combobox down arrow now references `assets/icons/chevron-down.svg` through `PathManager.icon_url()`.

The post-count control uses icon buttons for plus/minus through `PathManager.icon_path()` and `QIcon`, preserving the earlier requirement for graphic controls instead of relying on OS spinner rendering.

## 6. UX review

### Pass

- GPT1 is now the first visible workflow step.
- Tabs reduce visual overload.
- Scroll areas prevent overflow from hiding content.
- Operator can still choose `_operator_workspace` for parallel SKU processing.
- `_ready_for_gpt2` remains the user-facing GPT2 handoff package.
- Path handling remains relative and portable.
- Arrow/icon controls remain explicit.

### Remaining manual gates

- User still runs GPT1 manually.
- User still runs GPT2 manually.
- User still reviews GPT2 output.
- Image generation and final post approval remain human quality gates.

## 7. Review verdict

```text
Document-driven pipeline alignment: PASS
Tabbed workflow: PASS
Scrollable overflow handling: PASS
PathManager preservation: PASS
Combobox arrow/icon treatment: PASS
Plus/minus graphic buttons: PASS
Parallel workspace flow: PASS
GPT2-ready package flow: PASS
```
