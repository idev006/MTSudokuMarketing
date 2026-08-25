from __future__ import annotations

import csv
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

SUPPORTED_INPUT_SUFFIXES = {".md", ".txt", ".text"}
MIN_POST_COUNT = 1
MAX_POST_COUNT = 60
DEFAULT_POST_COUNT = 10

VISUAL_TYPE_PRIORITY = [
    "PRODUCT_HERO",
    "STUDENT_ACTIVITY",
    "PARENT_CHILD",
    "BENEFIT",
    "INFOGRAPHIC",
    "PUZZLE_CHALLENGE",
    "PRODUCT_BOX",
    "LIFESTYLE",
    "TEACHER_CLASSROOM",
    "COMPETITION",
]


@dataclass(frozen=True)
class CleanResult:
    raw_file: Path
    clean_file: Path
    report_file: Path
    selected_file: Path | None
    prompt_folder: Path | None
    summary_file: Path | None
    status: str
    extracted_rows: int
    expected_rows: int
    target_posts: int
    selected_rows: int
    prompt_files: int
    exit_code: int
    message: str
    next_action: str


@dataclass(frozen=True)
class PipelineBatchSummary:
    input_folder: Path
    output_root: Path
    raw_file_count: int
    pass_count: int
    fail_count: int
    target_posts_per_file: int
    selected_row_count: int
    prompt_file_count: int
    results: list[CleanResult] = field(default_factory=list)


def validate_post_count(value: int) -> int:
    if value < MIN_POST_COUNT or value > MAX_POST_COUNT:
        raise ValueError(f"Post count N must be between {MIN_POST_COUNT} and {MAX_POST_COUNT}. Got: {value}")
    return value


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "marketing-content-os" / "tools" / "clean_validate_campaign_markdown.py").exists():
            return candidate
    raise RuntimeError("Repository root not found. Run from inside MTSudokuMarketing.")


def discover_raw_files(input_folder: Path) -> list[Path]:
    if not input_folder.exists() or not input_folder.is_dir():
        raise ValueError(f"Input folder not found: {input_folder}")

    ignored_parts = {"_cleaned", "clean", "reports", "selected", "handoff", "prompts", "images", "final"}
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


def _read_tsv_dicts(tsv_file: Path) -> tuple[list[str], list[dict[str, str]]]:
    with tsv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = [dict(row) for row in reader]
        return list(reader.fieldnames or []), rows


