# Desktop Pipeline Guided UX Spec

Status: PILOT UX STANDARD
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## 1. UX objective

The desktop app must reduce operator thinking load.

The operator should not need to understand the full internal pipeline before using the app. The app must show the current stage, the next action, and the safe boundary.

## 2. User mental model

The app should present the process as:

```text
1. Choose folder
2. Clean all files
3. Review PASS / FAIL
4. Copy GPT2 prompt
5. Create image and review
```

This is the visible user journey. The internal logic may run extraction, validation, TSV generation, and report generation, but the user should not need to operate those substeps manually.

## 3. Process engineering design

### SIPOC

| Element | Definition |
|---|---|
| Supplier | GPT1 Campaign Content Generator |
| Input | raw `.md`, `.txt`, `.text` files containing GPT1 output |
| Process | folder discovery → deterministic clean → validation gate → GPT2 prompt preparation |
| Output | clean TSV, JSON report, GPT2 handoff prompt |
| Customer | operator preparing BiiigBee social media posts |

### Stage gates

| Gate | Pass condition | Failure action |
|---|---|---|
| G1 Folder selected | valid folder path | ask user to choose folder |
| G2 Raw files found | at least 1 supported raw file | instruct user to add `.md` or `.txt` files |
| G3 Clean executed | extraction tool ran | show cleaner error |
| G4 Validation PASS | validator exit code `0` | open report; block GPT2 handoff |
| G5 GPT2 handoff | selected result is `PASS` | copy `MODE: TEMPLATE_HANDOFF` prompt |
| G6 Publish readiness | image and copy pass human review | do not publish yet |

## 4. Error-proofing rules

- Advanced validation overrides are hidden by default.
- `Clean All Files` is disabled until valid raw files exist.
- GPT2 prompt copy is disabled unless a selected result is `PASS`.
- The app auto-selects the first `PASS` result after cleansing.
- A `FAIL` result shows report-first guidance, not GPT2 guidance.
- Output files are placed under `_cleaned/` inside the selected folder so the user does not need to choose output paths.

## 5. Navigation language

Every stage should answer one question:

```text
What should I do now?
```

The coach card at the top of the app is the main navigation surface. It must use direct operator language, not system-oriented language.

Good:

```text
พบไฟล์ raw 3 ไฟล์ พร้อม clean แล้ว
กดปุ่มใหญ่ 2. Clean All Files ได้เลย
```

Avoid:

```text
Run deterministic validation pipeline
```

## 6. Defaults

| Setting | Default | Reason |
|---|---:|---|
| Expected rows per file | 10 | GPT1 normally creates 10 ideas so the operator can select 5 |
| Output location | `<selected-folder>/_cleaned/` | no user decision required |
| Input file extensions | `.md`, `.txt`, `.text` | covers normal GPT copy-paste files |

## 7. Non-goals for current pilot

The app does not call GPT1 or GPT2 directly.

The app does not publish to social media.

The app does not bypass human review.

The app does not convert failed validation into acceptable output.

## 8. Success criteria

A non-technical operator can:

1. select a folder;
2. press clean;
3. see which files passed;
4. copy a GPT2 prompt;
5. continue to GPT2 without knowing internal TSV validation rules.
