# 16 — Controlled Vocabulary / Canonical Taxonomy v1

## Purpose
Marketing Content OS produces structured marketing data, not arbitrary labels. Fields used for analytics, validation, filtering, and downstream automation must use canonical values.

## FUNNEL_STAGE
Allowed values:
- `AWARENESS`
- `CONSIDERATION`
- `CONVERSION`
- `RETENTION`

## CAMPAIGN_ROLE
Allowed values:
- `AWARENESS`
- `EDUCATION`
- `PROBLEM_SOLUTION`
- `ENGAGEMENT`
- `PRODUCT_BENEFIT`
- `USE_CASE`
- `TRUST`
- `CONVERSION`
- `REMINDER`
- `CROSS_SELL`

## VISUAL_TYPE
Allowed values:
- `PRODUCT_HERO`
- `LIFESTYLE`
- `PARENT_CHILD`
- `STUDENT_ACTIVITY`
- `TEACHER_CLASSROOM`
- `PUZZLE_CHALLENGE`
- `BENEFIT`
- `INFOGRAPHIC`
- `COMPETITION`
- `PRODUCT_BOX`

Each VISUAL_TYPE maps one-to-one to an approved `PROMPT_TEMPLATE_ID` family unless a later schema version explicitly permits another mapping.

## OBJECTIVE
Canonical families:
- `BUILD_AWARENESS`
- `EDUCATE`
- `CREATE_ENGAGEMENT`
- `SHOW_PRODUCT_VALUE`
- `BUILD_TRUST`
- `DRIVE_CONSIDERATION`
- `DRIVE_CONVERSION`
- `RETENTION_CROSS_SELL`

## CONTENT_PILLAR
Canonical families:
- `EDUCATION`
- `PARENT_TEACHER_INSIGHT`
- `SKILL_DEVELOPMENT`
- `CHALLENGE_ENGAGEMENT`
- `PRODUCT_BENEFIT`
- `USE_CASE`
- `TRUST_CONFIDENCE`
- `COMPETITION_PREPARATION`
- `OFFER_CONVERSION`
- `PORTFOLIO_PROGRESSION`

## MARKETING_ANGLE
MARKETING_ANGLE remains more flexible than the fields above, but each row must assign one canonical family plus optional human-readable detail.

Canonical families:
- `EASY_START`
- `SKILL_PROGRESS`
- `LOGIC_TRAINING`
- `FOCUS_ACCURACY`
- `CHALLENGE_MASTERY`
- `VARIETY_MIX`
- `PARENT_CONFIDENCE`
- `TEACHER_UTILITY`
- `PRINTABLE_CONVENIENCE`
- `500_PUZZLE_VALUE`
- `COMPETITION_PREPARATION`
- `PORTFOLIO_NEXT_STEP`

Recommended serialization: `FAMILY: short detail`, e.g. `SKILL_PROGRESS: จากพื้นฐานสู่โจทย์ระดับกลาง`.

## PLATFORM
Canonical v1 values:
- `FACEBOOK`
- `LINE_OA`
- `MARKETPLACE`
- `LANDING_PAGE`

`AUTO` is an input value, not an output PLATFORM value. In General Mode, `PLATFORM=AUTO` resolves to one primary canonical platform for the campaign using Marketing Plan channel strategy. Multi-platform generation requires Advanced Mode `PLATFORM_MIX`.

## Governance
- Do not invent synonyms for controlled fields.
- Human-facing copy may use natural language freely.
- Schema/taxonomy version must change before adding or renaming canonical values.
- Validator must reject non-canonical values in controlled fields.
