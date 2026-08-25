from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

READY_DIR_NAME = "_ready_for_gpt2"
PARALLEL_SUMMARY_NAME = "_workspace_parallel_summary.json"
HEALTH_REPORT_NAME = "_workspace_health_check.json"
SUPPORTED_INPUT_SUFFIXES = {".md", ".txt", ".text"}
IGNORED_PARTS = {
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


@dataclass(frozen=True)
class SkuHealth:
    sku: str
    workspace_dir: Path
    raw_dir: Path
    raw_file_count: int
    raw_digest: str
    raw_newest_mtime_ns: int
    ready_prompt_count: int
    ready_newest_mtime_ns: int
    stale_output: bool


def _normal_workspace_root(path: Path) -> Path:
    root = path.resolve()
    return root.parent if root.name.lower() == "raw" else root


def _is_ignored(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return any(part.lower() in parts for part in IGNORED_PARTS)


def discover_raw_files(folder: Path) -> list[Path]:
    files: list[Path] = []
    if not folder.exists() or not folder.is_dir():
        return files
    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
            continue
        if _is_ignored(path):
            continue
        files.append(path)
    return files


def _raw_dir_for_workspace(path: Path) -> Path:
    raw = path / "raw"
    return raw if raw.exists() and raw.is_dir() else path


def discover_sku_workspaces(selected_root: Path) -> list[Path]:
    root = _normal_workspace_root(selected_root)
    if root.name.lower() == "raw":
        return [root.parent]
    child_workspaces: list[Path] = []
    for child in sorted(root.iterdir()) if root.exists() else []:
        if not child.is_dir() or child.name.startswith(".") or child.name in IGNORED_PARTS:
            continue
        if discover_raw_files(_raw_dir_for_workspace(child)):
            child_workspaces.append(child)
    if child_workspaces:
        return child_workspaces
    return [root] if discover_raw_files(_raw_dir_for_workspace(root)) else []


def _file_digest(path: Path, root: Path) -> str:
    hasher = hashlib.sha256()
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = path.name
    hasher.update(rel.encode("utf-8"))
    hasher.update(b"\0")
    hasher.update(path.read_bytes())
    return hasher.hexdigest()


def raw_digest(files: list[Path], raw_dir: Path) -> str:
    hasher = hashlib.sha256()
    for path in files:
        hasher.update(_file_digest(path, raw_dir).encode("ascii"))
        hasher.update(b"\n")
    return hasher.hexdigest()


def newest_mtime_ns(paths: list[Path]) -> int:
    newest = 0
    for path in paths:
        try:
            newest = max(newest, path.stat().st_mtime_ns)
        except OSError:
            continue
    return newest


def ready_prompt_files(workspace_dir: Path) -> list[Path]:
    ready_dir = workspace_dir / READY_DIR_NAME
    if not ready_dir.exists():
        return []
    return sorted(ready_dir.glob("*_gpt2_prompt.txt"))


def collect_sku_health(workspace_dir: Path) -> SkuHealth:
    raw_dir = _raw_dir_for_workspace(workspace_dir)
    raw_files = discover_raw_files(raw_dir)
    ready_files = ready_prompt_files(workspace_dir)
    raw_newest = newest_mtime_ns(raw_files)
    ready_newest = newest_mtime_ns(ready_files)
    return SkuHealth(
        sku=workspace_dir.name,
        workspace_dir=workspace_dir,
        raw_dir=raw_dir,
        raw_file_count=len(raw_files),
        raw_digest=raw_digest(raw_files, raw_dir),
        raw_newest_mtime_ns=raw_newest,
        ready_prompt_count=len(ready_files),
        ready_newest_mtime_ns=ready_newest,
        stale_output=bool(raw_files and ready_files and raw_newest > ready_newest),
    )


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _summary_by_sku(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("sku", "")): item for item in summary.get("results", []) if item.get("sku")}


def collect_workspace_health(selected_root: Path) -> dict[str, Any]:
    root = _normal_workspace_root(selected_root)
    summary_path = root / PARALLEL_SUMMARY_NAME
    prior_health = _read_json(root / HEALTH_REPORT_NAME)
    prior_by_sku = {item.get("sku"): item for item in prior_health.get("results", []) if item.get("sku")}
    summary = _read_json(summary_path)
    summary_by_sku = _summary_by_sku(summary)

    results: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    sku_health = [collect_sku_health(workspace) for workspace in discover_sku_workspaces(root)]
    actual_raw_count = sum(item.raw_file_count for item in sku_health)
    actual_ready_count = sum(item.ready_prompt_count for item in sku_health)

    if summary:
        if int(summary.get("job_count", -1)) != len(sku_health):
            errors.append(f"job_count mismatch: summary={summary.get('job_count')} actual={len(sku_health)}")
        if int(summary.get("raw_file_count", -1)) != actual_raw_count:
            errors.append(f"raw_file_count mismatch: summary={summary.get('raw_file_count')} actual={actual_raw_count}")
        if int(summary.get("ready_prompt_file_count", -1)) != actual_ready_count:
            errors.append(
                f"ready_prompt_file_count mismatch: summary={summary.get('ready_prompt_file_count')} actual={actual_ready_count}"
            )
    else:
        warnings.append("No workspace summary found. Run the GPT1 validation pipeline first.")

    for item in sku_health:
        summary_item = summary_by_sku.get(item.sku, {})
        previous = prior_by_sku.get(item.sku, {})
        raw_changed = bool(previous and previous.get("raw_digest") != item.raw_digest)
        ready_summary = int(summary_item.get("ready_prompt_count", -1)) if summary_item else -1
        raw_summary = int(summary_item.get("raw_file_count", -1)) if summary_item else -1
        status = str(summary_item.get("status", "")) if summary_item else ""
        row: dict[str, Any] = {
            "sku": item.sku,
            "workspace_dir": str(item.workspace_dir),
            "raw_dir": str(item.raw_dir),
            "raw_file_count": item.raw_file_count,
            "raw_digest": item.raw_digest,
            "ready_prompt_count": item.ready_prompt_count,
            "summary_status": status,
            "summary_raw_file_count": raw_summary,
            "summary_ready_prompt_count": ready_summary,
            "raw_changed_since_last_health_check": raw_changed,
            "stale_output": item.stale_output,
        }
        if summary_item:
            if raw_summary != item.raw_file_count:
                errors.append(f"{item.sku}: raw count mismatch summary={raw_summary} actual={item.raw_file_count}")
            if ready_summary != item.ready_prompt_count:
                errors.append(f"{item.sku}: ready prompt mismatch summary={ready_summary} actual={item.ready_prompt_count}")
            if status == "PASS" and item.ready_prompt_count <= 0:
                errors.append(f"{item.sku}: status PASS but no ready GPT2 prompts found")
        if item.stale_output:
            errors.append(f"{item.sku}: raw file is newer than ready GPT2 output; rerun this SKU")
        if raw_changed:
            warnings.append(f"{item.sku}: raw digest changed since last health check")
        results.append(row)

    payload: dict[str, Any] = {
        "health_status": "PASS" if not errors else "FAIL",
        "selected_root": str(root),
        "summary_file": str(summary_path) if summary_path.exists() else "",
        "job_count_actual": len(sku_health),
        "raw_file_count_actual": actual_raw_count,
        "ready_prompt_file_count_actual": actual_ready_count,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "results": results,
    }
    return payload


def write_health_report(selected_root: Path, payload: dict[str, Any]) -> Path:
    root = _normal_workspace_root(selected_root)
    path = root / HEALTH_REPORT_NAME
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check BiiigBee operator workspace health.")
    parser.add_argument("workspace", type=Path, help="_operator_workspace, SKU workspace, or raw folder")
    parser.add_argument("--write-report", action="store_true", help=f"Write {HEALTH_REPORT_NAME} beside the workspace summary")
    args = parser.parse_args(argv)

    payload = collect_workspace_health(args.workspace)
    if args.write_report:
        report = write_health_report(args.workspace, payload)
        payload["health_report_file"] = str(report)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["health_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
