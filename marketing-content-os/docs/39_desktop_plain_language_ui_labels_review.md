# Desktop Plain-Language UI Labels Review

Status: ACTIVE
Date: 2026-08-25

## Purpose

This review records the UI wording correction requested by the product owner: labels, buttons, tabs, helper text, messages, table headers, and status guidance inside the desktop app must be understandable by ordinary operators. The app should not require users to know internal pipeline vocabulary.

## Design principle

The desktop app should use plain Thai labels for operator-facing actions. Internal terms such as `pipeline`, `raw folder`, `handoff`, `clean TSV`, `selected rows`, and `prompt` may still exist in code and generated artifacts, but visible UI should explain what the user must do next in everyday language.

## Implemented changes

- App title changed to Thai plain language: `เครื่องมือเตรียมคอนเทนต์โซเชียล BiiigBee`.
- Command bar label changed to `ปุ่มหลัก`.
- Primary actions changed to Thai plain-language labels:
  - `คัดลอกคำสั่ง GPT1`
  - `เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1`
  - `เลือกโฟลเดอร์คำตอบ GPT1`
  - `ตรวจไฟล์และเตรียมส่งต่อ`
  - `เปิดโฟลเดอร์ผลลัพธ์`
- Tabs changed to task-oriented Thai labels.
- Table headers changed to Thai labels.
- Metrics changed from system terms to Thai user terms where possible.
- Helper text and message boxes changed from internal system wording to user-action wording.
- GPT1/GPT2 remain visible only where they are actual user-facing tools in the workflow.

## Accepted remaining technical terms

Some exact GPT/tool names remain because the user must use those tools directly:

- GPT1
- GPT2
- SKU
- `.md`, `.txt`

Some machine values remain inside the generated GPT1 prompt preview because they are the exact required tokens for GPT1, not user labels:

- `PLATFORM`
- `CAMPAIGN_GOAL`
- `NUMBER_OF_ROWS`
- controlled flag tokens

## Review result

PASS_WITH_NOTE.

The UI wording is now substantially closer to ordinary operator language. Further refinement should continue by observing the owner using the app and replacing any label that causes hesitation with a clearer action phrase.
