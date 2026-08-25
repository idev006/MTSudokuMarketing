# Operator Guided Mode V3 Review

Status: ACTIVE UI/UX COMPLETION REVIEW
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## 1. Objective

Improve the desktop pipeline so a non-technical operator can move from SKU planning to GPT1 request, raw folder import, deterministic cleansing, and GPT2 handoff with minimal cognitive load.

This review follows the document-driven project rule: the UI must follow the documented workflow and the workflow must remain the source of truth.

## 2. User requirements addressed

- The operator can specify dynamic post count `N`, where `1 <= N <= 60`.
- The UI must make the first step obvious: GPT1 is always the starting point.
- The user should not need to manually edit `<SKU>` inside a prompt.
- The user should not need to understand TSV internals before continuing.
- GPT2 actions should not look available before a PASS result exists.
- Empty panels should explain what will happen next instead of appearing broken.
- The N control should be clear and theme-safe.

## 3. Implemented V3 changes

### 3.1 SKU-first GPT1 request panel

The setup panel now includes a SKU input field. The GPT1 prompt preview is generated from:

```text
SKU: <operator SKU>
NUMBER_OF_ROWS: <N>
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

This reduces manual editing errors and makes the GPT1 starting point explicit.

### 3.2 Manual N stepper

The previous Qt spinner was replaced with a controlled stepper:

```text
[-] [N] [+]
```

The input is clamped to:

```text
1 <= N <= 60
```

This avoids theme-specific low-contrast spinner arrows and is easier for operators to understand.

### 3.3 Copy GPT1 Prompt button

A dedicated `Copy GPT1 Prompt` button was added. The intended operator path is now:

```text
1. Enter SKU
2. Set N
3. Copy GPT1 Prompt
4. Paste into GPT1
5. Save GPT1 output as .md or .txt
6. Choose raw folder
7. Clean and prepare GPT2 prompts
```

### 3.4 GPT2 actions hidden until relevant

GPT2 action buttons are hidden before PASS results exist. They are shown only when a PASS result is selected, or when a FAIL result needs report access.

This reduces the risk that the operator presses the wrong button too early.

### 3.5 Empty states

Batch results and preview areas now explain what will appear after processing. The table no longer looks like a broken blank area before the first run.

## 4. UX result

The updated visible workflow is:

```text
1. ใส่ SKU + ตั้ง N
2. Copy GPT1 prompt
3. เลือก folder raw
4. Clean + เตรียม prompts
5. GPT2 + Review
```

The UI now answers the operator's main question more directly:

```text
What should I do now?
```

## 5. Process engineering boundary

The app still automates only deterministic handoff work:

- raw-file discovery;
- clean TSV generation;
- deterministic validation;
- selected N-row output generation;
- GPT2 prompt file generation;
- batch summary generation;
- navigation and gating.

The app still does not automate:

- GPT1 generation;
- GPT2 reasoning/refinement;
- image generation decision;
- human review;
- publishing.

## 6. Review conclusion

Operator Guided Mode V3 better satisfies the Level 3 cockpit requirement. It reduces manual editing, makes the first step obvious, prevents premature GPT2 handoff, and improves clarity when the workspace is empty.

The app is now more suitable for a document-driven production workflow where generated outputs must be correct, efficient, and easy to continue downstream.
