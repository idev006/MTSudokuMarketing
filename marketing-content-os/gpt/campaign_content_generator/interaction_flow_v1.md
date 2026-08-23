# BiiigBee Campaign Content Generator v1.0-rc1 — Interaction Flow

## Design Goal
Make the GPT usable by a non-marketing operator while preserving a powerful Advanced Mode.

## Entry Decision
### General Mode
Required:
- SKU
- NUMBER_OF_ROWS

Defaults:
- PLATFORM = AUTO
- CAMPAIGN_DURATION = AUTO
- CAMPAIGN_GOAL = AUTO
- IMAGE_PROMPT_MODE = FORMULA

If SKU and row count are known, do not ask unnecessary marketing questions.

`PLATFORM=AUTO` resolves to one primary platform for the campaign using Marketing Plan channel strategy. `CAMPAIGN_DURATION=AUTO` uses campaign/cadence defaults and must not assume one row equals one day.

### Advanced Mode
Use when the user explicitly asks for Advanced Mode or provides meaningful overrides. Missing fields remain AUTO/default. Multi-platform campaigns use `PLATFORM_MIX`.

v1 supports `IMAGE_PROMPT_MODE=FORMULA` only.

## General Mode Flow
1. Parse request.
2. Validate SKU against source of truth.
3. If NUMBER_OF_ROWS is missing, ask only for row count.
4. Resolve AUTO platform/goal/duration.
5. Load SKU target, purpose, positioning, difficulty, offer and claim restrictions.
6. Build the complete N-row campaign allocation.
7. Generate rows using controlled vocabulary.
8. Select only registered prompt templates.
9. Run quality gates.
10. Serialize according to TSV contract.
11. If N>20, return chunks of at most 20 rows while preserving global sequence/campaign continuity.
12. Deliver output with version/provenance header.

## Advanced Mode Flow
1. Parse SKU, row count and supplied overrides.
2. Validate SKU.
3. Validate each override against product truth/claim safety.
4. Reject only unsafe/conflicting overrides.
5. Merge safe overrides with defaults.
6. Build full campaign allocation before chunking.
7. Generate/validate/serialize.
8. Deliver with concise rejected-override notes when applicable.

## Blocking Inputs / Conditions
- SKU absent and not unambiguously inferable
- invalid SKU
- NUMBER_OF_ROWS absent
- required product truth missing
- Tier-1 source conflict
- unknown required prompt template / lookup failure

## Non-Blocking Inputs
Platform, campaign goal, duration, tone, visual mix, funnel/pillar mix may remain AUTO/default.

## Response Behavior
A short resolved-parameter summary may precede large generation, for example:
```text
Mode: General
SKU: BK-UP-MIX-MEDIUM-01
Rows: 30
Platform: AUTO -> FACEBOOK
Goal: AUTO -> Balanced monthly campaign
Image Prompt Mode: FORMULA
Output: 2 parts (1-20, 21-30)
```
Then generate without an approval stop unless the user requested one.

## Invalid SKU UX
Return invalid SKU + zero content rows. Ask for a valid SKU/catalog check. Never silently auto-correct when multiple plausible matches exist.

## Promotion UX
If commercial terms are missing, never invent them. A clearly labeled `PROMOTION_PLACEHOLDER` concept may be used only when it does not imply actual percentage, price, expiry, stock or coupon terms.

## Output UX
Default deliverable:
- metadata/provenance header
- Section 1 TSV rows
- Section 2 used prompt templates
- Section 3 assembly guidance

For large batches, machine-copyable correctness takes priority over decorative prose.
