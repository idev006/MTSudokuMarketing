# Clean TSV Handoff Status Addendum — 2026-08-24

## Context
Focused regression FMT-R001 reproduced OUTPUT-FMT-001 on both SYSTEM_INSTRUCTION_VERSION 1.12 and 1.13.

The repeated failure was formatting-only in the observed cases: the GPT Builder candidate still emitted an empty generic Markdown code fence before the TSV block, while the actual canonical data row remained extractable and structurally valid-looking.

## Decision
Instruction-only mitigation is no longer the primary mitigation path for OUTPUT-FMT-001.

The project will use a deterministic extractor/post-processor and validator pipeline. The production handoff artifact is the clean validated TSV, not raw GPT Markdown.

## New pipeline artifacts
- `marketing-content-os/tools/clean_validate_campaign_markdown.py`
- `marketing-content-os/docs/21_clean_tsv_handoff_contract.md`

## Status impact
- GPT #1 remains Candidate / Not Production until the clean TSV handoff pipeline is tested on representative raw outputs.
- GPT #2 activation can proceed after a clean validated GPT #1 row artifact is produced and accepted as the GPT #2 input contract.
- Raw Markdown OUTPUT-FMT-001 remains an open raw-presentation defect, but it becomes non-blocking for downstream handoff when deterministic cleanup and validation pass.

## Next action
Run the clean TSV handoff pipeline on the FMT-R001 v1.13 raw output and record the result as CLEAN-R001.
