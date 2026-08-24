# Social Content Production Workspace

Status: ACTIVE / PILOT PRODUCTION
Date: 2026-08-24
Owner: BiiigBee Easy Maths marketing content pipeline

## 1. Purpose

This document converts the GPT1/GPT2 pipeline into a repeatable production workspace that the operator can run later without relying on chat memory.

The working target is:

- all approved SKUs;
- 5 social posts per SKU;
- reusable post packages for multi-day social media posting;
- controlled pilot production before any fully automated publishing.

## 2. Production target

The current canonical SKU set contains 24 SKUs.

Therefore the first full social content inventory target is:

```text
24 SKUs × 5 posts per SKU = 120 planned social post slots
```

Each post slot must become a post package before it is publish-ready.

## 3. Approved pipeline in plain language

Use this every time.

```text
Step 1: GPT1 creates campaign rows
Step 2: Clean TSV tool extracts and validates rows
Step 3: Select the best 5 rows for that SKU
Step 4: GPT2 reviews/refines selected rows
Step 5: Assemble final caption + CTA + hashtags + image prompt
Step 6: Generate image
Step 7: Human review
Step 8: Mark post package as READY
```

Operator meaning:

- GPT1 is the content planner.
- Clean TSV is the machine gate.
- GPT2 is the visual/prompt reviewer.
- Human review is the final business/brand gate.

## 4. Input to GPT1 for each SKU

For each SKU, run:

```text
SKU: <SKU>
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

Why 10 rows if only 5 posts are needed?

Because GPT1 should generate enough options. The operator then selects the best 5 rows for social posting. This improves quality and gives alternatives.

## 5. Selection rule for 5 posts per SKU

Select a balanced set whenever available:

1. PRODUCT_HERO
2. BENEFIT
3. STUDENT_ACTIVITY or LIFESTYLE
4. PRODUCT_BOX digital mockup
5. INFOGRAPHIC, PUZZLE_CHALLENGE, TEACHER_CLASSROOM, PARENT_CHILD, or COMPETITION where appropriate

Do not force a visual type that violates product truth or campaign logic.

## 6. Storage layout

Production workspace:

```text
marketing-content-os/production/social-posts/
```

Files:

```text
README.md
social_content_inventory_v1.tsv
```

Future generated batches may be stored under:

```text
marketing-content-os/production/social-posts/batches/<BATCH_ID>/
```

Recommended future files per batch:

```text
raw_gpt1_output.md
clean_validated_rows.tsv
selected_rows.tsv
gpt2_handoffs.md
post_packages.tsv
image_prompts.md
review_notes.md
```

## 7. Post package Definition of Done

A post is publish-ready only when it has:

- SKU;
- ROW_ID from clean validated GPT1 row;
- final caption;
- headline/hook;
- CTA;
- hashtags;
- visual type;
- final image prompt;
- generated image candidate;
- human review status = APPROVED;
- no unsafe claim;
- no unsupported named-variant claim;
- no misleading physical shipping implication;
- post-ready status = READY.

## 8. Status vocabulary

Use these statuses in inventory/tracker files.

```text
PLANNED
GPT1_RAW_READY
CLEAN_VALIDATED
SELECTED_FOR_GPT2
GPT2_REVIEWED
PROMPT_READY
IMAGE_GENERATED
HUMAN_REVIEWED
READY
PUBLISHED
BLOCKED
```

## 9. KPI targets

Production KPI targets inherit from `23_pilot_production_kpi_framework.md`.

Minimum operational targets:

- 5 selected post rows per SKU;
- 120 planned slots total;
- row validity rate >= 98%;
- clean extraction success rate >= 99%;
- unsafe claim escape = 0;
- first-pass approval rate >= 70% during pilot;
- post-ready package time <= 15 minutes after clean row selection;
- image prompt usability >= 80%.

## 10. Non-negotiable guardrails

- Raw GPT1 Markdown is evidence only, not operational handoff.
- Clean validated TSV is the operational handoff artifact.
- GPT2 must receive complete 27-field rows.
- Standard SKU exact composition remains UNSPECIFIED unless approved source says otherwise.
- Do not claim named Sudoku variants for Standard SKUs.
- Competition products are training/preparation only.
- Do not add unsupported discounts, deadlines, guarantees, trophies, or official competition symbols.
- Do not publish without human review.

## 11. Immediate production order

Start with Pilot Batch 001 already defined in `24_pilot_batch_001_runbook.md`.

Then continue by SKU order in `social_content_inventory_v1.tsv` until every SKU has 5 selected post packages.

## 12. Operator quick checklist

For one SKU:

```text
[ ] Run GPT1 with NUMBER_OF_ROWS=10
[ ] Save raw GPT1 output
[ ] Run clean/validate
[ ] Choose 5 best rows
[ ] Run GPT2 TEMPLATE_HANDOFF for each selected row
[ ] Assemble final post package
[ ] Generate image
[ ] Review image/copy
[ ] Mark READY or BLOCKED
```
