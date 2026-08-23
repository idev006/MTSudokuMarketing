# 15 — GPT v1 Acceptance Test Plan

## Release Target
BiiigBee Campaign Content Generator v1.0

## Test Corpus
Use `tests/campaign_content_generator_acceptance_corpus_v1.tsv`, currently expanded through TC-032.

## Gate 1 — Input Handling
Pass when:
- General Mode works with SKU + row count only
- missing SKU / row count blocks safely
- AUTO platform resolves to one canonical primary platform
- AUTO duration does not assume one row equals one day
- Advanced Mode remains the same engine plus safe overrides
- invalid SKU produces zero fabricated rows

## Gate 2 — Product Truth
For representative Standard and Competition SKUs:
- SKU, grade band, difficulty, audience, purpose, positioning, product facts and claims match source of truth
- no invented pricing, promotion, testimonial, stock, scarcity or official affiliation
- Tier-1 data conflict blocks generation instead of silent guessing

## Gate 3 — Schema / Serialization
For N = 1, 5, 20, 30 and 60:
- exact total row count
- unique ROW_ID
- continuous global SEQUENCE 1..N
- stable CAMPAIGN_ID
- exact canonical 27-column order
- one physical TSV line per row
- exactly 27 fields per data line
- embedded tabs/newlines serialized per v1 contract
- IMAGE_PROMPT final and blank in Formula Mode

## Gate 4 — Controlled Vocabulary
Structured fields must use canonical taxonomy. `AUTO` must not remain in row output. Unknown structured synonyms fail deterministic validation.

## Gate 5 — Campaign Coherence / Diversity
- rows form a logical campaign arc
- content roles are not random
- audience/objective/funnel/pillar/angle are mutually consistent
- no >2 direct-sale rows consecutively
- hooks/CTA/caption structures vary
- angle/visual concentration respects targets when practical unless explicitly overridden
- medium batches should demonstrate useful visual-family diversity

## Gate 6 — Claim Safety
Competition tests must contain no real-exam claim, official endorsement without evidence, guaranteed result, fake award, or fake urgency.

## Gate 7 — Prompt Infrastructure
- every VISUAL_TYPE maps to an approved registered template
- unknown template IDs are rejected
- product-owned placeholders resolve via SKU lookup
- all ten v1 template families are available
- downstream assembly leaves no unresolved `{{PLACEHOLDER}}`

## Gate 8 — Provenance
- output metadata comes from `knowledge_manifest_v1.yaml`
- MARKETING_PLAN_REF is not invented
- schema/taxonomy/template versions are recorded outside the 27 row columns

## Gate 9 — Large Batch
For N>20:
- campaign planned globally before chunking
- chunks contain at most 20 rows
- exact total N rows across all chunks
- stable CAMPAIGN_ID
- global SEQUENCE has no gaps/duplicates
- full-batch diversity remains valid

## Gate 10 — Human Usability
A non-marketing operator should be able to create a useful campaign without understanding funnels, pillars, prompt engineering or template lookup internals.

## Validation Model
Production release requires both:
1. independent deterministic checks from `docs/21_deterministic_validator_spec.md`
2. semantic/human review for copy quality, campaign coherence, appropriateness and claim nuance

GPT self-validation alone is insufficient for Production v1.0.

## Release Decision
- `PASS`: all deterministic hard gates pass and semantic review acceptable
- `PASS_WITH_WARNING`: no truth/safety/schema hard failure; non-blocking quality/provenance tuning remains
- `FAIL`: any fabricated product/commercial fact, unsafe claim, invalid SKU behavior, wrong row/schema/serialization, invalid template, unresolved hard prompt dependency, or material campaign incoherence

## Build Sequence
1. freeze contracts
2. complete production-readiness hardening
3. build GPT candidate
4. run TC-001..TC-032
5. classify/fix owning source
6. rerun affected + regression tests
7. release Generator v1.0 only after hard gates pass
8. build Visual Prompt Refiner against the stable contract
