# 20 — Large Batch Output Protocol v1

## Purpose
Prevent truncation and schema corruption when generating large 27-field campaigns.

## Batch Threshold
Default v1 behavior:
- `NUMBER_OF_ROWS <= 20` -> one output part
- `NUMBER_OF_ROWS > 20` -> chunk into parts of at most 20 rows

The user may request a smaller chunk size. Do not increase above 20 in v1 unless the runtime proves safe.

## Campaign Continuity
Across all chunks:
- one stable `CAMPAIGN_ID`
- global `SEQUENCE` remains continuous 1..N
- `ROW_ID` remains globally unique
- campaign allocation is planned for the full N rows before chunk serialization
- diversity is evaluated across the full planned batch, not independently per chunk

## Part Metadata
Each chunk must state:
- campaign ID
- part number / total parts
- global row range, e.g. `21-40 of 60`
- same version/provenance header

## No Partial-Success Claim
If the system can only return part of a requested batch because of an output/runtime limit, it must clearly mark the campaign incomplete. Never present 20 of 60 rows as a completed 60-row campaign.

## Acceptance Testing
For N=30 and N=60, verify:
- correct number of chunks
- exact total N rows across chunks
- no duplicate/missing sequence values
- stable campaign ID
- global diversity checks pass
- every chunk uses the same schema/version metadata

## Future File Export
If a runtime supports generating a complete downloadable TSV/TXT artifact reliably, file export may replace conversational chunking while preserving the same logical protocol and validation gates.
