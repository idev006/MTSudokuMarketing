# Campaign Content Generator v1.0 — Acceptance Execution Rubric

## Purpose
Provide a repeatable review method for the acceptance corpus before declaring Production v1.0.

## Per-Test Result
Each test must be labeled:
- `PASS`
- `PASS_WITH_WARNING`
- `FAIL`

## Hard-Fail Conditions
Any one of the following makes the test `FAIL`:
- invalid/fabricated SKU accepted as real
- wrong product fact
- wrong grade/difficulty relationship
- invented price/discount/deadline/stock/testimonial/award/social proof
- unsafe Competition claim
- wrong number of rows
- missing/extra/reordered schema columns in strict-output test
- duplicate ROW_ID
- non-continuous SEQUENCE
- non-blank IMAGE_PROMPT in FORMULA mode
- material campaign incoherence that makes the output unusable

## Warning Conditions
May be `PASS_WITH_WARNING` when no hard gate fails but:
- copy quality is uneven
- angle distribution is slightly concentrated for a small batch
- visual variation could improve
- some CTA/hook structures are stylistically close
- platform adaptation is adequate but not optimal

## Scored Quality Dimensions
Use 0–5 per dimension for diagnostic scoring:
1. Product Truth Accuracy
2. Audience/Difficulty Fit
3. Campaign Coherence
4. Copy Quality
5. Diversity
6. Visual Direction Quality
7. Claim Safety
8. Schema/Determinism
9. Human Usability

Maximum diagnostic score = 45.

Recommended candidate threshold:
- no hard failures
- average >= 4.0/5 across dimensions
- Product Truth Accuracy, Claim Safety and Schema/Determinism must each be 5/5

## Batch Audit Metrics
For N >= 20 record:
- row_count_actual
- unique_row_id_count
- sequence_min/max
- direct_sale_max_consecutive
- top_angle_share
- top_visual_type_share
- duplicate_or_near_duplicate_hook_count
- repeated_cta_pattern_count
- unsafe_claim_count
- fabricated_fact_count

## Release Gate
Production v1.0 requires:
- all hard-gate tests PASS
- no fabricated fact across corpus
- no unsafe Competition claim across corpus
- deterministic schema tests PASS at N = 1, 5, 20, 30, 60
- invalid SKU tests fail safely
- General Mode judged usable by a non-marketing operator

Until then, release label remains `v1.0-rc1` or later RC.
