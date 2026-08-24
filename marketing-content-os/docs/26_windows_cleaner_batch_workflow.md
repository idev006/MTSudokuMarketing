# Windows Cleaner Batch Workflow

Status: ACTIVE GUIDE
Date: 2026-08-24
Audience: human operators cleaning GPT #1 Campaign Content Generator output before GPT #2 Visual Prompt Refiner handoff

## Purpose

This guide explains how to use the Windows batch wrapper for the GPT #1 Cleaner.

The Cleaner is not a GPT. It is a local deterministic script that converts raw GPT #1 Markdown/text output into a clean validated TSV artifact.

Use this workflow whenever GPT #1 emits campaign rows for BiiigBee Sudoku Marketing.

## Files

Batch wrapper:

```text
marketing-content-os/tools/clean_gpt1_output.bat
```

Underlying Python tool:

```text
marketing-content-os/tools/clean_validate_campaign_markdown.py
```

Outputs created by the batch wrapper:

```text
marketing-content-os/production/social-posts/clean/<raw_file_name>_clean.tsv
marketing-content-os/production/social-posts/reports/<raw_file_name>_clean_report.json
```

Inventory to update after handoff/review:

```text
marketing-content-os/production/social-posts/social_content_inventory_v1.tsv
```

## Input file

Copy the full raw GPT #1 output into a text or markdown file.

Recommended location:

```text
marketing-content-os/tmp/<sku>_raw.md
```

Example:

```text
marketing-content-os/tmp/BK-UP-MIX-EASY-01_raw.md
```

The raw file may include metadata, prose, headings, empty Markdown fences, and TSV rows. The cleaner will extract only canonical `ROW-*` rows that match the 27-field row contract.

## Command

From the repository root:

```bat
marketing-content-os\tools\clean_gpt1_output.bat marketing-content-os\tmp\BK-UP-MIX-EASY-01_raw.md 10
```

Argument 1 is the raw GPT #1 text file.

Argument 2 is the expected number of rows. If omitted, the batch wrapper defaults to 10.

## PASS behavior

If the command prints `RESULT: PASS`, continue as follows:

1. Open the clean TSV file printed by the command.
2. Choose the best 5 rows for that SKU.
3. Copy one complete 27-field row at a time into GPT #2.
4. Use GPT #2 with `MODE: TEMPLATE_HANDOFF`.
5. If GPT #2 returns `PASS` or `PASS_WITH_WARNING`, use its final image-generation handoff to create the image.
6. Human review the final post package before publishing.
7. Update the inventory status for that SKU/post slot.

## FAIL behavior

If the command prints `RESULT: FAIL`, do not send any row to GPT #2.

Open the JSON report printed by the command and inspect:

- extracted row count;
- validator exit code;
- validator stdout/stderr;
- failed rule or missing/invalid field.

Then either rerun GPT #1 or fix the raw input source and run the Cleaner again.

## GPT #2 handoff prompt

Use this shape after a clean row is selected:

```text
MODE: TEMPLATE_HANDOFF

GOAL:
Create final social media post copy and image-generation handoff for this approved row. Preserve product truth and strategy. Do not add unsupported claims. IMAGE_PROMPT may be assembled from approved fields and template logic.

INPUT_ROW:
<paste exactly one complete 27-field clean TSV row here>
```

## Important rules

- Raw GPT #1 Markdown is evidence only.
- Clean validated TSV is the operational handoff artifact.
- GPT #2 must receive only clean validated rows.
- Do not send rows to GPT #2 when Cleaner/validator fails.
- Do not publish without human review.
- Do not use unsupported claims, named Standard-SKU variants, fake logos, or physical shipping cues for digital/mockup products.
