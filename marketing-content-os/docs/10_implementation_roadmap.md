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

## Phase 2 — Build Campaign Content Generator v1.0 Implementation Package — COMPLETE

Created:
- production-ready system instructions
- GPT Builder configuration spec
- conversation starters
- source-of-truth / knowledge mapping
- General Mode interaction flow
- Advanced Mode interaction flow
- blocking/non-blocking input behavior
- deterministic output behavior
- v1 acceptance corpus
- acceptance execution rubric

Candidate release label:
**BiiigBee Campaign Content Generator v1.0-rc1**

## Phase 3 — Build / Validate Prompt Template Library — NEXT IN PARALLEL

Validate and expand reusable visual prompt families, including:
- Product Hero
- Lifestyle
- Parent-Child
- Student Activity
- Teacher/Classroom
- Puzzle Challenge
- Benefit / Infographic
- Competition
- Product Box

All template IDs used by Generator tests must resolve to an approved versioned template.

## Phase 4 — Acceptance Testing of Generator — NEXT

Run the acceptance corpus against:
- Standard + Competition SKUs
- N = 1, 5, 20, 30, 60 rows
- General Mode
- Advanced Mode overrides
- invalid SKU cases
- claim-safety cases
- diversity and campaign-coherence cases
- formula-mode IMAGE_PROMPT behavior

Record hard gates and diagnostic rubric scores.

Do not declare v1.0 production-ready if any hard truth/safety/schema gate fails.

## Phase 5 — Fix / Re-test Loop

For each material failure:
1. classify root cause: knowledge / instruction / schema / template / generation quality
2. fix the owning source rather than patching individual output rows
3. version changed contract/template/instruction where required
4. rerun affected tests plus regression set

## Phase 6 — Google Sheets Prompt Assembly

- placeholder mapping
- prompt-template version mapping
- formula assembly
- IMAGE_PROMPT column
- validation

## Phase 7 — Build Visual Prompt Refiner

Build only after Campaign Content Generator row contract is stable and hard-gate tests pass.

The specialist may refine creative execution but may not change SKU facts, audience, objective, campaign role, offer, or claim policy.

## Phase 8 — Pilot Campaign

Pilot at least one representative SKU with approximately 30 rows and complete human review.

## Phase 9 — Portfolio Scale

Expand production use across all 24 SKUs while keeping product truth in `marketing-plan/` and execution logic in `marketing-content-os/`.

## Release Rule

Release sequence:

**Contracts → Generator Implementation → Acceptance Test → Fix/Re-test → Prompt Assembly → Visual Refiner → Pilot → 24-SKU Scale**

Production v1.0 requires all hard gates to pass; before that use an RC label.
