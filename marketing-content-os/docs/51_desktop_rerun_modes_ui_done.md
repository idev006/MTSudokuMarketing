# Desktop Rerun Modes UI — Done

Status: DONE
Date: 2026-08-25

## Objective

Expose the two required GPT1-check rerun modes in the desktop UI so operators can safely run an existing `_operator_workspace` again without guessing what the program will do.

## User-observed gap

The backend already supported rerun behavior, but the UI still had one generic button:

```text
ตรวจหลายสินค้าแบบขนาน
```

That was ambiguous for an existing workspace because the operator needed two explicit choices:

1. ตรวจใหม่ทั้งหมดจาก raw เดิม
2. ตรวจซ้ำเฉพาะที่ไม่ผ่าน

## Implemented UI changes

Updated `marketing-content-os/apps/social_pipeline_desktop/main_workspace_parallel.py`.

### 1. Two explicit rerun buttons

The check tab now exposes:

```text
ตรวจใหม่ทั้งหมดจาก raw เดิม
ตรวจซ้ำเฉพาะที่ไม่ผ่าน
```

Both modes preserve `raw/` and pass the selected mode into backend `process_workspace_parallel()`.

### 2. Safe cleanup button

Added:

```text
ล้างเฉพาะผลลัพธ์ที่สร้างใหม่ได้
```

This calls `cleanup_generated_outputs(selected_root)` and confirms that only generated outputs are removed:

```text
_cleaned/
_ready_for_gpt2/
_workspace_parallel_summary.json
```

It does not delete:

```text
raw/
GPT1_REQUEST.txt
```

### 3. Diagnostic export button

Added:

```text
สร้างไฟล์วินิจฉัย
```

This exports a diagnostic ZIP for the selected SKU when a row is selected, or the workspace default diagnostic bundle otherwise.

### 4. PASS_WITH_AUTOFIX visibility

The dashboard now shows an `แก้อัตโนมัติ` metric. The table includes:

```text
ผลละเอียด
Auto-fix
ต้องทำต่อ
```

This lets operators see `PASS_WITH_AUTOFIX`, diagnosis, and next action without opening JSON.

### 5. Summary mode visibility

The summary tab now shows:

```text
Run ID
โหมดตรวจ
แก้อัตโนมัติ
```

so a rerun can be audited from the UI.

## Expected user experience

When selecting an existing `_operator_workspace`, the operator now sees separate choices:

```text
ตรวจใหม่ทั้งหมดจาก raw เดิม
ตรวจซ้ำเฉพาะที่ไม่ผ่าน
```

The default production behavior remains safe: raw GPT1 source files are preserved, generated outputs are recreated only when requested, and diagnostics are available from the UI.
