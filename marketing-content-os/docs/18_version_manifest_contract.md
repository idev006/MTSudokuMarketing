# 18 — Knowledge / Version Manifest Contract v1

## Purpose
A Custom GPT does not automatically know the Git commit from which uploaded knowledge files came. Production tests therefore require an explicit manifest bundled with the GPT knowledge set.

## Required Manifest Fields
- `CONTENT_OS_VERSION`
- `GPT_BUILD_VERSION`
- `SYSTEM_INSTRUCTION_VERSION`
- `ROW_SCHEMA_VERSION`
- `TAXONOMY_VERSION`
- `PROMPT_TEMPLATE_VERSION`
- `MARKETING_PLAN_REF`
- `KNOWLEDGE_BUILD_DATE`
- `KNOWLEDGE_STATUS`

## Rules
- `MARKETING_PLAN_REF` must be a real approved Git commit/reference supplied during knowledge packaging; never invented by the GPT.
- If Marketing Plan files change, rebuild the manifest before production use.
- Test reports must record the manifest values used for each run.
- Manifest metadata is batch/package metadata; it does not add columns to the 27-field content-row schema.

## Output Package Header
Before Section 1, v1 outputs should include a compact metadata header:

```text
CONTENT_OS_VERSION: 1.0-rc1
ROW_SCHEMA_VERSION: 1.0
TAXONOMY_VERSION: 1.0
PROMPT_TEMPLATE_VERSION: 1.0
MARKETING_PLAN_REF: <from knowledge manifest>
GENERATION_STATUS: DRAFT_REVIEW_REQUIRED
```

If the manifest is missing during acceptance/production testing, the run is not provenance-complete and must be marked `PASS_WITH_WARNING` at best unless provenance is a hard gate for that test.
