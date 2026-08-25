# Desktop Pipeline V2 Completion Review

Status: PILOT COMPLETE
Date: 2026-08-25
Scope: `marketing-content-os/apps/social_pipeline_desktop`

## 1. Executive objective

Build a guided desktop operator cockpit that manages the deterministic parts of the BiiigBee Sudoku Marketing production workflow so the user does not need to understand the internal pipeline.

The product goal is not only to clean files. The product goal is to reduce thinking load and prevent wrong handoff.

## 2. Process engineering design target

The workflow must move one or more GPT1 raw output files through controlled gates:

```text
1. GPT1 raw files
2. Folder discovery
3. Deterministic clean
4. Validation gate
5. Recommended 5-row selection
6. GPT2 handoff prompt generation
7. GPT2 visual refinement
8. Image generation
9. Human review
10. Post-ready package
```

## 3. SIPOC

| Element | Design |
|---|---|
| Supplier | GPT1 Campaign Content Generator, human operator |
| Input | folder containing `.md`, `.txt`, or `.text` GPT1 raw output files |
| Process | discover → clean → validate → select 5 rows → generate GPT2 prompts → guide next action |
| Output | clean TSV, reports, selected 5-row TSV, GPT2 prompt files, batch summary |
| Customer | operator, GPT2 Visual Prompt Refiner, social content production process |

## 4. Stage gates

| Gate | Pass condition | Failure action | App behavior |
|---|---|---|---|
| G1 Folder | valid folder selected | choose another folder | `Clean` disabled until raw files exist |
| G2 Raw files | supported files found | add `.md` / `.txt` files | coach card tells operator what to do |
| G3 Clean | canonical rows extracted | rerun GPT1 or fix raw file | report JSON generated |
| G4 Validate | validator exit code `0` | do not send to GPT2 | result remains `FAIL` |
| G5 Select | 5 recommended rows generated | inspect clean TSV manually | selected TSV generated only after PASS |
| G6 GPT2 prompt | prompt files generated | inspect selected rows | copy button enabled only for PASS |
| G7 Publish | human review approved | do not publish | app does not publish |

## 5. Automation boundary

The app automates deterministic, repeatable work:

- raw-file discovery;
- output folder management;
- clean TSV generation;
- deterministic validation;
- PASS / FAIL classification;
- 5-row recommended selection;
- GPT2 prompt file generation;
- batch summary generation;
- next-action navigation.

The app does not automate judgment-heavy work:

- GPT1 content generation;
- GPT2 visual refinement;
- final image generation decision;
- claim-safety human review;
- publishing.

## 6. UX design

The operator journey is intentionally reduced to 5 visible steps:

```text
1. Choose Folder
2. Clean All Files + Prepare GPT2 Prompts
3. Review PASS / FAIL
4. Copy First GPT2 Prompt
5. Create image + Human Review
```

The app's coach card must always answer:

```text
What should I do now?
```

## 7. Output workspace

For each selected folder, the app creates:

```text
_cleaned/
  clean/
    <raw_file>_clean.tsv
  reports/
    <raw_file>_clean_report.json
  selected/
    <raw_file>_selected_5.tsv
  handoff/
    <raw_file>/
      01_<ROW_ID>_gpt2_prompt.txt
      02_<ROW_ID>_gpt2_prompt.txt
      03_<ROW_ID>_gpt2_prompt.txt
      04_<ROW_ID>_gpt2_prompt.txt
      05_<ROW_ID>_gpt2_prompt.txt
    <raw_file>_handoff_index.tsv
  pipeline_batch_summary.json
```

## 8. Recommended 5-row selection logic

The default selection prefers a balanced 5-post set using `VISUAL_TYPE` priority:

```text
PRODUCT_HERO
STUDENT_ACTIVITY
PARENT_CHILD
BENEFIT
INFOGRAPHIC
PUZZLE_CHALLENGE
PRODUCT_BOX
LIFESTYLE
TEACHER_CLASSROOM
COMPETITION
```

The algorithm selects at most one row from each priority visual type before filling remaining slots from the clean row order. This reduces repetitive manual selection while preserving operator review.

## 9. Expected user feeling

The intended user experience is:

```text
I only choose a folder and press one main button.
The program tells me what to do next.
The program prevents me from sending bad files to GPT2.
The program already prepares the 5 rows and prompts.
I do not need to understand TSV internals to continue.
```

## 10. Expected production result

Per PASS raw GPT1 file, the operator should get:

- 1 clean validated TSV;
- 1 validation report;
- 1 selected 5-row TSV;
- 5 GPT2 handoff prompt files;
- 1 handoff index;
- 1 batch-level summary.

Per SKU, this supports the intended production target:

```text
1 SKU → 10 GPT1 ideas → 5 selected posts → 5 GPT2 prompts → 5 post packages
```

Across the full catalog:

```text
24 SKUs × 5 posts = 120 post-ready packages after GPT2, image generation, and human review
```

## 11. Review result

### What is complete

- PySide6 desktop app exists.
- Requirements file exists.
- Windows launcher exists.
- Folder-level raw discovery exists.
- Batch clean / validation exists.
- PASS / FAIL result table exists.
- Guided coach card exists.
- Advanced options are hidden by default.
- Clean button is gated by raw-file discovery.
- GPT2 prompt copy is gated by PASS status.
- Automatic 5-row selection exists.
- GPT2 prompt files are generated automatically.
- Batch summary is generated.

### Controlled limitations

- The app does not call GPT1 or GPT2 directly.
- The app does not generate images directly.
- The app does not publish.
- Human review is still required.

### Overall assessment

The desktop app now satisfies the Level 3 workflow goal for pilot use: it is a guided operator cockpit that manages the deterministic pipeline and reduces operator cognitive load while preserving quality gates.
