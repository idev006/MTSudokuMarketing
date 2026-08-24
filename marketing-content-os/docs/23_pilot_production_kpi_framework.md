# Pilot Production KPI Framework — Social Media Content Pipeline

Status: ACTIVE_DRAFT_FOR_PILOT
Effective date: 2026-08-24
Scope: BiiigBee Easy Maths social media content production using GPT #1 Campaign Content Generator, Clean TSV pipeline, GPT #2 Visual Prompt Refiner, image generation, and human review.

## 1. Strategic objective

The pilot production objective is to create a repeatable social media content pipeline that reduces content creation time while preserving marketing quality, product truth, claim safety, and visual consistency.

The pipeline must produce post-ready social media content packages that include:

- approved campaign row source;
- final caption/copy;
- hook/headline;
- CTA;
- hashtags;
- visual direction;
- final image-generation prompt or image handoff;
- generated image candidate;
- human review status;
- publish decision.

## 2. Operating principle

The pilot is not a fully autonomous publishing system.

Approved operating flow:

```text
GPT #1 Campaign Content Generator
→ deterministic clean TSV extraction and validation
→ GPT #2 Visual Prompt Refiner
→ final post package assembly
→ image generation
→ human review
→ approved social media post
```

Raw GPT #1 output is evidence only. The operational handoff artifact is the clean validated 27-field TSV row.

GPT #2 must receive only clean validated 27-field rows or clearly marked test inputs.

## 3. Pilot production goal

### 7-day pilot goal

The first pilot cycle must target:

- 10 post-ready packages;
- 3 generated image candidates;
- 3 publish-ready social media posts;
- 1 measurable baseline for time, quality, and rework;
- 1 repeatable SOP for future batches.

### Daily pilot target

- generate 10–20 campaign rows;
- refine 5–10 rows;
- create 1–3 generated image candidates;
- approve 1–3 post-ready packages.

## 4. Core pipeline KPIs

### 4.1 System reliability KPIs

| KPI | Target | Measurement |
|---|---:|---|
| Row validity rate | >= 98% | Valid rows / rows generated after deterministic validation |
| Clean extraction success rate | >= 99% | Clean TSV outputs that pass extraction / raw GPT #1 outputs processed |
| 27-field schema compliance | 100% | Rows with exactly canonical 27 fields |
| Template mapping accuracy | 100% | VISUAL_TYPE to PROMPT_TEMPLATE_ID mapping correctness |
| SKU truth accuracy | 100% | No SKU, grade, difficulty, grid, puzzle-count, format, answer-key contradiction |
| Unsafe claim escape rate | 0 | Unsafe claims that reach final post package |
| Named-variant overclaim escape rate | 0 | Standard SKU named variant claims without approved exact composition |

### 4.2 GPT #1 KPIs

| KPI | Target | Notes |
|---|---:|---|
| Required-input fail-safe accuracy | 100% | Missing SKU or NUMBER_OF_ROWS must fail safely |
| Controlled vocabulary compliance | >= 99% | PLATFORM, OBJECTIVE, FUNNEL_STAGE, CONTENT_PILLAR, CAMPAIGN_ROLE, VISUAL_TYPE |
| Campaign diversity pass rate | >= 90% | Visual type/angle/conversion streak constraints |
| Stable campaign ID rate | 100% | One campaign ID per generated campaign batch |
| Global sequence correctness | 100% | SEQUENCE must be contiguous 1..N |
| Raw output direct-use readiness | Not required | Raw Markdown formatting remains non-operational; cleaner is required |

### 4.3 Clean TSV pipeline KPIs

| KPI | Target | Notes |
|---|---:|---|
| Extraction success | >= 99% | Extract canonical rows from raw Markdown |
| Validator pass rate | >= 98% | After extraction |
| Zero-row extraction incident rate | <= 1% | Must block GPT #2 handoff |
| Duplicate row ID escape rate | 0 | Must be blocked |
| Blank IMAGE_PROMPT in formula mode | 100% | GPT #1 v1 mode |

