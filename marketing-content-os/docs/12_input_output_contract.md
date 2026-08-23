# 12 — Final Input / Output Contract v1

## General Mode — Minimum Input
Required:
- `SKU`
- `NUMBER_OF_ROWS`

Optional:
- `PLATFORM` (default `AUTO`)
- `CAMPAIGN_DURATION` (default `AUTO`)
- `CAMPAIGN_GOAL` (default `AUTO`)

General Mode must not force a long marketing questionnaire. The engine infers audience mix, funnel mix, content pillars, angles, CTA distribution, visual diversity, campaign sequence, and sell/value balance from approved Marketing Plan data.

### AUTO Rules
- `PLATFORM=AUTO` resolves to one primary canonical output platform for the campaign.
- Multi-platform campaigns require Advanced Mode `PLATFORM_MIX`.
- `CAMPAIGN_DURATION=AUTO` uses channel/cadence/campaign defaults; it must not assume one content row equals one day.

## Advanced Mode — Override Layer
Uses the same engine and may override campaign goal/theme, audience/funnel/content-pillar mix, platform mix, angle preferences/forbidden angles, CTA style, promotion, visual mix, tone, posting cadence, aspect ratio, and previous campaign context.

Overrides may not contradict product truth or claim-safety rules.

## IMAGE_PROMPT_MODE v1
Supported value:
- `FORMULA`

`PRECOMPILED` and `BOTH` are not active v1 modes and require a future contract/version.

## Output Row Contract
Each row is one Marketing Content Unit with fields in exactly this order:
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

## Structured-Field Rules
Controlled fields must use canonical values from `docs/16_controlled_vocabulary.md` / machine-readable taxonomy. `AUTO` is an input state and must be resolved before row output.

## Deterministic Row Rules
- total output rows = `NUMBER_OF_ROWS` exactly
- unique `ROW_ID`
- stable `CAMPAIGN_ID` within one campaign
- `SEQUENCE` exactly 1..N
- valid SKU on every row
- required fields nonblank except explicitly allowed
- `PROMPT_TEMPLATE_ID` must exist in approved registry
- `VISUAL_TYPE` and template family must be compatible
- `IMAGE_PROMPT` is the final field and blank in Formula Mode
- no extra columns without a schema-version change

## Product Metadata / Prompt Assembly
The 27-row schema does not duplicate stable product metadata solely for prompt construction. Final prompt assembly uses:

`Content Row + SKU Lookup + Prompt Template`.

SKU lookup supplies product-owned placeholders such as brand/product name, grade band, display difficulty and format.

## Metadata Header
A batch/package carries version/provenance metadata outside the 27-row schema:
- CONTENT_OS_VERSION
- ROW_SCHEMA_VERSION
- TAXONOMY_VERSION
- PROMPT_TEMPLATE_VERSION
- MARKETING_PLAN_REF
- GENERATION_STATUS

Values come from the explicit knowledge/version manifest; Git references must never be invented.

## TSV Serialization
Section 1 follows `docs/19_tsv_serialization_contract.md`: one physical line per row, exactly 27 tab-separated fields, embedded tabs replaced with spaces, embedded physical newlines serialized as literal `\n`, and CR removed.

## Large Batches
- N <= 20: one part
- N > 20: chunks of at most 20 rows

The complete campaign must be planned before chunking. Across chunks, CAMPAIGN_ID stays stable, ROW_ID stays globally unique and SEQUENCE remains globally continuous. Total rows across all parts must equal N exactly.

## File / Text Output
Primary v1 package:
1. metadata/provenance header
2. `CONTENT ROWS` as TSV
3. `USED IMAGE PROMPT TEMPLATES`
4. `PROMPT ASSEMBLY` guidance

Future CSV/JSON exports may be added only if they preserve the same semantic contract and versioning rules.
