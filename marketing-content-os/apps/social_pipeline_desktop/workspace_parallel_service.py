from __future__ import annotations

import json
import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

try:
    from .pipeline_service import (
        DEFAULT_POST_COUNT,
        MAX_POST_COUNT,
        MIN_POST_COUNT,
        PipelineBatchSummary,
        clean_folder,
        discover_raw_files,
        validate_post_count,
    )
except ImportError:
    from pipeline_service import (  # type: ignore
        DEFAULT_POST_COUNT,
        MAX_POST_COUNT,
        MIN_POST_COUNT,
        PipelineBatchSummary,
        clean_folder,
        discover_raw_files,
        validate_post_count,
    )


IGNORED_WORKSPACE_DIRS = {
    "_cleaned",
    "_ready_for_gpt2",
    "_diagnostics",
    "_runs",
    "clean",
    "reports",
    "selected",
    "handoff",
    "prompts",
    "images",
    "final",
    ".git",
    ".venv",
    "__pycache__",
}

READY_DIR_NAME = "_ready_for_gpt2"
READY_INDEX_NAME = "_gpt2_ready_index.tsv"
READY_README_NAME = "README_วิธีใช้.txt"
PARALLEL_SUMMARY_NAME = "_workspace_parallel_summary.json"
DIAGNOSTIC_DIR_NAME = "_diagnostics"
GENERATED_OUTPUT_DIRS = ("_cleaned", READY_DIR_NAME)


@dataclass(frozen=True)
class WorkspaceJob:
    sku: str
    workspace_dir: Path
    raw_dir: Path
    output_dir: Path
    raw_file_count: int


@dataclass(frozen=True)
class WorkspaceJobResult:
    job: WorkspaceJob
    status: str
    raw_file_count: int
    pass_count: int
    fail_count: int
    selected_row_count: int
    prompt_file_count: int
    output_root: Path
    summary: PipelineBatchSummary | None
    ready_gpt2_dir: Path | None = None
    ready_prompt_count: int = 0
    error_message: str = ""
    result_label: str = ""
    auto_fix_count: int = 0
    diagnosis: str = ""
    next_action: str = ""


@dataclass(frozen=True)
class ParallelWorkspaceSummary:
    selected_root: Path
    post_count: int
    max_workers: int
    job_count: int
    pass_job_count: int
    fail_job_count: int
    raw_file_count: int
    prompt_file_count: int
    ready_prompt_file_count: int
    results: list[WorkspaceJobResult] = field(default_factory=list)
    summary_file: Path | None = None
    run_id: str = ""
    run_mode: str = "all"


def _looks_like_sku_workspace(path: Path) -> bool:
    return path.is_dir() and path.name not in IGNORED_WORKSPACE_DIRS and not path.name.startswith(".")


def _raw_dir_for_workspace(path: Path) -> Path:
    raw = path / "raw"
    return raw if raw.exists() and raw.is_dir() else path


def _job_from_workspace(path: Path) -> WorkspaceJob | None:
    raw_dir = _raw_dir_for_workspace(path)
    try:
        raw_files = discover_raw_files(raw_dir)
    except Exception:
        return None
    if not raw_files:
        return None
    return WorkspaceJob(
        sku=path.name,
        workspace_dir=path,
        raw_dir=raw_dir,
        output_dir=path / "_cleaned",
        raw_file_count=len(raw_files),
    )


def discover_workspace_jobs(selected_root: Path) -> list[WorkspaceJob]:
    """Discover cleanable SKU workspaces under a selected folder.

    Supported operator selections:
    - `_operator_workspace` root containing one child folder per SKU;
    - one SKU folder containing `raw/`;
    - one `raw/` folder directly;
    - any folder with raw `.md/.txt/.text` files.

    The output root is always the SKU workspace folder's `_cleaned/`, never the
    global workspace root, so parallel runs do not mix outputs across SKUs.
    """
    root = selected_root.resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Folder not found: {root}")

    if root.name.lower() == "raw":
        job = _job_from_workspace(root.parent)
        return [job] if job else []

    direct_job = _job_from_workspace(root)

    child_jobs: list[WorkspaceJob] = []
    for child in sorted(root.iterdir()):
        if not _looks_like_sku_workspace(child):
            continue
        job = _job_from_workspace(child)
        if job:
            child_jobs.append(job)

    if child_jobs:
        return child_jobs
    return [direct_job] if direct_job else []


