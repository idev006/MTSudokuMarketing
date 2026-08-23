# Acceptance Run 001 — Preflight

Date: 2026-08-23
Target: `BiiigBee Campaign Content Generator v1.0-rc1`
Marketing Plan reference: `445cc35e9dfff3a26bd81cdb08398f024057513c`
Content OS main hardening merge: `dee12fa26da6688ac45bf59aab9a90e92a0cea3a`

## Scope
This is a preflight before executing TC-001..TC-032 against an actual GPT Builder candidate.

## Static Checks Completed
- acceptance corpus TC-001..TC-032 exists
- deterministic validator specification exists
- controlled vocabulary exists
- approved prompt-template registry contains 10 visual families
- v1 is locked to FORMULA mode
- knowledge manifest exists
- 27-field row contract is frozen

## Blocking Defect Found
`schemas/sku_lookup_schema.tsv` exists, but an approved populated 24-SKU lookup dataset is not present in the repository.

This blocks production-grade execution of:
- SKU existence validation against the intended lookup artifact
- product-owned prompt placeholder resolution
- TC-031 SKU_LOOKUP_PROMPT_ASSEMBLY
- deterministic validator SKU gate using the intended canonical dataset

Do not substitute model assumptions or silently derive a permanent lookup artifact without an approved product/marketing source mapping.

## GPT Builder Execution Boundary
The repository contains the GPT Builder configuration and instructions, but creation/configuration of a Custom GPT in the ChatGPT GPT Builder requires a product-side write capability. This execution environment does not expose a GPT Builder create/update tool. Therefore this run must not be recorded as an actual Custom GPT acceptance run until the candidate is instantiated in GPT Builder using the approved package.

## Action Taken
Added `tools/validate_campaign_output.py` as the first independent deterministic validator implementation. It checks machine-verifiable gates including schema/order, row count, IDs, sequence, SKU lookup membership, taxonomy, prompt registry mapping, FORMULA-mode blank IMAGE_PROMPT, conversion streaks, and concentration thresholds.

## Current Decision
`ACCEPTANCE_RUN_001 = BLOCKED_PRE_EXECUTION`

Blockers:
1. create/approve populated `sku_lookup_v1.tsv` for all 24 SKUs
2. instantiate `BiiigBee Campaign Content Generator v1.0-rc1` in GPT Builder from the approved build package

After both blockers are cleared, execute TC-001..TC-032 and record deterministic + semantic/human results without changing architecture unless a test exposes a real defect.
