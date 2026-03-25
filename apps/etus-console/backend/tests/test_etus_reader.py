from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app import etus_reader as reader


class EtusReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.docs_root = self.root / "docs" / "ets"
        self.projects_root = self.docs_root / "projects"
        self.memory_root = self.docs_root / ".memory"

        self.project_slug = "demo"
        self.project_root = self.projects_root / self.project_slug
        (self.project_root / "state").mkdir(parents=True, exist_ok=True)
        (self.project_root / "features" / "csv-upload").mkdir(parents=True, exist_ok=True)
        (self.project_root / "planning").mkdir(parents=True, exist_ok=True)

        (self.project_root / "state" / "project-status.yaml").write_text(
            "mode: product\ncurrent_phase: planning\nnext_step: /design\n",
            encoding="utf-8",
        )
        (self.project_root / "state" / "workflow-state.yaml").write_text(
            "gates:\n  requirements_gate: go\n",
            encoding="utf-8",
        )
        (self.project_root / "state" / "feature-index.yaml").write_text(
            "features:\n  csv-upload:\n    title: CSV Upload\n    discovery_state: solution_selected\n    delivery_state: brief_ready\n    release_state: not_released\n    governance_state: active\n    next_recommended_step: /feature stories csv-upload\n",
            encoding="utf-8",
        )
        (self.project_root / "planning" / "user-stories.md").write_text(
            "# User Stories\n\nGiven algo\nWhen algo\nThen algo\n",
            encoding="utf-8",
        )
        (self.project_root / "planning" / "prd.md").write_text(
            "# PRD\n\nGiven algo indevido\nWhen algo indevido\nThen algo indevido\n",
            encoding="utf-8",
        )

        self.original_docs_root = reader.DOCS_ROOT
        self.original_projects_root = reader.PROJECTS_ROOT
        self.original_memory_root = reader.MEMORY_ROOT
        reader.DOCS_ROOT = self.docs_root
        reader.PROJECTS_ROOT = self.projects_root
        reader.MEMORY_ROOT = self.memory_root

    def tearDown(self) -> None:
        reader.DOCS_ROOT = self.original_docs_root
        reader.PROJECTS_ROOT = self.original_projects_root
        reader.MEMORY_ROOT = self.original_memory_root
        self.tmp.cleanup()

    def test_iso_mtime_returns_iso_string(self) -> None:
        path = self.project_root / "planning" / "user-stories.md"
        result = reader.iso_mtime(path)
        self.assertIsNotNone(result)
        self.assertIn("T", result)
        self.assertTrue(result.endswith("+00:00"))

    def test_resolve_artifact_path_blocks_traversal(self) -> None:
        with self.assertRaises(FileNotFoundError):
            reader.resolve_artifact_path(self.project_slug, "../README.md")

    def test_build_validation_summary_detects_sst_warning(self) -> None:
        artifacts = reader.build_project_artifacts(self.project_slug)
        validation = reader.build_validation_summary(self.project_slug, artifacts, {"gates": {}})
        self.assertTrue(any("Given/When/Then" in warning for warning in validation.sst_warnings))


if __name__ == "__main__":
    unittest.main()