def _relative_or_absolute(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _first_failure_line(text: str) -> str:
    for line in text.splitlines():
        clean = line.strip()
        if clean.startswith("FAIL") or " FAIL:" in clean or "ERROR" in clean:
            return clean
    return ""


def _diagnose_pipeline_result(summary: PipelineBatchSummary | None) -> tuple[str, str, int, str]:
    """Return result_label, diagnosis, auto_fix_count, next_action."""
    if summary is None:
        return "FAIL_SYSTEM_ERROR", "Pipeline summary is missing.", 0, "Open raw file and rerun this SKU."

    auto_fix_count = 0
    failure_notes: list[str] = []
    pass_with_autofix = False
    for result in summary.results:
        report = _read_json(result.report_file)
        auto_fix_count += int(report.get("auto_fix_count", 0) or 0)
        if report.get("result") == "PASS_WITH_AUTOFIX":
            pass_with_autofix = True
        if result.status != "PASS":
            failure_line = _first_failure_line(
                "\n".join(
                    [
                        str(report.get("validator_stdout", "")),
                        str(report.get("validator_stderr", "")),
                        result.message,
                    ]
                )
            )
            if failure_line:
                failure_notes.append(failure_line)

    if summary.fail_count > 0:
        diagnosis = failure_notes[0] if failure_notes else "Validation failed, but no detailed validator message was captured."
        return "FAIL_RECOVERABLE", diagnosis, auto_fix_count, "Open report/raw, fix recoverable GPT1 output issue, then rerun this SKU."

    if pass_with_autofix or auto_fix_count > 0:
        return (
            "PASS_WITH_AUTOFIX",
            f"Passed after {auto_fix_count} safe whitespace auto-fix(es).",
            auto_fix_count,
            "Ready for GPT2. No user action needed for the auto-fixed formatting issue.",
        )

    return "PASS", "Passed deterministic cleaning and validation.", auto_fix_count, "Ready for GPT2."


def _collect_generated_prompt_files(summary: PipelineBatchSummary) -> list[Path]:
    prompt_files: list[Path] = []
    for result in summary.results:
        if result.status != "PASS" or result.prompt_folder is None:
            continue
        prompt_files.extend(sorted(result.prompt_folder.glob("*_gpt2_prompt.txt")))
    return sorted(prompt_files)


def _write_ready_readme(ready_dir: Path, sku: str, prompt_count: int) -> None:
    readme = f"""ชุดคำสั่งพร้อมส่งเข้า GPT2 สำหรับสินค้า {sku}

วิธีใช้:
1. เปิดไฟล์ 01_gpt2_prompt.txt
2. คัดลอกข้อความทั้งหมดในไฟล์
3. วางใน GPT2 Visual Prompt Refiner
4. เมื่อ GPT2 ตอบกลับ ให้ใช้เฉพาะ Final post copy และ Image-generation handoff ต่อไป
5. ทำไฟล์ถัดไปตามลำดับ 02, 03, ... จนครบ

จำนวนคำสั่ง GPT2 ที่เตรียมไว้: {prompt_count}

ไฟล์ดัชนี:
- {READY_INDEX_NAME}

หมายเหตุ:
- ไฟล์ในโฟลเดอร์นี้ถูกคัดจากผลลัพธ์ที่ตรวจผ่านแล้วเท่านั้น
- ลำดับ 01, 02, 03 คือ “ลำดับที่ระบบแนะนำให้ส่งเข้า GPT2” และอาจไม่ตรงกับ SEQUENCE เดิมของแคมเปญ
- ไม่ต้องเปิด clean TSV เอง เว้นแต่ต้องการตรวจสอบเชิงเทคนิค
"""
    (ready_dir / READY_README_NAME).write_text(readme, encoding="utf-8")


def _prepare_ready_for_gpt2(job: WorkspaceJob, summary: PipelineBatchSummary) -> tuple[Path, int]:
    """Create a human-friendly GPT2-ready package for one SKU workspace.

    The deterministic pipeline already creates canonical prompt files under
    `_cleaned/handoff/...`. This function creates an operator-facing package:

    `_ready_for_gpt2/01_gpt2_prompt.txt`, `02_gpt2_prompt.txt`, ...

    These files are the only files the operator needs to copy into GPT2.
    """
    prompt_files = _collect_generated_prompt_files(summary)
    ready_dir = job.workspace_dir / READY_DIR_NAME
    if ready_dir.exists():
        shutil.rmtree(ready_dir)
    ready_dir.mkdir(parents=True, exist_ok=True)

    width = max(2, len(str(len(prompt_files))))
    index_lines = [
        "ORDER\tSKU\tREADY_PROMPT_FILE\tSOURCE_PROMPT_FILE\tNEXT_ACTION"
    ]
    for index, source in enumerate(prompt_files, start=1):
        ready_name = f"{index:0{width}d}_gpt2_prompt.txt"
        destination = ready_dir / ready_name
        shutil.copyfile(source, destination)
        index_lines.append(
            "\t".join(
                [
                    str(index),
                    job.sku,
                    _relative_or_absolute(destination, job.workspace_dir),
                    _relative_or_absolute(source, job.workspace_dir),
                    "Copy this whole file into GPT2 Visual Prompt Refiner",
                ]
            )
        )

    (ready_dir / READY_INDEX_NAME).write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    _write_ready_readme(ready_dir, job.sku, len(prompt_files))
    return ready_dir, len(prompt_files)


def _run_job(job: WorkspaceJob, post_count: int) -> WorkspaceJobResult:
    try:
        summary = clean_folder(
            job.raw_dir,
            expected_rows=post_count,
            target_posts=post_count,
            output_folder=job.output_dir,
        )
        status = "PASS" if summary.fail_count == 0 and summary.pass_count > 0 else "FAIL"
        result_label, diagnosis, auto_fix_count, next_action = _diagnose_pipeline_result(summary)
        ready_dir: Path | None = None
        ready_prompt_count = 0
        if status == "PASS":
            ready_dir, ready_prompt_count = _prepare_ready_for_gpt2(job, summary)
        return WorkspaceJobResult(
            job=job,
            status=status,
            raw_file_count=summary.raw_file_count,
            pass_count=summary.pass_count,
            fail_count=summary.fail_count,
            selected_row_count=summary.selected_row_count,
            prompt_file_count=summary.prompt_file_count,
            output_root=summary.output_root,
            summary=summary,
            ready_gpt2_dir=ready_dir,
            ready_prompt_count=ready_prompt_count,
            error_message="" if status == "PASS" else diagnosis,
            result_label=result_label,
            auto_fix_count=auto_fix_count,
            diagnosis=diagnosis,
            next_action=next_action,
        )
    except Exception as exc:  # noqa: BLE001
        return WorkspaceJobResult(
            job=job,
            status="FAIL",
            raw_file_count=job.raw_file_count,
            pass_count=0,
            fail_count=job.raw_file_count,
            selected_row_count=0,
            prompt_file_count=0,
            output_root=job.output_dir,
            summary=None,
            ready_gpt2_dir=None,
            ready_prompt_count=0,
            error_message=str(exc),
            result_label="FAIL_SYSTEM_ERROR",
            auto_fix_count=0,
            diagnosis=str(exc),
            next_action="Fix the system/file error, then rerun this SKU.",
        )


def _previous_failed_skus(selected_root: Path) -> set[str]:
    summary_path = selected_root / PARALLEL_SUMMARY_NAME
    payload = _read_json(summary_path)
    failed: set[str] = set()
    for item in payload.get("results", []):
        if str(item.get("status", "")) != "PASS":
            sku = str(item.get("sku", "")).strip()
            if sku:
                failed.add(sku)
    return failed


def _filter_jobs_for_rerun(jobs: list[WorkspaceJob], selected_root: Path, run_mode: str) -> list[WorkspaceJob]:
    if run_mode == "all":
        return jobs
    if run_mode == "failed_only":
        failed = _previous_failed_skus(selected_root)
        return [job for job in jobs if job.sku in failed]
    raise ValueError(f"Unsupported run_mode: {run_mode}")


def _write_parallel_summary(summary: ParallelWorkspaceSummary) -> Path:
    path = summary.selected_root / PARALLEL_SUMMARY_NAME
    payload = {
        "run_id": summary.run_id,
        "run_mode": summary.run_mode,
        "selected_root": str(summary.selected_root),
        "post_count": summary.post_count,
        "max_workers": summary.max_workers,
        "job_count": summary.job_count,
        "pass_job_count": summary.pass_job_count,
        "fail_job_count": summary.fail_job_count,
        "raw_file_count": summary.raw_file_count,
        "prompt_file_count": summary.prompt_file_count,
        "ready_prompt_file_count": summary.ready_prompt_file_count,
        "auto_fix_count": sum(result.auto_fix_count for result in summary.results),
        "results": [
            {
                "sku": result.job.sku,
                "workspace_dir": str(result.job.workspace_dir),
                "raw_dir": str(result.job.raw_dir),
                "output_root": str(result.output_root),
                "ready_gpt2_dir": str(result.ready_gpt2_dir) if result.ready_gpt2_dir else "",
                "status": result.status,
                "result_label": result.result_label or result.status,
                "raw_file_count": result.raw_file_count,
                "pass_count": result.pass_count,
                "fail_count": result.fail_count,
                "selected_row_count": result.selected_row_count,
                "prompt_file_count": result.prompt_file_count,
                "ready_prompt_count": result.ready_prompt_count,
                "auto_fix_count": result.auto_fix_count,
                "diagnosis": result.diagnosis,
                "next_action": result.next_action,
                "error_message": result.error_message,
            }
            for result in summary.results
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def cleanup_generated_outputs(selected_root: Path) -> dict[str, object]:
    """Delete only generated outputs; never delete raw GPT1 source files."""
    root = selected_root.resolve()
    jobs = discover_workspace_jobs(root)
    removed: list[str] = []
    preserved: list[str] = []
    for job in jobs:
        preserved.append(str(job.raw_dir))
        for dirname in GENERATED_OUTPUT_DIRS:
            target = job.workspace_dir / dirname
            if target.exists():
                shutil.rmtree(target)
                removed.append(str(target))
    summary_file = root / PARALLEL_SUMMARY_NAME
    if summary_file.exists():
        summary_file.unlink()
        removed.append(str(summary_file))
    return {
        "selected_root": str(root),
        "removed_generated_outputs": removed,
        "preserved_raw_dirs": preserved,
        "raw_deleted": False,
    }


def export_diagnostic_zip(selected_root: Path, sku: str | None = None) -> Path:
    """Export a compact diagnostic bundle for failed or selected SKU workspaces."""
    root = selected_root.resolve()
    jobs = discover_workspace_jobs(root)
    if sku:
        jobs = [job for job in jobs if job.sku == sku]
        if not jobs:
            raise ValueError(f"SKU not found in workspace: {sku}")

    if sku is None:
        failed = _previous_failed_skus(root)
        if failed:
            jobs = [job for job in jobs if job.sku in failed]

    diagnostics_dir = root / DIAGNOSTIC_DIR_NAME
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    suffix = sku or "failed_or_selected"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = diagnostics_dir / f"{suffix}_diagnostic_{timestamp}.zip"

    def add_if_exists(zf: zipfile.ZipFile, path: Path) -> None:
        if path.exists() and path.is_file():
            zf.write(path, arcname=str(path.resolve().relative_to(root)))

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        add_if_exists(zf, root / PARALLEL_SUMMARY_NAME)
        for job in jobs:
            for raw_file in discover_raw_files(job.raw_dir):
                add_if_exists(zf, raw_file)
            for report_file in sorted((job.output_dir / "reports").glob("*.json")):
                add_if_exists(zf, report_file)
            add_if_exists(zf, job.output_dir / "pipeline_batch_summary.json")
            add_if_exists(zf, job.workspace_dir / READY_DIR_NAME / READY_README_NAME)
            add_if_exists(zf, job.workspace_dir / READY_DIR_NAME / READY_INDEX_NAME)
        readme = (
            "Diagnostic bundle for BiiigBee Social Content Production Cockpit.\n"
            "Includes raw GPT1 source files, cleaner reports, summaries, and GPT2-ready indexes when available.\n"
            "Generated outputs can be recreated; raw files are included for diagnosis only.\n"
        )
        zf.writestr("README_diagnostic.txt", readme)
    return zip_path


def process_workspace_parallel(
    selected_root: Path,
    *,
    post_count: int = DEFAULT_POST_COUNT,
    max_workers: int | None = None,
    run_mode: str = "all",
) -> ParallelWorkspaceSummary:
    post_count = validate_post_count(post_count)
    all_jobs = discover_workspace_jobs(selected_root)
    if not all_jobs:
        raise ValueError("No GPT1 raw files were found in the selected folder or its SKU child folders.")

    jobs = _filter_jobs_for_rerun(all_jobs, selected_root.resolve(), run_mode)
    if not jobs:
        raise ValueError("No jobs selected for this rerun mode. Use run_mode='all' to process every raw file.")

    if max_workers is None:
        max_workers = min(4, len(jobs), max(1, os.cpu_count() or 1))
    max_workers = max(1, min(max_workers, 8, len(jobs)))

    results: list[WorkspaceJobResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {executor.submit(_run_job, job, post_count): job for job in jobs}
        for future in as_completed(future_to_job):
            results.append(future.result())

    results.sort(key=lambda result: result.job.sku)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = ParallelWorkspaceSummary(
        selected_root=selected_root.resolve(),
        post_count=post_count,
        max_workers=max_workers,
        job_count=len(jobs),
        pass_job_count=sum(1 for result in results if result.status == "PASS"),
        fail_job_count=sum(1 for result in results if result.status != "PASS"),
        raw_file_count=sum(result.raw_file_count for result in results),
        prompt_file_count=sum(result.prompt_file_count for result in results),
        ready_prompt_file_count=sum(result.ready_prompt_count for result in results),
        results=results,
        run_id=run_id,
        run_mode=run_mode,
    )
    summary_file = _write_parallel_summary(summary)
    return ParallelWorkspaceSummary(
        selected_root=summary.selected_root,
        post_count=summary.post_count,
        max_workers=summary.max_workers,
        job_count=summary.job_count,
        pass_job_count=summary.pass_job_count,
        fail_job_count=summary.fail_job_count,
        raw_file_count=summary.raw_file_count,
        prompt_file_count=summary.prompt_file_count,
        ready_prompt_file_count=summary.ready_prompt_file_count,
        results=summary.results,
        summary_file=summary_file,
        run_id=run_id,
        run_mode=run_mode,
    )


__all__ = [
    "DEFAULT_POST_COUNT",
    "MAX_POST_COUNT",
    "MIN_POST_COUNT",
    "READY_DIR_NAME",
    "READY_INDEX_NAME",
    "READY_README_NAME",
    "WorkspaceJob",
    "WorkspaceJobResult",
    "ParallelWorkspaceSummary",
    "cleanup_generated_outputs",
    "discover_workspace_jobs",
    "export_diagnostic_zip",
    "process_workspace_parallel",
]