### 4.4 GPT #2 KPIs

| KPI | Target | Notes |
|---|---:|---|
| Locked strategy preservation | 100% | Must not silently edit AUDIENCE, OBJECTIVE, FUNNEL_STAGE, CONTENT_PILLAR, MARKETING_ANGLE, CAMPAIGN_ROLE |
| Product truth preservation | 100% | No invented product facts |
| Unsafe refinement rejection accuracy | 100% | Promotion, guarantee, official/competition claims |
| Template mismatch detection | >= 99% | Wrong PROMPT_TEMPLATE_ID must be flagged |
| Incomplete row fail-safe | 100% | Must not infer or fabricate missing fields |
| Valid visual refinement usefulness | >= 85% | Human reviewer marks refinement useful or directly usable |
| Template handoff completeness | >= 90% | Handoff has final copy and image prompt or clearly identifies blocker |

### 4.5 Image-generation KPIs

| KPI | Target | Notes |
|---|---:|---|
| Prompt usability rate | >= 80% | Prompt produces a usable candidate without full rewrite |
| First image pass rate | >= 60% | First generated candidate needs no major regeneration |
| Visual safety pass rate | 100% | No fake official logos, misleading packaging, forbidden text, unsafe claims |
| Brand/quality acceptance | >= 80% | Human reviewer approves style as premium/parent-friendly |
| Text-in-image violation rate | 0 | When prompt says no Thai text in image |
| Misleading physical product implication rate | 0 | Especially PRODUCT_BOX and PRODUCT_HERO |

### 4.6 Business/productivity KPIs

| KPI | Target | Measurement |
|---|---:|---|
| Time reduction vs manual workflow | 60–80% | Compare brief-to-post-ready time |
| Average row-to-post package time | <= 15 minutes | From clean row to post package |
| Average prompt-to-usable-image time | <= 10 minutes | From approved image prompt to usable image candidate |
| Cost per usable post reduction | >= 50% | Compared to manual baseline |
| First-pass post approval rate | >= 70% pilot; >= 80% after stabilization | Reviewer approves with minor/no edits |
| Publish-ready rate | >= 70% | Final packages accepted for scheduling/posting |
| Batch throughput | 10–20 rows/day; 3–8 image candidates/day | Pilot working rate |

## 5. Readiness scoring model

### 5.1 GPT #1 scoring

| Dimension | Weight |
|---|---:|
| Input validation and fail-safe | 20 |
| 27-field row schema accuracy | 20 |
| Product truth and claim safety | 20 |
| Campaign strategy quality | 15 |
| Visual-template mapping | 10 |
| Output handoff reliability | 15 |
| Total | 100 |

Current pilot score:

- GPT #1 raw output direct-use readiness: 89/100
- GPT #1 with Clean TSV pipeline: 96/100

Operational verdict: GPT #1 is pilot-ready only when paired with the Clean TSV pipeline.

### 5.2 GPT #2 scoring

| Dimension | Weight |
|---|---:|
| Strategy lock discipline | 20 |
| Product truth preservation | 20 |
| Visual refinement quality | 20 |
| Fail-safe / return-upstream behavior | 15 |
| Template logic / mapping review | 10 |
| Claim and promotion safety | 10 |
| Handoff usability | 5 |
| Total | 100 |

Current pilot score:

- GPT #2 Visual Prompt Refiner: 95/100

Operational verdict: GPT #2 is pilot-ready for visual review/refinement when input is clean validated 27-field rows.

### 5.3 Full-pipeline score

Current full-pipeline pilot readiness:

- GPT #1 + Clean TSV pipeline + GPT #2 + human review: 95/100

Operational verdict: ready for controlled pilot production. Not approved for fully autonomous publishing.

## 6. Definition of Done for one post package

A post package is publish-ready only when all of the following are present and reviewed:

- source ROW_ID and SKU;
- validated product truth;
- final caption;
- hook/headline;
- CTA;
- hashtags;
- approved visual direction;
- final image prompt or image-generation handoff;
- generated image candidate;
- human review result;
- final publish/schedule decision.

