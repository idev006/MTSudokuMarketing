# CLEAN-R003 Review — Clean TSV Handoff

Date: 2026-08-24
Component: BiiigBee Campaign Content Generator -> Clean TSV Handoff Pipeline
Raw source: user-supplied GPT Builder Markdown output `Pasted markdown (2).md`

## Input

- SKU: `BK-UP-MIX-MEDIUM-01`
- NUMBER_OF_ROWS: `30`
- PLATFORM: `AUTO`
- CAMPAIGN_GOAL: `AUTO`

## Raw-output observation

The raw Markdown is a multi-part output and still includes OUTPUT-FMT-001 style empty/generic code fences. This is treated as raw-presentation evidence only.

- SYSTEM_INSTRUCTION_VERSION: `1.13`
- Parts: 2
  - Part 1: sequence 1..20
  - Part 2: sequence 21..30
- Empty code blocks found: 2
- Raw row span: 30 data rows, sequence 1..30

## Clean pipeline result

- Extracted canonical rows: 30
- Single campaign ID: `CMP-BK-UP-MIX-MEDIUM-01-20260824-MONTHLY`
- SEQUENCE range: 1..30
- Field count: 27 fields per row
- IMAGE_PROMPT: blank for all rows
- Controlled vocab: PASS
- VISUAL_TYPE -> PROMPT_TEMPLATE_ID mapping: PASS
- Product grounding: PASS
- Standard SKU named-variant composition claims: not emitted beyond generic mixed Sudoku
- Multi-part extraction: PASS

## Diversity checks

Top VISUAL_TYPE counts:

- PRODUCT_HERO: 4
- PARENT_CHILD: 4
- BENEFIT: 4
- TEACHER_CLASSROOM: 4
- STUDENT_ACTIVITY: 3
- INFOGRAPHIC: 3
- PUZZLE_CHALLENGE: 3
- LIFESTYLE: 3
- PRODUCT_BOX: 2

Top MARKETING_ANGLE family counts:

- SKILL_PROGRESS: 4
- TEACHER_UTILITY: 4
- LOGIC_TRAINING: 3
- PARENT_CONFIDENCE: 3
- 500_PUZZLE_VALUE: 3
- FOCUS_ACCURACY: 3
- VARIETY_MIX: 3
- PRINTABLE_CONVENIENCE: 3
- CHALLENGE_MASTERY: 2
- PORTFOLIO_NEXT_STEP: 2

## Warnings / notes

- ASPECT-RATIO-001 monitor: rows 21 and 27 use `1:1.618` / `1236x2000 px` for PRODUCT_BOX.
- Raw Markdown still has OUTPUT-FMT-001 presentation defects; clean TSV handoff removes them.

## Verdict

CLEAN-R003 = PASS_WITH_NOTE

Rationale: the raw GPT Markdown still has presentational fence defects, but the deterministic clean handoff path extracted the intended 30 rows from two parts and passed machine-verifiable validation. Downstream systems, including GPT #2, must use the clean validated TSV artifact rather than raw GPT Markdown.
