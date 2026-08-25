# Operator Command Bar V4 Review

Status: ACTIVE UX FIX
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop/main.py`

## 1. User problem

The previous Operator Guided Mode V3 hid too many action buttons until later states. The user correctly identified the operational problem:

```text
ไม่มีปุ่มสั่งงาน แล้วจะใช้ยังไง
```

In a production operator cockpit, core commands must be visible at all times. The app may disable commands that are not ready, but it must not hide the workflow's primary command path.

## 2. UX principle

The app must provide an always-visible command bar that answers:

```text
What can I do now?
```

The coach card answers:

```text
What should I do now?
```

Both are required. Guidance without visible commands creates friction.

## 3. Implemented fix

The main window now includes an always-visible Command Bar directly below the stage flow:

```text
Command Bar:
1. Copy GPT1 Prompt
2. Choose Raw Folder
3. Run Pipeline
Open _cleaned Folder
Reset
```

The buttons are visible immediately. Readiness is communicated by enabled/disabled state:

- `Copy GPT1 Prompt` is always available after SKU/N entry.
- `Choose Raw Folder` is always available.
- `Run Pipeline` is visible but disabled until raw files are found.
- `Open _cleaned Folder` is visible but disabled until output exists.
- GPT2 continuation buttons remain in the lower panel and become enabled only when a PASS result is selected.

## 4. Process engineering rationale

The command bar maps directly to the production workflow:

```text
1. GPT1 request creation
2. Raw input import
3. Deterministic clean/validate/output preparation
4. GPT2 continuation
5. Human review
```

This preserves process control while reducing cognitive load.

## 5. Expected operator effect

The operator should now feel:

```text
I can see the buttons.
I know the order of work.
If a button is disabled, I understand it is not ready yet.
I do not need to hunt for actions inside panels.
```

## 6. Review result

The V4 command bar fix addresses the immediate usability defect. The app is now closer to a production operator cockpit because the primary workflow commands are visible, ordered, and tied to gate readiness.
