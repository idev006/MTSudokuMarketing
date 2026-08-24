#!/usr/bin/env python3
"""Clean and validate Campaign Content Generator Markdown output.

This is the deterministic production handoff wrapper for GPT #1 raw Markdown.
It extracts canonical 27-field TSV rows from raw GPT output, ignores empty or
untagged Markdown fences, writes a clean TSV artifact, and runs the existing
machine validator on that clean TSV.

The intended production handoff is the clean validated TSV file, not raw GPT
Markdown. Raw Markdown can still be archived as evidence.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from extract_tsv_from_markdown import HEADER, extract


def count_empty_fences(text: str) -> int:
    """Count empty generic Markdown code fences.

    This detects the recurring OUTPUT-FMT-001 shape:
    ```
    ```
    with only whitespace between the fences.
    """
    count = 0
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip() == "```" and lines[i + 1].strip() == "```":
            count += 1
            i += 2
        else:
            i += 1
    return count


def count_untagged_fences(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() == "```")


def write_clean_tsv(rows: list[str], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(HEADER + "\n" + "\n".join(rows) + "\n", encoding="utf-8")


def run_validator(args: argparse.Namespace) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(Path(__file__).with_name("validate_campaign_output.py")),
        "--input",
        str(args.clean_output),
        "--expected-rows",
        str(args.expected_rows),
        "--sku-lookup",
        str(args.sku_lookup),
        "--taxonomy",
        str(args.taxonomy),
        "--template-registry",
        str(args.template_registry),
    ]
    if args.allow_visual_concentration:
        cmd.append("--allow-visual-concentration")
    if args.allow_angle_concentration:
        cmd.append("--allow-angle-concentration")
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--raw-input", type=Path, required=True, help="Raw GPT Markdown/text output")
    p.add_argument("--clean-output", type=Path, required=True, help="Clean canonical TSV artifact")
    p.add_argument("--expected-rows", type=int, required=True)
    p.add_argument("--sku-lookup", type=Path, required=True)
    p.add_argument("--taxonomy", type=Path, required=True)
    p.add_argument("--template-registry", type=Path, required=True)
    p.add_argument("--report", type=Path, default=None, help="Optional JSON report path")
    p.add_argument("--allow-visual-concentration", action="store_true")
    p.add_argument("--allow-angle-concentration", action="store_true")
    return p


def main() -> int:
    args = build_parser().parse_args()
    text = args.raw_input.read_text(encoding="utf-8")
    rows = extract(text)

    report = {
        "raw_input": str(args.raw_input),
        "clean_output": str(args.clean_output),
        "expected_rows": args.expected_rows,
        "extracted_rows": len(rows),
        "raw_empty_generic_fences": count_empty_fences(text),
        "raw_untagged_fence_lines": count_untagged_fences(text),
        "clean_tsv_written": False,
        "validator_exit_code": None,
        "validator_stdout": "",
        "validator_stderr": "",
        "result": "FAIL",
    }

    if not rows:
        print("RESULT=FAIL reason=no canonical 27-field rows found")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 1

    write_clean_tsv(rows, args.clean_output)
    report["clean_tsv_written"] = True

    validator = run_validator(args)
    report["validator_exit_code"] = validator.returncode
    report["validator_stdout"] = validator.stdout
    report["validator_stderr"] = validator.stderr
    report["result"] = "PASS" if validator.returncode == 0 else "FAIL"

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"EXTRACTED_ROWS={len(rows)}")
    print(f"RAW_EMPTY_GENERIC_FENCES={report['raw_empty_generic_fences']}")
    print(f"RAW_UNTAGGED_FENCE_LINES={report['raw_untagged_fence_lines']}")
    print(validator.stdout, end="")
    if validator.stderr:
        print(validator.stderr, file=sys.stderr, end="")
    print(f"CLEAN_TSV={args.clean_output}")
    print(f"RESULT={report['result']}")
    return validator.returncode


if __name__ == "__main__":
    raise SystemExit(main())
