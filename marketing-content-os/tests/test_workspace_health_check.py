from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = REPO_ROOT / "marketing-content-os" / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import workspace_health_check as health  # noqa: E402


class WorkspaceHealthCheckTests(unittest.TestCase):
    def test_health_check_detects_summary_count_mismatch(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            sku = root / "SKU-001"
            raw = sku / "raw"
            raw.mkdir(parents=True)
            (raw / "gpt1.md").write_text("ROW-example", encoding="utf-8")
            ready = sku / health.READY_DIR_NAME
            ready.mkdir()
            (ready / "01_gpt2_prompt.txt").write_text("prompt", encoding="utf-8")

            bad_summary = {
                "job_count": 1,
                "raw_file_count": 1,
                "ready_prompt_file_count": 2,
                "results": [
                    {
                        "sku": "SKU-001",
                        "status": "PASS",
                        "raw_file_count": 1,
                        "ready_prompt_count": 2,
                    }
                ],
            }
            (root / health.PARALLEL_SUMMARY_NAME).write_text(
                json.dumps(bad_summary, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            payload = health.collect_workspace_health(root)
            self.assertEqual(payload["health_status"], "FAIL")
            self.assertGreaterEqual(payload["error_count"], 1)
            self.assertTrue(any("ready" in error for error in payload["errors"]))

    def test_health_check_passes_when_summary_matches_files(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            sku = root / "SKU-001"
            raw = sku / "raw"
            raw.mkdir(parents=True)
            (raw / "gpt1.md").write_text("ROW-example", encoding="utf-8")
            ready = sku / health.READY_DIR_NAME
            ready.mkdir()
            (ready / "01_gpt2_prompt.txt").write_text("prompt", encoding="utf-8")

            summary = {
                "job_count": 1,
                "raw_file_count": 1,
                "ready_prompt_file_count": 1,
                "results": [
                    {
                        "sku": "SKU-001",
                        "status": "PASS",
                        "raw_file_count": 1,
                        "ready_prompt_count": 1,
                    }
                ],
            }
            (root / health.PARALLEL_SUMMARY_NAME).write_text(
                json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            payload = health.collect_workspace_health(root)
            self.assertEqual(payload["health_status"], "PASS")
            self.assertEqual(payload["ready_prompt_file_count_actual"], 1)


if __name__ == "__main__":
    unittest.main()
