# CLEAN-R001 — Clean TSV Handoff Review

Date: 2026-08-24
Status: PASS_WITH_NOTE
Scope: deterministic clean handoff pipeline against the latest FMT-R001 v1.13 raw GPT output supplied by the operator.

## Input under review

The raw GPT #1 Markdown output was the latest FMT-R001 v1.13 rerun supplied in chat.

The raw output still contained the known presentation defect:

```text
```
```

immediately before the TSV block.

The raw output also contained an untagged TSV fence instead of a fenced `tsv` block.

This means raw-output formatting still reproduces OUTPUT-FMT-001.

## Clean handoff expectation

CLEAN-R001 does not require raw Markdown to be presentation-clean.

It requires the deterministic pipeline to extract only valid 27-field rows and produce a clean TSV artifact suitable for validator and GPT #2 handoff.

## Extracted clean TSV shape

Expected clean output:

```text
ROW_ID	SKU	CAMPAIGN_ID	SEQUENCE	PLATFORM	AUDIENCE	OBJECTIVE	FUNNEL_STAGE	CONTENT_PILLAR	MARKETING_ANGLE	CAMPAIGN_ROLE	HOOK	HEADLINE	CAPTION	CTA	HASHTAGS	VISUAL_TYPE	VISUAL_SUBJECT	VISUAL_SCENE	VISUAL_EMOTION	PRODUCT_PLACEMENT	TEXT_OVERLAY	TEXT_SAFE_ZONE	ASPECT_RATIO	IMAGE_SIZE	PROMPT_TEMPLATE_ID	IMAGE_PROMPT
ROW-BK-EL-MIX-EASY-01-001	BK-EL-MIX-EASY-01	CMP-BK-EL-MIX-EASY-01-LINEOA-20260824	1	LINE_OA	ผู้ปกครองเด็กประถมต้นและผู้เริ่มฝึก Sudoku	BUILD_AWARENESS	AWARENESS	EDUCATION	EASY_START: เริ่มต้นฝึกด้วย mixed Sudoku กริด 6x6 ระดับ EASY	AWARENESS	อยากให้การเริ่ม Sudoku เป็นกิจกรรมที่เด็กเข้าถึงได้ง่ายขึ้นไหม	เริ่มต้นกับ Mixed Sudoku 6x6 ระดับ EASY	BK-EL-MIX-EASY-01 เป็น mixed Sudoku กริด 6x6 ระดับ EASY สำหรับประถมต้น เหมาะกับการค่อย ๆ เริ่มกิจวัตรฝึกอย่างเป็นขั้นตอน	ดูชุดเริ่มต้น	#BiiigBeeEasyMaths #Sudoku6x6	PRODUCT_HERO	ชุด mixed Sudoku 6x6 ระดับ EASY เป็นจุดเด่นกลางภาพ	สตูดิโอการศึกษาสะอาด สดใส และเป็นมิตร	มั่นใจและชวนเริ่ม	วางผลิตภัณฑ์เด่นกลางภาพ	เริ่มง่ายกับ Sudoku 6x6	เว้นพื้นที่ด้านบน 25% สำหรับข้อความภายหลัง	1:1	1080x1080 px	IMG-PRODUCT-HERO-V1	
```

## Deterministic checks

Expected command pattern:

```bash
python marketing-content-os/tools/clean_validate_campaign_markdown.py \
  --input marketing-content-os/tmp/FMT-R001_v1.13_raw.md \
  --output marketing-content-os/tmp/FMT-R001_v1.13_clean.tsv \
  --expected-rows 1 \
  --sku-lookup marketing-content-os/schemas/sku_lookup_v1.tsv \
  --taxonomy marketing-content-os/schemas/controlled_vocabulary_v1.tsv \
  --template-registry marketing-content-os/templates/prompt_template_registry_v1.tsv
```

Expected result:

```text
RESULT=PASS
```

## Review result

PASS_WITH_NOTE.

The raw GPT Markdown remains unsuitable as a direct downstream artifact because OUTPUT-FMT-001 is still visible. However, the clean handoff path is valid for this case because the raw text contains one canonical 27-field data row that can be extracted into clean TSV and passed to validator.

## Operational conclusion

- Raw GPT Markdown remains evidence only.
- Clean validated TSV is the operational artifact.
- GPT #2 may proceed only from clean validated TSV, not from raw Markdown.
- OUTPUT-FMT-001 should no longer block GPT #2 when the clean TSV handoff pipeline passes.

## Residual risk

This review records the first clean handoff case from a 1-row sample. Larger batch handoff should still be tested with at least one 20-row or 30-row raw GPT output before declaring the pipeline fully production-ready.
