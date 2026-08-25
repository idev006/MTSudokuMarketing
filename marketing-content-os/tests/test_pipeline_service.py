from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = REPO_ROOT / "marketing-content-os" / "apps" / "social_pipeline_desktop"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import pipeline_service  # noqa: E402


class PipelineServiceDiscoveryTests(unittest.TestCase):
    def test_discover_raw_files_ignores_generated_and_system_folders(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            keep = root / "raw_answer.md"
            keep.write_text("ROW-example", encoding="utf-8")
            keep_nested = root / "BK-TEST" / "raw" / "gpt1.txt"
            keep_nested.parent.mkdir(parents=True)
            keep_nested.write_text("ROW-example", encoding="utf-8")

            generated_paths = [
                root / "_cleaned" / "clean" / "old_clean.tsv",
                root / "_ready_for_gpt2" / "01_gpt2_prompt.txt",
                root / "_diagnostics" / "diagnostic.txt",
                root / "_runs" / "run_notes.txt",
                root / ".venv" / "package.txt",
                root / ".git" / "COMMIT_EDITMSG.txt",
                root / "__pycache__" / "cache.txt",
            ]
            for path in generated_paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("generated", encoding="utf-8")

            discovered = {path.relative_to(root).as_posix() for path in pipeline_service.discover_raw_files(root)}
            self.assertEqual(discovered, {"raw_answer.md", "BK-TEST/raw/gpt1.txt"})

    def test_validate_post_count_accepts_only_supported_range(self) -> None:
        self.assertEqual(pipeline_service.validate_post_count(1), 1)
        self.assertEqual(pipeline_service.validate_post_count(60), 60)
        with self.assertRaises(ValueError):
            pipeline_service.validate_post_count(0)
        with self.assertRaises(ValueError):
            pipeline_service.validate_post_count(61)


if __name__ == "__main__":
    unittest.main()
