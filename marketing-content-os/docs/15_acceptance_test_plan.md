# 15 — GPT v1 Acceptance Test Plan

## Release Target
BiiigBee Campaign Content Generator v1.0

## Gate 1 — Input Handling
Pass when:
- General Mode works with SKU + number of rows only
- AUTO platform/goal defaults behave sensibly
- Advanced Mode overrides do not require a separate engine
- invalid SKU produces a validation error instead of fabricated data

## Gate 2 — Product Truth
For a representative set of Standard and Competition SKUs:
- SKU, grade band, difficulty, target, purpose, positioning, product facts, and claims match source of truth
- no invented pricing, promotion, testimonial, stock, or official affiliation

## Gate 3 — Batch Contract
For N = 1, 5, 20, 30 and 60:
- exact row count
- unique ROW_ID
- continuous sequence 1..N
- stable CAMPAIGN_ID
- all required columns present and ordered correctly
- IMAGE_PROMPT is final and blank in formula mode

## Gate 4 — Campaign Coherence
- rows form a logical campaign arc
- content roles are not random
- audience/objective/funnel/pillar/angle are mutually consistent
- conversion posts appear in context rather than dominating the batch

## Gate 5 — Diversity
- no more than 2 direct-sale rows consecutively
- hooks are materially different
- CTA and caption structures vary
- angle and visual-type concentration stay within target limits when mathematically practical

## Gate 6 — Claim Safety
Test especially Competition SKUs:
- no real-exam claim
- no official endorsement claim without verified data
- no guaranteed win/result claim
- wording stays in training/preparation territory

## Gate 7 — Visual Handoff
- every row has usable visual parameters
- PROMPT_TEMPLATE_ID is valid
- Visual Prompt Refiner can refine a row without changing marketing intent

## Gate 8 — Human Usability
A non-marketing user should be able to create a usable monthly campaign without understanding funnels, pillars, angles, or prompt engineering.

## Release Decision
- `PASS`: all hard gates pass; minor stylistic variation acceptable
- `PASS_WITH_WARNING`: no truth/safety/schema failures, but quality tuning remains
- `FAIL`: any fabricated product fact, unsafe claim, wrong row count/schema, invalid SKU handling, or material campaign incoherence

## Build Sequence
1. Freeze v1 contracts
2. Build Campaign Content Generator
3. Run acceptance corpus
4. Fix failures and re-run
5. Release Generator v1.0
6. Build Visual Prompt Refiner against the stable row contract
