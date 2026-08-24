from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SUPPORTED_INPUT_SUFFIXES = {".md", ".txt", ".text"}


@dataclass(frozen=True)
class CleanResult:
    raw_file: Path
    clean_file: Path
    report_file: Path
    status: str
    extracted_rows: int
    expected_rows: int
    exit_code: int
    message: str


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "marketing-content-os" / "tools" / "clean_validate_campaign_markdown.py").exists():
            return candidate
    raise RuntimeError("Repository root not found. Run from inside MTSudokuMarketing.")


def discover_raw_files(input_folder: Path) -> list[Path]:
    if not input_folder.exists() or not input_folder.is_dir():
        raise ValueError(f"Input folder not found: {input_folder}")

    ignored_parts = {"_cleaned", "clean", "reports", "selected", "handoff", "images", "final"}
    files: list[Path] = []
    for path in sorted(input_folder.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        files.append(path)
    return files


def _read_report(report_file: Path) -> dict:
    try:
        return json.loads(report_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def clean_one_file(
    raw_file: Path,
    *,
    repo_root: Path,
    output_root: Path,
    expected_rows: int,
    allow_visual_concentration: bool = False,
    allow_angle_concentration: bool = False,
) -> CleanResult:
    safe_stem = raw_file.stem
    clean_dir = output_root / "clean"
    report_dir = output_root / "reports"
    clean_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    clean_file = clean_dir / f"{safe_stem}_clean.tsv"
    report_file = report_dir / f"{safe_stem}_clean_report.json"

    tool = repo_root / "marketing-content-os" / "tools" / "clean_validate_campaign_markdown.py"
    cmd = [
        sys.executable,
        str(tool),
        "--raw-input",
        str(raw_file),
        "--clean-output",
        str(clean_file),
        "--expected-rows",
        str(expected_rows),
        "--sku-lookup",
        str(repo_root / "marketing-content-os" / "schemas" / "sku_lookup_v1.tsv"),
        "--taxonomy",
        str(repo_root / "marketing-content-os" / "schemas" / "controlled_vocabulary_v1.tsv"),
        "--template-registry",
        str(repo_root / "marketing-content-os" / "templates" / "prompt_template_registry_v1.tsv"),
        "--report",
        str(report_file),
    ]
    if allow_visual_concentration:
        cmd.append("--allow-visual-concentration")
    if allow_angle_concentration:
        cmd.append("--allow-angle-concentration")

    completed = subprocess.run(cmd, cwd=str(repo_root), text=True, capture_output=True, check=False)
    report = _read_report(report_file)
    extracted_rows = int(report.get("extracted_rows", 0) or 0)
    status = "PASS" if completed.returncode == 0 else "FAIL"
    message = (completed.stdout + completed.stderr).strip()

    return CleanResult(
        raw_file=raw_file,
        clean_file=clean_file,
        report_file=report_file,
        status=status,
        extracted_rows=extracted_rows,
        expected_rows=expected_rows,
        exit_code=completed.returncode,
        message=message,
    )


def clean_folder(
    input_folder: Path,
    *,
    expected_rows: int = 10,
    output_folder: Path | None = None,
    allow_visual_concentration: bool = False,
    allow_angle_concentration: bool = False,
) -> list[CleanResult]:
    repo_root = find_repo_root()
    raw_files = discover_raw_files(input_folder)
    output_root = output_folder or (input_folder / "_cleaned")
    output_root.mkdir(parents=True, exist_ok=True)

    results: list[CleanResult] = []
    for raw_file in raw_files:
        results.append(
            clean_one_file(
                raw_file,
                repo_root=repo_root,
                output_root=output_root,
                expected_rows=expected_rows,
                allow_visual_concentration=allow_visual_concentration,
                allow_angle_concentration=allow_angle_concentration,
            )
        )
    return results


def build_gpt2_template(row_text: str) -> str:
    return (
        "MODE: TEMPLATE_HANDOFF\n\n"
        "GOAL:\n"
        "Create final social media post copy and image-generation handoff for this approved row. "
        "Preserve product truth and strategy. Do not add unsupported claims. "
        "IMAGE_PROMPT may be assembled from approved fields and template logic.\n\n"
        "INPUT_ROW:\n"
        f"{row_text.strip()}\n"
    )


def read_clean_rows(clean_file: Path) -> list[str]:
    lines = clean_file.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.startswith("ROW-")]
