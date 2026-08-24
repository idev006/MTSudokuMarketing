# Clean TSV Handoff Contract v1

## Status
ACTIVE for GPT #1 candidate handoff after FMT-R001 v1.12 and v1.13 reproduced OUTPUT-FMT-001.

## Purpose
The raw GPT Markdown response is no longer the production handoff artifact. The production handoff artifact is the deterministic **clean validated TSV** produced from raw GPT Markdown by the extractor/post-processor and validator pipeline.

This contract exists because GPT #1 repeatedly emitted empty generic Markdown code fences before TSV blocks despite strengthened instructions. The defect is formatting-only when canonical 27-field rows can still be extracted and validated. The system therefore treats raw Markdown as evidence and clean validated TSV as the operational artifact.

## Inputs
- Raw GPT #1 Markdown/text response.
- Expected row count.
- Approved SKU lookup.
- Approved controlled vocabulary.
- Approved prompt-template registry.

## Deterministic pipeline
1. Archive the raw GPT Markdown as evidence.
2. Run `marketing-content-os/tools/clean_validate_campaign_markdown.py`.
3. Extract only canonical data rows that:
   - start with `ROW-`;
   - contain exactly 26 tab characters, meaning 27 TSV fields;
   - match the canonical row schema when re-emitted with the canonical header.
4. Ignore empty fences, untagged fences, prose, summaries, and non-row text.
5. Write one clean TSV artifact with exactly one canonical header.
6. Run `validate_campaign_output.py` against the clean TSV.
7. Pass the clean validated TSV to downstream systems, including GPT #2.

## Required command shape

```bash
python marketing-content-os/tools/clean_validate_campaign_markdown.py \
  --raw-input raw_gpt_output.md \
  --clean-output clean_output.tsv \
  --expected-rows 20 \
  --sku-lookup marketing-content-os/schemas/sku_lookup_v1.tsv \
  --taxonomy marketing-content-os/schemas/controlled_vocabulary_v1.tsv \
  --template-registry marketing-content-os/templates/prompt_template_registry_v1.tsv \
  --report clean_output_report.json
```

## Pass criteria
The clean handoff passes only when:
- extracted row count equals expected row count;
- clean TSV has canonical 27-column header;
- every physical data row has exactly 27 fields;
- `ROW_ID` values are unique;
- one stable nonblank `CAMPAIGN_ID` is used for the dataset;
- `SEQUENCE` is globally continuous `1..N`;
- all SKUs exist in approved lookup;
- controlled vocabulary fields are canonical;
- `MARKETING_ANGLE` family is canonical;
- `PROMPT_TEMPLATE_ID` is approved and matches `VISUAL_TYPE`;
- `IMAGE_PROMPT` is blank in rc1 FORMULA mode;
- diversity hard gates pass unless an explicit approved override allows concentration.

## Failure criteria
The clean handoff fails when:
- no canonical rows can be extracted;
- extracted row count differs from expected row count;
- validator returns `RESULT=FAIL`;
- semantic/human review identifies product-truth, claim-safety, or campaign-fit failure.

## Raw Markdown warning policy
Raw GPT Markdown may contain non-production formatting defects such as:
- empty generic Markdown fences;
- untagged fences;
- extra prose outside TSV;
- repeated section headers.

These are warnings only if the clean validated TSV passes all gates and raw evidence is archived. They remain release-quality defects for raw GPT presentation, but they do not block GPT #2 handoff when deterministic cleanup succeeds.

## GPT #2 handoff rule
GPT #2 must receive only:
- one complete clean validated 27-field row; or
- a clean validated TSV row copied from the clean artifact.

GPT #2 must not use raw GPT #1 Markdown, GPT #1 self-summary, or unvalidated extracted text as an authoritative input.

## Release governance update
For GPT #1 rc1, production/candidate handoff quality is measured on the clean validated TSV artifact. Raw GPT Markdown is evidence, not the operational data contract.

Production v1.0 still requires semantic/human review and resolution or explicit acceptance of any remaining non-blocking defects.
