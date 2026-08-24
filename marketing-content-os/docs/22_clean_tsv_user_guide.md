# Clean TSV Handoff User Guide

Status: ACTIVE GUIDE
Date: 2026-08-24
Audience: human operators using GPT #1 output before GPT #2 handoff

## 1. This guide in one sentence

Do not send raw GPT Markdown directly to GPT #2. First convert it into a clean validated TSV file, then use that clean TSV row set as the handoff artifact.

## 2. Why this step exists

GPT #1 can generate valid 27-field campaign rows but may still add presentation noise around the TSV, such as empty Markdown code fences.

That raw Markdown is useful as evidence, but it is not the safest operational artifact.

The safe handoff artifact is:

```text
raw GPT Markdown -> clean_validate_campaign_markdown.py -> clean TSV -> validator PASS -> GPT #2
```

## 3. What files are involved

Input:

```text
raw_output.md
```

This is the full text copied from GPT #1, including metadata, sections, code fences, prose, and TSV rows.

Output:

```text
clean_output.tsv
```

This contains only:

```text
canonical 27-column header
validated ROW-* data rows
```

Tools:

```text
marketing-content-os/tools/clean_validate_campaign_markdown.py
marketing-content-os/tools/extract_tsv_from_markdown.py
marketing-content-os/tools/validate_campaign_output.py
```

Reference files used by validator:

```text
marketing-content-os/schemas/sku_lookup_v1.tsv
marketing-content-os/schemas/controlled_vocabulary_v1.tsv
marketing-content-os/templates/prompt_template_registry_v1.tsv
```

## 4. Normal operator workflow

Step 1: Copy GPT #1 full output into a text file.

Example:

```text
marketing-content-os/tmp/raw_output.md
```

Step 2: Run the clean handoff command.

Example for 1 row:

```bash
python marketing-content-os/tools/clean_validate_campaign_markdown.py \
  --input marketing-content-os/tmp/raw_output.md \
  --output marketing-content-os/tmp/clean_output.tsv \
  --expected-rows 1 \
  --sku-lookup marketing-content-os/schemas/sku_lookup_v1.tsv \
  --taxonomy marketing-content-os/schemas/controlled_vocabulary_v1.tsv \
  --template-registry marketing-content-os/templates/prompt_template_registry_v1.tsv
```

Example for 20 rows:

```bash
python marketing-content-os/tools/clean_validate_campaign_markdown.py \
  --input marketing-content-os/tmp/raw_output.md \
  --output marketing-content-os/tmp/clean_output.tsv \
  --expected-rows 20 \
  --sku-lookup marketing-content-os/schemas/sku_lookup_v1.tsv \
  --taxonomy marketing-content-os/schemas/controlled_vocabulary_v1.tsv \
  --template-registry marketing-content-os/templates/prompt_template_registry_v1.tsv
```

Step 3: Check the terminal result.

Good result:

```text
RESULT=PASS
```

Bad result:

```text
RESULT=FAIL
```

If the result is FAIL, do not send the file to GPT #2.

## 5. What the cleaner removes

The cleaner ignores:

- empty code fences
- prose before or after TSV
- metadata lines
- section headings
- Markdown presentation noise
- duplicate TSV headers from multi-part GPT output

The cleaner keeps only:

- canonical `ROW_ID ... IMAGE_PROMPT` header
- data rows beginning with `ROW-`
- rows that contain exactly 27 tab-delimited fields

## 6. What the validator checks

The validator checks machine-verifiable gates, including:

- exact expected row count
- canonical 27-column header order
- one stable nonblank `CAMPAIGN_ID`
- unique `ROW_ID`
- continuous `SEQUENCE` from 1 to N
- valid approved SKU
- controlled vocabulary tokens
- `VISUAL_TYPE -> PROMPT_TEMPLATE_ID` mapping
- blank `IMAGE_PROMPT` in FORMULA mode
- basic diversity gates where applicable

Semantic/product review still remains separate.

## 7. What to give GPT #2

Give GPT #2 the clean validated TSV row or rows.

Do not give GPT #2 the raw GPT #1 Markdown if it contains fences, metadata, prose, or warnings.

GPT #2 should treat the clean row values as the locked campaign input. GPT #2 may refine visual fields according to its own rules, but must not change locked product truth or campaign strategy fields.

## 8. Simple decision table

| Situation | Action |
|---|---|
| Raw GPT output has empty fences but extractor + validator pass | Use clean TSV for GPT #2 |
| Extractor finds zero rows | Do not proceed; rerun GPT #1 or inspect raw output |
| Validator fails row count/schema/tokens/template mapping | Do not proceed; fix upstream output |
| Clean TSV passes but copy quality feels weak | Keep as draft review; semantic review still needed |
| Clean TSV passes and semantic review passes | Approved for GPT #2 handoff |

## 9. Important rule

Raw GPT Markdown is evidence.

Clean validated TSV is the operational handoff artifact.

This keeps the workflow reliable even when GPT Markdown formatting is imperfect.
