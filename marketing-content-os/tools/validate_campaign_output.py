#!/usr/bin/env python3
"""Deterministic validator for BiiigBee Campaign Content Generator v1 outputs.

Usage:
  python validate_campaign_output.py \
    --input output.tsv \
    --expected-rows 30 \
    --sku-lookup schemas/sku_lookup_v1.tsv \
    --taxonomy schemas/controlled_vocabulary_v1.tsv \
    --template-registry templates/prompt_template_registry_v1.tsv

This validator checks machine-verifiable hard gates only. Semantic/marketing review
remains a separate human/model gate.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

EXPECTED_COLUMNS = [
    "ROW_ID", "SKU", "CAMPAIGN_ID", "SEQUENCE", "PLATFORM", "AUDIENCE",
    "OBJECTIVE", "FUNNEL_STAGE", "CONTENT_PILLAR", "MARKETING_ANGLE",
    "CAMPAIGN_ROLE", "HOOK", "HEADLINE", "CAPTION", "CTA", "HASHTAGS",
    "VISUAL_TYPE", "VISUAL_SUBJECT", "VISUAL_SCENE", "VISUAL_EMOTION",
    "PRODUCT_PLACEMENT", "TEXT_OVERLAY", "TEXT_SAFE_ZONE", "ASPECT_RATIO",
    "IMAGE_SIZE", "PROMPT_TEMPLATE_ID", "IMAGE_PROMPT",
]

CONTROLLED_FIELDS = {"FUNNEL_STAGE", "CAMPAIGN_ROLE", "VISUAL_TYPE", "PLATFORM"}


def load_tsv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def load_allowed_taxonomy(path: Path):
    allowed = {}
    for row in load_tsv(path):
        allowed.setdefault(row["FIELD"], set()).add(row["VALUE"])
    return allowed


def load_template_registry(path: Path):
    registry = {}
    for row in load_tsv(path):
        if row.get("STATUS") == "APPROVED":
            registry[row["PROMPT_TEMPLATE_ID"]] = row["VISUAL_TYPE"]
    return registry


def load_valid_skus(path: Path):
    return {row["SKU"] for row in load_tsv(path) if row.get("SKU")}


def fail(errors, msg):
    errors.append(msg)


def validate(args):
    errors = []
    warnings = []

    raw_lines = args.input.read_text(encoding="utf-8").splitlines()
    if not raw_lines:
        return ["input is empty"], warnings

    header = raw_lines[0].split("\t")
    if header != EXPECTED_COLUMNS:
        fail(errors, "TSV header/order does not match canonical 27-column schema")

    for i, line in enumerate(raw_lines[1:], start=2):
        if line.count("\t") != 26:
            fail(errors, f"physical line {i} does not contain exactly 27 TSV fields")

    rows = load_tsv(args.input)
    if len(rows) != args.expected_rows:
        fail(errors, f"expected {args.expected_rows} rows, found {len(rows)}")

    if not rows:
        return errors, warnings

    row_ids = [r.get("ROW_ID", "") for r in rows]
    if any(not x for x in row_ids):
        fail(errors, "blank ROW_ID found")
    if len(set(row_ids)) != len(row_ids):
        fail(errors, "duplicate ROW_ID found")

    campaign_ids = {r.get("CAMPAIGN_ID", "") for r in rows}
    if "" in campaign_ids or len(campaign_ids) != 1:
        fail(errors, "single-campaign output must have one stable nonblank CAMPAIGN_ID")

    try:
        seq = [int(r.get("SEQUENCE", "")) for r in rows]
    except ValueError:
        fail(errors, "SEQUENCE contains non-integer values")
        seq = []
    if seq and seq != list(range(1, args.expected_rows + 1)):
        fail(errors, "SEQUENCE must be globally continuous 1..N in output order")

    valid_skus = load_valid_skus(args.sku_lookup)
    for i, row in enumerate(rows, start=1):
        if row.get("SKU") not in valid_skus:
            fail(errors, f"row {i}: SKU {row.get('SKU')!r} not present in approved SKU lookup")

    allowed = load_allowed_taxonomy(args.taxonomy)
    for i, row in enumerate(rows, start=1):
        for field in CONTROLLED_FIELDS:
            if field in allowed and row.get(field) not in allowed[field]:
                fail(errors, f"row {i}: {field}={row.get(field)!r} is outside canonical taxonomy")

    registry = load_template_registry(args.template_registry)
    for i, row in enumerate(rows, start=1):
        template_id = row.get("PROMPT_TEMPLATE_ID", "")
        visual_type = row.get("VISUAL_TYPE", "")
        if template_id not in registry:
            fail(errors, f"row {i}: unapproved/unknown PROMPT_TEMPLATE_ID {template_id!r}")
        elif registry[template_id] != visual_type:
            fail(errors, f"row {i}: template {template_id} maps to {registry[template_id]}, not {visual_type}")
        if row.get("IMAGE_PROMPT", "") != "":
            fail(errors, f"row {i}: IMAGE_PROMPT must be blank in v1 FORMULA mode")

    conversion_streak = 0
    for i, row in enumerate(rows, start=1):
        if row.get("CAMPAIGN_ROLE") == "CONVERSION":
            conversion_streak += 1
            if conversion_streak > 2:
                fail(errors, f"row {i}: more than 2 consecutive CONVERSION rows")
        else:
            conversion_streak = 0

    if not args.allow_visual_concentration and len(rows) >= 8:
        counts = Counter(r.get("VISUAL_TYPE") for r in rows)
        top_value, top_count = counts.most_common(1)[0]
        ratio = top_count / len(rows)
        if ratio > 0.25:
            fail(errors, f"VISUAL_TYPE concentration {top_value}={ratio:.1%} exceeds 25%")

    if not args.allow_angle_concentration and len(rows) >= 10:
        counts = Counter(r.get("MARKETING_ANGLE") for r in rows)
        top_value, top_count = counts.most_common(1)[0]
        ratio = top_count / len(rows)
        if ratio > 0.20:
            fail(errors, f"MARKETING_ANGLE concentration {top_value!r}={ratio:.1%} exceeds 20%")

    return errors, warnings


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--expected-rows", type=int, required=True)
    p.add_argument("--sku-lookup", type=Path, required=True)
    p.add_argument("--taxonomy", type=Path, required=True)
    p.add_argument("--template-registry", type=Path, required=True)
    p.add_argument("--allow-visual-concentration", action="store_true")
    p.add_argument("--allow-angle-concentration", action="store_true")
    return p


def main():
    args = build_parser().parse_args()
    errors, warnings = validate(args)
    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"RESULT=FAIL errors={len(errors)}")
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
