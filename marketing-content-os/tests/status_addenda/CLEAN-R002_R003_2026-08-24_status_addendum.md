# CLEAN-R002/R003 Status Addendum — 2026-08-24

## Summary

CLEAN-R002 and CLEAN-R003 validate the deterministic clean TSV handoff path after OUTPUT-FMT-001 reproduced through GPT #1 v1.13.

## Results

- CLEAN-R002: PASS_WITH_NOTE
  - Raw output: 20 rows for `BK-UP-MIX-EASY-01`
  - Result: extractor + deterministic validator pass
  - Note: raw Markdown still includes an empty generic code fence; clean TSV handoff removes it.

- CLEAN-R003: PASS_WITH_NOTE
  - Raw output: 30 rows for `BK-UP-MIX-MEDIUM-01`
  - Raw output is multi-part, with Part 1 rows 1..20 and Part 2 rows 21..30
  - Result: extractor + deterministic validator pass
  - Note: raw Markdown still includes empty generic code fences; clean TSV handoff removes them.

## Operational decision

Raw GPT Markdown remains useful as evidence, but it is not the production or GPT #2 handoff artifact.

The operational handoff artifact is the clean validated TSV produced by the deterministic extractor/post-processor and accepted by the deterministic validator.

## Impact

- OUTPUT-FMT-001 remains a raw-presentation defect.
- OUTPUT-FMT-001 no longer blocks GPT #2 candidate testing when clean validated TSV artifacts are used.
- GPT #2 must receive only clean validated 27-field rows.
- Continue to monitor ASPECT-RATIO-001 for `PRODUCT_BOX` rows using `1:1.618` / `1236x2000 px`.

## GPT #2 readiness

With CLEAN-R001, CLEAN-R002, and CLEAN-R003 passing, GPT #2 candidate testing can proceed using clean validated TSV rows as the only accepted input artifact.
