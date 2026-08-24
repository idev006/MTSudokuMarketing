# Social Posts Production Workspace

This folder stores the operational working list for social media content production.

Current production target:

```text
24 approved SKUs × 5 posts per SKU = 120 planned social post slots
```

Primary inventory:

```text
social_content_inventory_v1.tsv
```

Use the inventory to track progress from planned SKU coverage to post-ready packages.

## Standard working flow

```text
GPT1 raw output
→ clean validated TSV
→ selected rows
→ GPT2 TEMPLATE_HANDOFF / REFINE_FIELDS
→ final post package
→ image prompt
→ generated image
→ human review
→ ready/published
```

## Important rule

Do not treat raw GPT1 Markdown as a final artifact. Raw GPT1 output must be cleaned and validated before handoff to GPT2.

## Current first batch

Start with:

```text
SKU: BK-UP-MIX-EASY-01
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

Then select 5 rows for that SKU and update the inventory.
