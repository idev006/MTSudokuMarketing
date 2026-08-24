# Pilot Batch 001 Production Runbook

Status: ACTIVE PILOT
Date: 2026-08-24
Owner: BiiigBee Easy Maths Marketing Content OS

## Purpose

This runbook starts the first controlled production batch for the social media content pipeline. The objective is to produce usable, reviewable, post-ready social media content while measuring speed, quality, and safety.

This is not a fully autonomous publishing workflow. Human review remains required before publishing.

## Strategic Objective

Pilot Batch 001 must prove that the pipeline can:

1. reduce content creation time versus manual workflow;
2. preserve product truth and claim safety;
3. generate standardized post packages;
4. create image-generation handoff prompts ready for visual production;
5. produce at least three publish-ready social media post candidates.

## Approved Pipeline

```text
GPT1 Campaign Content Generator
→ Clean TSV validation
→ GPT2 Visual Prompt Refiner
→ Final post package assembly
→ Image generation
→ Human review
→ Approved social media post
```

Raw GPT1 Markdown is not an operational production artifact. Clean validated TSV is the operational handoff artifact.

## Batch Scope

### Batch ID

```text
PILOT-BATCH-001
```

### Source SKU

```text
BK-UP-MIX-EASY-01
```

### GPT1 Request

```text
SKU: BK-UP-MIX-EASY-01
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

### Required Clean Handoff

The GPT1 output must be cleaned and validated before GPT2 use.

Required clean handoff checks:

- exactly 10 content rows;
- canonical 27-field row format;
- stable CAMPAIGN_ID within the batch;
- SEQUENCE 1..10;
- valid SKU from `sku_lookup_v1.tsv`;
- controlled vocabulary compliance;
- VISUAL_TYPE to PROMPT_TEMPLATE_ID mapping compliance;
- blank IMAGE_PROMPT in GPT1 Formula Mode;
- no unsafe claims;
- no named-variant overclaim for Standard SKU.

## Target Pilot Content Mix

Select three rows for the first image-production pass:

| Slot | Preferred Visual Type | Purpose |
|---|---|---|
| P001 | PRODUCT_HERO | Main product awareness post |
| P002 | BENEFIT or STUDENT_ACTIVITY | Parent value / learning benefit post |
| P003 | PRODUCT_BOX | Digital mockup / promotional asset |

If the 10-row batch does not contain all preferred visual types, choose the closest safe rows and record the deviation.

## Product Truth Guardrails

For `BK-UP-MIX-EASY-01`, safe product facts include:

- Brand: `BiiigBee Easy Maths`;
- Product name from SKU lookup: `ประถมปลาย Mixed Sudoku Pack EASY`;
- Thai name from SKU lookup: `ซูโดกุ ประถมปลาย แบบผสม ระดับ EASY`;
- Grade band: `ประถมปลาย (ป.4–ป.6)`;
- Display difficulty: `EASY`;
- Format: `Printable PDF; Optional Print-on-Demand`;
- Puzzle count: `500`;
- Answer key status: `Included for all 500 puzzles`;
- Standard SKU exact composition: `UNSPECIFIED`;
- Safe wording: generic `9x9 mixed Sudoku ระดับ EASY`.

Do not claim named variants, exact type counts, official endorsement, discounts, urgency, guaranteed outcomes, or competition wins.

## GPT2 TEMPLATE_HANDOFF Input Pattern

For each selected clean row, use:

```text
MODE: TEMPLATE_HANDOFF

GOAL:
Create final social media post copy and image-generation handoff for this approved clean validated row. Preserve product truth and strategy. Do not add unsupported claims. IMAGE_PROMPT may be assembled from approved fields, SKU lookup facts, and template logic.

INPUT_ROW:
[paste one complete 27-field clean validated row]
```

If GPT2 reports an unresolved lookup field such as `PRODUCT_NAME`, resolve from canonical `sku_lookup_v1.tsv`, not from guesswork.

## Final Post Package Definition of Done

A post package is publish-ready only when it includes:

- ROW_ID;
- SKU;
- PLATFORM;
- post status;
- final caption;
- final headline or hook;
- CTA;
- hashtags;
- final visual direction;
- final image-generation prompt or template handoff;
- generated image candidate;
- human review result;
- known open warnings, if any.

## Review Gate

Human review must verify:

1. Product truth is accurate.
2. No unsupported promotion or urgency is present.
3. No guaranteed performance/result claim is present.
4. No named Sudoku variant overclaim is present for Standard SKU.
5. Template and visual type match.
6. Image does not render misleading Thai text, fake logos, distorted Sudoku grids, or misleading physical shipping packaging.
7. Caption and CTA match the locked strategy.

## Pilot Batch 001 KPI Targets

| KPI | Target |
|---|---:|
| Clean extraction success | 100% for this batch |
| Valid row count | 10/10 |
| Selected post packages | 3 |
| Generated image candidates | at least 3 |
| Publish-ready posts after review | at least 1, target 3 |
| Unsafe claim escape | 0 |
| Named-variant overclaim escape | 0 |
| Template mismatch escape | 0 |
| Average row-to-post-package time | ≤ 15 minutes |
| Average approved prompt-to-usable-image time | ≤ 10 minutes |
| First-pass post package approval | ≥ 70% |

## Timing Capture

For each selected post package, capture:

- `started_at`;
- `gpt1_raw_received_at`;
- `clean_validated_at`;
- `gpt2_handoff_at`;
- `image_generated_at`;
- `human_reviewed_at`;
- `final_status`.

Use these values to compute actual production cycle time.

## Batch Exit Criteria

Pilot Batch 001 is complete when:

1. 10 GPT1 rows are generated;
2. clean validation passes or failures are recorded;
3. at least 3 rows are selected for GPT2 handoff;
4. at least 3 image prompts are produced;
5. at least 1 image candidate is generated;
6. at least 1 post is marked publish-ready after human review;
7. KPI baseline is recorded.

## Immediate Operator Action

Run GPT1 with:

```text
SKU: BK-UP-MIX-EASY-01
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

Then provide the raw GPT1 output for cleaning, validation, row selection, and GPT2 handoff.
