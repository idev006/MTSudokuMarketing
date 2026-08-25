# Agile Kanban Completion Review — Plain-Language UI Labels

Status: DONE  
Date: 2026-08-25

## Goal

Reduce operator cognitive load by ensuring the desktop app displays human-readable labels instead of internal tokens, while still emitting the exact machine tokens required by GPT1.

## Kanban board

| Lane | Card | Status |
|---|---|---|
| Backlog | Replace internal dropdown tokens with plain-language labels | Done |
| Backlog | Preserve exact GPT1 token values behind the UI | Done |
| Backlog | Replace technical checkbox labels with plain-language labels | Done |
| Backlog | Keep high-contrast combo box display and dropdown states | Done |
| Backlog | Review UI copy for beginner readability | Done |
| In Progress | Implement app changes in `main.py` | Done |
| Review | Confirm generated GPT1 prompt still uses canonical tokens | Done |
| Done | Push implementation to `main` | Done |

## Implemented changes

### 1. Human-readable dropdowns

The following controls now display user-friendly labels:

- ช่องทางโพสต์
- เป้าหมายของโพสต์
- ระยะเวลาแคมเปญ

The UI no longer shows raw values such as `BUILD_AWARENESS`, `CREATE_ENGAGEMENT`, or `RETENTION_CROSS_SELL` in those dropdowns.

### 2. Hidden token values preserved

The app still sends exact GPT1 tokens in the generated prompt:

- `PLATFORM`
- `CAMPAIGN_GOAL`
- `CAMPAIGN_DURATION`

Example:

```text
User sees: ทำให้คนรู้จักสินค้า
Generated prompt value: BUILD_AWARENESS
```

### 3. Plain-language checkbox labels

The optional GPT1 flags now display human-readable labels while keeping token values internally:

- ให้ระบบเลือกช่องทางและรูปแบบให้เหมาะสม
- ตรวจคำมาตรฐานของระบบ
- ใช้ข้อมูลสินค้าจากฐานข้อมูล
- บังคับตรวจชุดข้อมูลอ้างอิงก่อนสร้าง

### 4. UI copy cleanup

Technical labels were replaced with operator-friendly Thai wording, such as:

- ตรวจไฟล์และเตรียมส่งต่อ
- เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1
- ผลการตรวจไฟล์
- เตรียมส่งเข้า GPT2

## Acceptance criteria

| Criterion | Result |
|---|---|
| User does not need to understand internal campaign tokens | Pass |
| GPT1 generated prompt still uses exact tokens | Pass |
| Dropdown choices are readable by non-technical users | Pass |
| Checkbox labels explain what the option does | Pass |
| UI color contrast for combo boxes remains explicit | Pass |

## Remaining guardrail

Some terms remain visible because they are actual workflow names the operator must use:

- GPT1
- GPT2
- SKU in the generated prompt preview
- `.md` / `.txt`

These are acceptable because the app explains what the user should do with them.
