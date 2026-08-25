# Parallel Cockpit GPT1-Start Review

Status: DONE
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop/main_workspace_parallel.py`

## Reason for change

The desktop cockpit must not begin only at folder cleansing. The real operator pipeline begins earlier:

```text
select product -> choose N -> copy GPT1 request -> run GPT1 -> save raw output -> clean/validate -> prepare GPT2 prompts
```

The previous parallel cockpit supported the deterministic handoff but did not make the GPT1 request builder the first visible step.

## Implemented changes

- Added a visible `0. เริ่มงาน: สร้างคำสั่งสำหรับ GPT1` start panel.
- Loaded product choices from `marketing-content-os/schemas/sku_lookup_v1.tsv`.
- Displayed human-readable product names while preserving the SKU as the operational value.
- Added product detail preview.
- Generated the GPT1 request text from the selected SKU and current N:

```text
SKU: <SKU>
NUMBER_OF_ROWS: <N>
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

- Added `คัดลอกคำสั่ง GPT1`.
- Added `เปิดโฟลเดอร์ raw ของสินค้านี้`, creating `_operator_workspace/<SKU>/raw` when needed.
- Added `GPT1_REQUEST.txt` in the SKU workspace as a local trace of the request sent to GPT1.
- Kept the existing parallel clean/validate workflow.
- Kept the existing `_ready_for_gpt2` package workflow after PASS.

## Updated user journey

```text
1. เลือกสินค้า
2. เลือกจำนวนโพสต์ N
3. คัดลอกคำสั่ง GPT1
4. วางคำสั่งใน GPT1
5. บันทึกคำตอบ GPT1 เป็น .md/.txt ใน raw folder ของสินค้า
6. กดตรวจหลายสินค้าแบบขนาน
7. เปิด _ready_for_gpt2
8. คัดลอก 01_gpt2_prompt.txt, 02_gpt2_prompt.txt ... เข้า GPT2
```

## Review

| Gate | Result |
|---|---|
| GPT1 request begins workflow | PASS |
| Product selection avoids SKU memorization | PASS |
| N is synchronized with GPT1 prompt | PASS |
| Raw folder is created per SKU | PASS |
| Parallel workspace pipeline retained | PASS |
| GPT2-ready package retained | PASS |

## Notes

The app still does not call GPT1, GPT2, image generation, or publishing automatically. Those remain human/GPT quality gates.