A package is not publish-ready if it has any unresolved product truth, offer, template, visual safety, or missing-field blocker.

## 7. Review gates

### Gate A — GPT #1 output gate

Pass only if:

- clean TSV extraction succeeds;
- deterministic validator passes;
- row count is correct;
- SKU and controlled vocabulary are valid;
- IMAGE_PROMPT is blank in formula mode;
- no unsafe product or promotion claim is present.

### Gate B — GPT #2 visual handoff gate

Pass only if:

- GPT #2 preserves locked strategy fields;
- template mapping is valid;
- visual refinements do not change product truth;
- unsafe claims are rejected;
- blockers are identified rather than guessed;
- final prompt is assembled only from approved row/template/lookup facts.

### Gate C — Image candidate gate

Pass only if:

- image follows requested aspect ratio and safe space;
- image does not render forbidden Thai headline text when prohibited;
- product representation is not misleading physical shipping packaging;
- no fake official logos, medals, certificates, or competition affiliation;
- no distorted, unreadable, or claim-bearing Sudoku elements;
- visual quality is suitable for BiiigBee Easy Maths brand.

### Gate D — Final social post gate

Pass only if:

- caption and visual match the same strategy intent;
- CTA is supported and safe;
- no unsupported promotion/deadline/discount exists;
- final package has reviewer approval;
- post is assigned to a platform and campaign.

## 8. Pilot content mix

Recommended first pilot batch of 10 post packages:

| Visual/content type | Count | Purpose |
|---|---:|---|
| PRODUCT_HERO | 3 | Product awareness and recognition |
| BENEFIT / STUDENT_ACTIVITY | 3 | Parent benefit and learning confidence |
| PRODUCT_BOX digital mockup | 2 | Product visualization / marketplace-style asset |
| PUZZLE_CHALLENGE or INFOGRAPHIC | 1 | Engagement / education |
| COMPETITION_PREPARATION | 1 | Competition-safe training positioning |

For the first 3 publish-ready posts, prioritize:

1. PRODUCT_HERO;
2. BENEFIT or STUDENT_ACTIVITY;
3. PRODUCT_BOX digital mockup.

## 9. Traffic-light operating status

| Area | Status | Meaning |
|---|---|---|
| GPT #1 raw output direct use | Yellow | Not operational without cleaner |
| GPT #1 with cleaner | Green | Pilot-ready |
| GPT #2 visual review/refinement | Green | Pilot-ready |
| Full pipeline with human review | Green | Controlled pilot-ready |
| Fully autonomous publishing | Red | Not recommended |

## 10. Pilot reporting cadence

During the first pilot week, report daily:

- rows generated;
- rows validated;
- rows sent to GPT #2;
- post packages assembled;
- images generated;
- images approved;
- post packages approved;
- average time per package;
- rework reasons;
- unsafe-claim or truth incidents.

Weekly pilot review must decide one of:

- continue pilot;
- expand to more SKUs;
- freeze SOP v1;
- patch GPT instructions or templates;
- block production scale-up due to quality or safety issue.

## 11. Non-negotiable constraints

The pipeline must not:

- use raw GPT #1 Markdown as production artifact;
- send incomplete or unvalidated rows to GPT #2 for production handoff;
- allow GPT #2 to rewrite locked strategy fields silently;
- add unsupported discounts, deadlines, scarcity, price, awards, reviews, or guarantees;
- claim official endorsement or official competition affiliation;
- claim named variant composition for Standard SKUs without approved exact composition;
- publish without human review during pilot.

## 12. Immediate next action

Start Pilot Batch 001 using:

```text
SKU: BK-UP-MIX-EASY-01
NUMBER_OF_ROWS: 10
PLATFORM: AUTO
CAMPAIGN_GOAL: AUTO
```

Then select 3 rows for first image production:

- one PRODUCT_HERO;
- one BENEFIT or STUDENT_ACTIVITY;
- one PRODUCT_BOX digital mockup.

Record row-level timing and review outcomes for KPI baseline.
