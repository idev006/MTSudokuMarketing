# 10 — Implementation Roadmap

## Phase 1 — Finalize v1 Contracts — COMPLETE

Locked:
- product requirements / system boundary
- General Mode minimum inputs
- Advanced Mode override model
- content row schema
- output contract
- system integrity and quality gates
- Shared Marketing Brain contract
- acceptance test plan

## Phase 2 — Build Campaign Content Generator v1.0 — NEXT

Create the GPT configuration for **BiiigBee Campaign Content Generator** using the approved v1 contracts.

Required components:
- system instructions
- source-of-truth usage rules
- General Mode flow
- Advanced Mode flow
- campaign planning logic
- batch generation logic
- pre-output validation
- deterministic TSV output behavior

## Phase 3 — Build Prompt Template Library

Create/version at least 8–10 reusable visual prompt families, including product hero, lifestyle, parent-child, student activity, teacher/classroom, puzzle challenge, benefit/infographic, competition, and product box.

## Phase 4 — Acceptance Testing of Generator

Run the acceptance plan against:
- Standard + Competition SKUs
- N = 1, 5, 20, 30, 60 rows
- General Mode
- Advanced Mode overrides
- invalid SKU cases
- claim-safety cases
- diversity and campaign-coherence cases

Do not declare v1.0 production-ready if any hard truth/safety/schema gate fails.

## Phase 5 — Google Sheets Prompt Assembly

- placeholder mapping
- prompt-template version mapping
- formula assembly
- IMAGE_PROMPT column
- validation

## Phase 6 — Build Visual Prompt Refiner

Build only after Campaign Content Generator row contract is stable.

The specialist may refine creative execution but may not change SKU facts, audience, objective, campaign role, offer, or claim policy.

## Phase 7 — Pilot Campaign

Pilot at least one representative SKU with approximately 30 rows and complete human review.

## Phase 8 — Portfolio Scale

Expand test coverage and production use across all 24 SKUs, while keeping product truth in `marketing-plan/` and execution logic in `marketing-content-os/`.

## Release Rule

Release sequence:

**Contracts → Generator → Acceptance Test → Prompt Assembly → Visual Refiner → Pilot → 24-SKU Scale**