def _write_tsv_dicts(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def recommend_rows(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    """Prepare up to N rows for GPT2 handoff.

    N is operator-defined and must be 1..60. In normal production the operator
    should ask GPT1 for NUMBER_OF_ROWS=N. After deterministic validation passes,
    this function prepares N rows for GPT2 using a stable and readable order.

    The first pass prioritizes VISUAL_TYPE diversity. The second pass fills any
    remaining slots from the original clean row order. This makes output useful
    immediately while still preserving the complete clean TSV for review.
    """
    validate_post_count(limit)
    selected: list[dict[str, str]] = []
    selected_ids: set[str] = set()

    for visual_type in VISUAL_TYPE_PRIORITY:
        for row in rows:
            row_id = row.get("ROW_ID", "")
            if row_id in selected_ids:
                continue
            if row.get("VISUAL_TYPE", "") == visual_type:
                selected.append(row)
                selected_ids.add(row_id)
                break
        if len(selected) >= limit:
            return selected

    for row in rows:
        row_id = row.get("ROW_ID", "")
        if row_id not in selected_ids:
            selected.append(row)
            selected_ids.add(row_id)
        if len(selected) >= limit:
            break
    return selected


def row_to_tsv_line(fieldnames: list[str], row: dict[str, str]) -> str:
    return "\t".join(row.get(field, "") for field in fieldnames)


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


def create_selected_outputs(
    clean_file: Path,
    output_root: Path,
    raw_stem: str,
    target_posts: int,
) -> tuple[Path, Path, Path, int, int]:
    target_posts = validate_post_count(target_posts)
    fieldnames, rows = _read_tsv_dicts(clean_file)
    selected = recommend_rows(rows, limit=target_posts)

    selected_file = output_root / "selected" / f"{raw_stem}_selected_{target_posts}.tsv"
    prompts_folder = output_root / "handoff" / raw_stem
    summary_file = output_root / "handoff" / f"{raw_stem}_handoff_index.tsv"

    _write_tsv_dicts(selected_file, fieldnames, selected)
    prompts_folder.mkdir(parents=True, exist_ok=True)

    prompt_records: list[dict[str, str]] = []
    prompt_files = 0
    for index, row in enumerate(selected, start=1):
        row_id = row.get("ROW_ID") or f"row_{index}"
        prompt_file = prompts_folder / f"{index:02d}_{row_id}_gpt2_prompt.txt"
        prompt = build_gpt2_template(row_to_tsv_line(fieldnames, row))
        prompt_file.write_text(prompt, encoding="utf-8")
        prompt_files += 1
        prompt_records.append(
            {
                "ORDER": str(index),
                "ROW_ID": row_id,
                "SKU": row.get("SKU", ""),
                "VISUAL_TYPE": row.get("VISUAL_TYPE", ""),
                "PROMPT_FILE": str(prompt_file),
                "NEXT_ACTION": "Paste this prompt into GPT2 Visual Prompt Refiner",
            }
        )

    _write_tsv_dicts(
        summary_file,
        ["ORDER", "ROW_ID", "SKU", "VISUAL_TYPE", "PROMPT_FILE", "NEXT_ACTION"],
        prompt_records,
    )
    return selected_file, prompts_folder, summary_file, len(selected), prompt_files


def clean_one_file(
    raw_file: Path,
    *,
    repo_root: Path,
    output_root: Path,
    expected_rows: int,
    target_posts: int,
    allow_visual_concentration: bool = False,
    allow_angle_concentration: bool = False,
) -> CleanResult:
    target_posts = validate_post_count(target_posts)
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

    selected_file: Path | None = None
    prompt_folder: Path | None = None
    summary_file: Path | None = None
    selected_rows = 0
    prompt_files = 0
    next_action = "Open report and fix before GPT2"

    if status == "PASS":
        try:
            selected_file, prompt_folder, summary_file, selected_rows, prompt_files = create_selected_outputs(
                clean_file, output_root, safe_stem, target_posts
            )
            if selected_rows < target_posts:
                next_action = f"Only {selected_rows}/{target_posts} prompts generated; inspect clean TSV"
            else:
                next_action = f"Use generated {prompt_files} GPT2 prompts"
        except Exception as exc:  # noqa: BLE001
            status = "FAIL"
            next_action = "Selected output generation failed; open report"
            message = f"{message}\nSelected output generation failed: {exc}"

    return CleanResult(
        raw_file=raw_file,
        clean_file=clean_file,
        report_file=report_file,
        selected_file=selected_file,
        prompt_folder=prompt_folder,
        summary_file=summary_file,
        status=status,
        extracted_rows=extracted_rows,
        expected_rows=expected_rows,
        target_posts=target_posts,
        selected_rows=selected_rows,
        prompt_files=prompt_files,
        exit_code=completed.returncode,
        message=message,
        next_action=next_action,
    )


def write_batch_summary(output_root: Path, summary: PipelineBatchSummary) -> Path:
    path = output_root / "pipeline_batch_summary.json"
    payload = {
        "input_folder": str(summary.input_folder),
        "output_root": str(summary.output_root),
        "raw_file_count": summary.raw_file_count,
        "pass_count": summary.pass_count,
        "fail_count": summary.fail_count,
        "target_posts_per_file": summary.target_posts_per_file,
        "selected_row_count": summary.selected_row_count,
        "prompt_file_count": summary.prompt_file_count,
        "results": [
            {
                "raw_file": str(result.raw_file),
                "status": result.status,
                "extracted_rows": result.extracted_rows,
                "expected_rows": result.expected_rows,
                "target_posts": result.target_posts,
                "selected_rows": result.selected_rows,
                "prompt_files": result.prompt_files,
                "clean_file": str(result.clean_file),
                "report_file": str(result.report_file),
                "selected_file": str(result.selected_file) if result.selected_file else "",
                "prompt_folder": str(result.prompt_folder) if result.prompt_folder else "",
                "summary_file": str(result.summary_file) if result.summary_file else "",
                "next_action": result.next_action,
            }
            for result in summary.results
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def clean_folder(
    input_folder: Path,
    *,
    expected_rows: int = DEFAULT_POST_COUNT,
    target_posts: int | None = None,
    output_folder: Path | None = None,
    allow_visual_concentration: bool = False,
    allow_angle_concentration: bool = False,
) -> PipelineBatchSummary:
    expected_rows = validate_post_count(expected_rows)
    target_posts = validate_post_count(target_posts if target_posts is not None else expected_rows)
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
                target_posts=target_posts,
                allow_visual_concentration=allow_visual_concentration,
                allow_angle_concentration=allow_angle_concentration,
            )
        )

    summary = PipelineBatchSummary(
        input_folder=input_folder,
        output_root=output_root,
        raw_file_count=len(raw_files),
        pass_count=sum(1 for result in results if result.status == "PASS"),
        fail_count=sum(1 for result in results if result.status != "PASS"),
        target_posts_per_file=target_posts,
        selected_row_count=sum(result.selected_rows for result in results),
        prompt_file_count=sum(result.prompt_files for result in results),
        results=results,
    )
    write_batch_summary(output_root, summary)
    return summary


def read_clean_rows(clean_file: Path) -> list[str]:
    lines = clean_file.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.startswith("ROW-")]


def read_first_prompt(prompt_folder: Path | None) -> str:
    if prompt_folder is None:
        return ""
    prompt_files = sorted(prompt_folder.glob("*_gpt2_prompt.txt"))
    if not prompt_files:
        return ""
    return prompt_files[0].read_text(encoding="utf-8")
