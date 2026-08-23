#!/usr/bin/env python3
"""Extract canonical campaign TSV rows from GPT Markdown output.

Ignores empty code fences and prose. Accepts multiple displayed chunks, each with the
canonical header, and emits one logical TSV dataset with a single header.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADER = "\t".join([
    "ROW_ID", "SKU", "CAMPAIGN_ID", "SEQUENCE", "PLATFORM", "AUDIENCE",
    "OBJECTIVE", "FUNNEL_STAGE", "CONTENT_PILLAR", "MARKETING_ANGLE",
    "CAMPAIGN_ROLE", "HOOK", "HEADLINE", "CAPTION", "CTA", "HASHTAGS",
    "VISUAL_TYPE", "VISUAL_SUBJECT", "VISUAL_SCENE", "VISUAL_EMOTION",
    "PRODUCT_PLACEMENT", "TEXT_OVERLAY", "TEXT_SAFE_ZONE", "ASPECT_RATIO",
    "IMAGE_SIZE", "PROMPT_TEMPLATE_ID", "IMAGE_PROMPT",
])


def extract(text: str) -> list[str]:
    blocks = re.findall(r"```(?:tsv)?\s*\n(.*?)```", text, flags=re.I | re.S)
    rows: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        for line in lines:
            if line == HEADER:
                continue
            if line.startswith("ROW-") and line.count("\t") == 26:
                rows.append(line)
    if not rows:
        # Fallback for plain-text pasted output outside code fences.
        for line in text.splitlines():
            if line.startswith("ROW-") and line.count("\t") == 26:
                rows.append(line)
    return rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True, help="GPT Markdown/text output")
    p.add_argument("--output", type=Path, required=True, help="Canonical TSV output")
    args = p.parse_args()

    text = args.input.read_text(encoding="utf-8")
    rows = extract(text)
    if not rows:
        print("RESULT=FAIL reason=no canonical 27-field rows found")
        return 1

    args.output.write_text(HEADER + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"RESULT=PASS rows={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
