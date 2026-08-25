from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = REPO_ROOT / "marketing-content-os" / "apps" / "social_pipeline_desktop"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import workspace_parallel_service as service  # noqa: E402


class WorkspaceParallelServiceRerunTests(unittest.TestCase):
    def test_failed_only_rerun_merges_back_into_full_summary(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            pass_dir = root / "SKU-PASS-01"
            fail_dir = root / "SKU-FAIL-01"
            for folder in (pass_dir, fail_dir):
                raw = folder / "raw"
                raw.mkdir(parents=True)
                (raw / "gpt1.md").write_text("ROW-example", encoding="utf-8")

            previous_summary = {
                "run_id": "previous",
                "run_mode": "all",
                "job_count": 2,
                "pass_job_count": 1,
                "fail_job_count": 1,
                "raw_file_count": 2,
                "ready_prompt_file_count": 10,
                "results": [
                    {
                        "sku": "SKU-PASS-01",
                        "workspace_dir": str(pass_dir),
                        "raw_dir": str(pass_dir / "raw"),
                        "output_root": str(pass_dir / "_cleaned"),
                        "ready_gpt2_dir": str(pass_dir / "_ready_for_gpt2"),
                        "status": "PASS",
                        "result_label": "PASS",
                        "raw_file_count": 1,
                        "pass_count": 1,
                        "fail_count": 0,
                        "selected_row_count": 10,
                        "prompt_file_count": 10,
                        "ready_prompt_count": 10,
                        "auto_fix_count": 0,
                        "diagnosis": "Passed.",
                        "next_action": "Ready for GPT2.",
                        "error_message": "",
                    },
                    {
                        "sku": "SKU-FAIL-01",
                        "workspace_dir": str(fail_dir),
                        "raw_dir": str(fail_dir / "raw"),
                        "output_root": str(fail_dir / "_cleaned"),
                        "ready_gpt2_dir": "",
                        "status": "FAIL",
                        "result_label": "FAIL_RECOVERABLE",
                        "raw_file_count": 1,
                        "pass_count": 0,
                        "fail_count": 1,
                        "selected_row_count": 0,
                        "prompt_file_count": 0,
                        "ready_prompt_count": 0,
                        "auto_fix_count": 0,
                        "diagnosis": "Recoverable fail.",
                        "next_action": "Rerun.",
                        "error_message": "Recoverable fail.",
                    },
                ],
            }
            (root / service.PARALLEL_SUMMARY_NAME).write_text(
                json.dumps(previous_summary, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            original_run_job = service._run_job  # type: ignore[attr-defined]

            def fake_run_job(job: service.WorkspaceJob, post_count: int) -> service.WorkspaceJobResult:
                self.assertEqual(job.sku, "SKU-FAIL-01")
                ready = job.workspace_dir / service.READY_DIR_NAME
                ready.mkdir(parents=True, exist_ok=True)
                return service.WorkspaceJobResult(
                    job=job,
                    status="PASS",
                    raw_file_count=1,
                    pass_count=1,
                    fail_count=0,
                    selected_row_count=10,
                    prompt_file_count=10,
                    output_root=job.output_dir,
                    summary=None,
                    ready_gpt2_dir=ready,
                    ready_prompt_count=10,
                    result_label="PASS",
                    diagnosis="Passed deterministic cleaning and validation.",
                    next_action="Ready for GPT2.",
                )

            try:
                service._run_job = fake_run_job  # type: ignore[attr-defined]
                summary = service.process_workspace_parallel(root, post_count=10, max_workers=1, run_mode="failed_only")
            finally:
                service._run_job = original_run_job  # type: ignore[attr-defined]

            self.assertEqual(summary.job_count, 2)
            self.assertEqual(summary.pass_job_count, 2)
            self.assertEqual(summary.fail_job_count, 0)
            self.assertEqual(summary.ready_prompt_file_count, 20)
            self.assertEqual({result.job.sku for result in summary.results}, {"SKU-PASS-01", "SKU-FAIL-01"})


if __name__ == "__main__":
    unittest.main()
