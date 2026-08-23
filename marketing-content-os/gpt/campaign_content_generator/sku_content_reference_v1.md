# BiiigBee SKU Content Reference v1

Purpose: retrieval-friendly mirror of `schemas/sku_content_spec_v1.tsv` for GPT Builder. This file grounds grid-size and content-detail claims without changing the 27-field content-row schema.

## Claiming rule
- Grid size may be stated only from this reference/spec.
- `VARIANT_SCOPE` is the approved program universe for the grade band, NOT proof that every named variant is included in every Standard SKU.
- For Standard SKUs, `EXACT_COMPOSITION_STATUS=UNSPECIFIED`: say `mixed Sudoku` and the approved grid size; do NOT invent named variant membership, ratios, or counts.
- For Competition SKUs, the mix is custom/multi-type and multi-difficulty. Do NOT invent exact type counts or claim exhaustive official coverage.
- If an exact composition/count is later approved, it must be added to the canonical TSV before the GPT may claim it.

## Grade-band grid/content scope
### EL — ประถมต้น (all BK-EL-* and CP-EL-*)
- GRID_SIZE: `6x6`
- VARIANT_SCOPE: Classic, Alphabet, Diagonal, Jigsaw, Thai Alphabet

### UP — ประถมปลาย (all BK-UP-* and CP-UP-*)
- GRID_SIZE: `9x9`
- VARIANT_SCOPE: Classic, Alphabet, Diagonal, Jigsaw, Even-Odd, Jigsaw Diagonal, Windoku, Asterisk, Consecutive, Thai Alphabet

### LS — มัธยมต้น (all BK-LS-* and CP-LS-*)
- GRID_SIZE: `9x9`
- VARIANT_SCOPE: Classic, Alphabet, Diagonal, Jigsaw, Even-Odd, Jigsaw Diagonal, Windoku, Asterisk, Consecutive, Thai Alphabet

### US — มัธยมปลาย (all BK-US-* and CP-US-*)
- GRID_SIZE: `9x9`
- VARIANT_SCOPE: Classic, Alphabet, Diagonal, Jigsaw, Even-Odd, Jigsaw Diagonal, Windoku, Asterisk, Consecutive, Thai Alphabet

## Standard SKU policy
All 20 `BK-*-MIX-*` SKUs are single fixed difficulty with mixed Sudoku types and 500 puzzles. Current v1 canonical content spec does not assign exact per-type counts. Use generic wording such as `ซูโดกุแบบผสม 6x6` or `ซูโดกุแบบผสม 9x9` as applicable.

## Competition SKU policy
`CP-EL-NAT-COMP-01` uses 6x6 training content. `CP-UP-NAT-COMP-01`, `CP-LS-NAT-COMP-01`, and `CP-US-NAT-COMP-01` use 9x9 training content. Competition products use a custom mixed-type/mixed-difficulty training design. Keep claims to training/preparation and approved product facts.
