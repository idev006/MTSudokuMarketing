from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
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
    error_message: str = ""


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
    results: list[WorkspaceJobResult] = field(default_factory=list)
    summary_file: Path | None = None


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


def _run_job(job: WorkspaceJob, post_count: int) -> WorkspaceJobResult:
    try:
        summary = clean_folder(
            job.raw_dir,
            expected_rows=post_count,
            target_posts=post_count,
            output_folder=job.output_dir,
        )
        status = "PASS" if summary.fail_count == 0 and summary.pass_count > 0 else "FAIL"
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
            error_message=str(exc),
        )


def _write_parallel_summary(summary: ParallelWorkspaceSummary) -> Path:
    path = summary.selected_root / "_workspace_parallel_summary.json"
    payload = {
        "selected_root": str(summary.selected_root),
        "post_count": summary.post_count,
        "max_workers": summary.max_workers,
        "job_count": summary.job_count,
        "pass_job_count": summary.pass_job_count,
        "fail_job_count": summary.fail_job_count,
        "raw_file_count": summary.raw_file_count,
        "prompt_file_count": summary.prompt_file_count,
        "results": [
            {
                "sku": result.job.sku,
                "workspace_dir": str(result.job.workspace_dir),
                "raw_dir": str(result.job.raw_dir),
                "output_root": str(result.output_root),
                "status": result.status,
                "raw_file_count": result.raw_file_count,
                "pass_count": result.pass_count,
                "fail_count": result.fail_count,
                "selected_row_count": result.selected_row_count,
                "prompt_file_count": result.prompt_file_count,
                "error_message": result.error_message,
            }
            for result in summary.results
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def process_workspace_parallel(
    selected_root: Path,
    *,
    post_count: int = DEFAULT_POST_COUNT,
    max_workers: int | None = None,
) -> ParallelWorkspaceSummary:
    post_count = validate_post_count(post_count)
    jobs = discover_workspace_jobs(selected_root)
    if not jobs:
        raise ValueError("No GPT1 raw files were found in the selected folder or its SKU child folders.")

    if max_workers is None:
        max_workers = min(4, len(jobs), max(1, os.cpu_count() or 1))
    max_workers = max(1, min(max_workers, 8, len(jobs)))

    results: list[WorkspaceJobResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {executor.submit(_run_job, job, post_count): job for job in jobs}
        for future in as_completed(future_to_job):
            results.append(future.result())

    results.sort(key=lambda result: result.job.sku)
    summary = ParallelWorkspaceSummary(
        selected_root=selected_root.resolve(),
        post_count=post_count,
        max_workers=max_workers,
        job_count=len(jobs),
        pass_job_count=sum(1 for result in results if result.status == "PASS"),
        fail_job_count=sum(1 for result in results if result.status != "PASS"),
        raw_file_count=sum(result.raw_file_count for result in results),
        prompt_file_count=sum(result.prompt_file_count for result in results),
        results=results,
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
        results=summary.results,
        summary_file=summary_file,
    )


__all__ = [
    "DEFAULT_POST_COUNT",
    "MAX_POST_COUNT",
    "MIN_POST_COUNT",
    "WorkspaceJob",
    "WorkspaceJobResult",
    "ParallelWorkspaceSummary",
    "discover_workspace_jobs",
    "process_workspace_parallel",
]
