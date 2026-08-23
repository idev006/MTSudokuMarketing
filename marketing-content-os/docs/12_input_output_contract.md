# 12 — Final Input / Output Contract

## General Mode — Minimum Input
Required:
- `SKU`
- `NUMBER_OF_ROWS`

Optional:
- `PLATFORM` (default `AUTO`)
- `CAMPAIGN_DURATION` (default inferred from row count)
- `CAMPAIGN_GOAL` (default `AUTO`)

General Mode must not force the user to answer a long marketing questionnaire. The engine infers audience mix, funnel mix, content pillars, angles, CTA distribution, visual diversity, campaign sequence, and sell/value balance from the Marketing Plan.

## Advanced Mode — Override Layer
Uses the same engine as General Mode and may override:
- `CAMPAIGN_GOAL`
- `CAMPAIGN_THEME`
- `AUDIENCE_MIX`
- `FUNNEL_MIX`
- `CONTENT_PILLAR_MIX`
- `PLATFORM_MIX`
- `MARKETING_ANGLE_PREFERENCES`
- `FORBIDDEN_ANGLES`
- `CTA_STYLE`
- `PROMOTION`
- `VISUAL_MIX`
- `TONE`
- `POSTING_CADENCE`
- `ASPECT_RATIO`
- `PREVIOUS_CAMPAIGN_CONTEXT`
- `IMAGE_PROMPT_MODE`

Overrides may not contradict product facts or claim-safety rules.

## Output Row Contract
Each row is one complete Marketing Content Unit with these fields in this order:

1. `ROW_ID`
2. `SKU`
3. `CAMPAIGN_ID`
4. `SEQUENCE`
5. `PLATFORM`
6. `AUDIENCE`
7. `OBJECTIVE`
8. `FUNNEL_STAGE`
9. `CONTENT_PILLAR`
10. `MARKETING_ANGLE`
11. `CAMPAIGN_ROLE`
12. `HOOK`
13. `HEADLINE`
14. `CAPTION`
15. `CTA`
16. `HASHTAGS`
17. `VISUAL_TYPE`
18. `VISUAL_SUBJECT`
19. `VISUAL_SCENE`
20. `VISUAL_EMOTION`
21. `PRODUCT_PLACEMENT`
22. `TEXT_OVERLAY`
23. `TEXT_SAFE_ZONE`
24. `ASPECT_RATIO`
25. `IMAGE_SIZE`
26. `PROMPT_TEMPLATE_ID`
27. `IMAGE_PROMPT`

## Deterministic Output Rules
- Output row count must equal `NUMBER_OF_ROWS` exactly.
- `ROW_ID` must be unique within the batch.
- `CAMPAIGN_ID` must be stable across rows in the same campaign.
- `SEQUENCE` must be unique and continuous from 1..N.
- `SKU` must be valid in source of truth.
- Required fields may not be blank except where explicitly allowed.
- `IMAGE_PROMPT` must be the final field and blank by default in formula mode.
- No extra columns without explicit schema version change.

## File Output
Primary v1 export:
1. `CONTENT ROWS` as TSV
2. `IMAGE PROMPT TEMPLATES`
3. `PROMPT ASSEMBLY` guidance

Future compatible exports may include CSV and JSON, but must preserve the same semantic field contract.
