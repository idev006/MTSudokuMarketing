#!/usr/bin/env python3
"""Compute acceptance batch metrics from canonical campaign TSV."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def load(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def angle_family(value: str) -> str:
    return (value or "").split(":", 1)[0].strip()


def max_conversion_streak(rows) -> int:
    best = cur = 0
    for r in rows:
        if r.get("CAMPAIGN_ROLE") == "CONVERSION":
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def duplicate_count(values) -> int:
    counts = Counter(v.strip() for v in values if v and v.strip())
    return sum(n - 1 for n in counts.values() if n > 1)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    args = p.parse_args()
    rows = load(args.input)
    if not rows:
        print("RESULT=FAIL reason=no rows")
        return 1

    visual = Counter(r.get("VISUAL_TYPE", "") for r in rows)
    angles = Counter(angle_family(r.get("MARKETING_ANGLE", "")) for r in rows)
    top_visual, top_visual_n = visual.most_common(1)[0]
    top_angle, top_angle_n = angles.most_common(1)[0]

    seq = []
    for r in rows:
        try:
            seq.append(int(r.get("SEQUENCE", "")))
        except ValueError:
            pass

    print(f"row_count_actual={len(rows)}")
    print(f"unique_row_id_count={len(set(r.get('ROW_ID','') for r in rows))}")
    print(f"campaign_id_count={len(set(r.get('CAMPAIGN_ID','') for r in rows))}")
    print(f"sequence_min={min(seq) if seq else 'NA'}")
    print(f"sequence_max={max(seq) if seq else 'NA'}")
    print(f"direct_sale_max_consecutive={max_conversion_streak(rows)}")
    print(f"top_angle={top_angle}")
    print(f"top_angle_share={top_angle_n/len(rows):.1%}")
    print(f"top_visual_type={top_visual}")
    print(f"top_visual_type_share={top_visual_n/len(rows):.1%}")
    print(f"duplicate_hook_count={duplicate_count(r.get('HOOK','') for r in rows)}")
    print(f"repeated_cta_exact_count={duplicate_count(r.get('CTA','') for r in rows)}")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
