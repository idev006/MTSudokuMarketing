# 21 — Deterministic Validator Specification v1

## Goal
Separate machine-checkable hard gates from semantic/human review. The GPT may self-check, but self-checking is not the only validator for production release.

## Deterministic Checks
A validator should verify:
1. metadata header present and parseable
2. canonical 27-column TSV header/order
3. exact total row count
4. exactly 27 fields per row
5. unique nonblank `ROW_ID`
6. one stable `CAMPAIGN_ID` for a single campaign
7. `SEQUENCE` is exactly 1..N with no gaps/duplicates
8. SKU exists in approved SKU lookup/catalog
9. controlled vocabulary fields use canonical values
10. `PROMPT_TEMPLATE_ID` exists in approved registry
11. `VISUAL_TYPE` maps to the expected prompt family
12. `IMAGE_PROMPT` is blank in v1 Formula Mode
13. no direct-sale/CONVERSION role more than 2 consecutive rows
14. visual-type concentration <=25% when mathematically practical and not explicitly overridden
15. marketing-angle family concentration <=20% when mathematically practical and not explicitly overridden
16. no physical TSV row contains malformed tab/newline serialization
17. all chunks collectively contain exactly N unique sequence values for large batches
18. no unresolved prompt placeholder after downstream prompt assembly validation

## Semantic / Human Checks
Require model/human review for:
- audience appropriateness
- copy quality and natural Thai
- campaign narrative/coherence
- materially different hooks
- semantic duplication
- brand voice
- claim nuance
- visual concept quality
- whether CTA strength fits campaign context

## Result Model
- `PASS` — deterministic hard gates pass and semantic review acceptable
- `PASS_WITH_WARNING` — deterministic hard gates pass; non-blocking semantic/provenance issue remains
- `FAIL` — any truth, schema, serialization, unsafe-claim, invalid-SKU, wrong-row-count, invalid-template or other hard gate fails

## Implementation Direction
Initial validator may be implemented in Python or Google Sheets/App Script. It must consume the same row schema, taxonomy, template registry, SKU lookup, and knowledge manifest used by the GPT build.

## Release Rule
Do not declare Campaign Content Generator v1.0 Production based only on the GPT saying its own output passed validation. At least the deterministic hard gates must be checked independently.
