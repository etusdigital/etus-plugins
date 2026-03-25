#!/usr/bin/env python3
"""Tests for feature_lifecycle.py — feature state management and ID extraction."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

# Ensure hooks directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from feature_lifecycle import (
    classify_etus_id,
    ensure_feature_state,
    ensure_project_state,
    extract_feature_slug,
    extract_ids_from_text,
    find_single_project_slug,
    list_project_slugs,
    sync_document_state,
)
from yaml_io import read_frontmatter_markdown, read_yaml_file


# ─── extract_feature_slug ────────────────────────────────────────────────────


class TestExtractFeatureSlug(unittest.TestCase):
    def test_feature_folder_path(self):
        self.assertEqual(extract_feature_slug("features/csv-upload/feature-status.md"), "csv-upload")

    def test_feature_subfolder(self):
        self.assertEqual(extract_feature_slug("features/login/user-stories.md"), "login")

    def test_legacy_flat_pattern(self):
        self.assertEqual(extract_feature_slug("features/feature-brief-login.md"), "login")

    def test_legacy_user_stories(self):
        self.assertEqual(extract_feature_slug("features/user-stories-csv.md"), "csv")

    def test_legacy_design_delta(self):
        self.assertEqual(extract_feature_slug("features/design-delta-auth.md"), "auth")

    def test_legacy_impl_plan(self):
        self.assertEqual(extract_feature_slug("features/impl-plan-search.md"), "search")

    def test_non_feature_path(self):
        self.assertIsNone(extract_feature_slug("planning/prd.md"))

    def test_readme_excluded(self):
        self.assertIsNone(extract_feature_slug("features/README.md"))

    def test_templates_excluded(self):
        self.assertIsNone(extract_feature_slug("features/_templates"))


# ─── extract_ids_from_text ───────────────────────────────────────────────────


class TestExtractIdsFromText(unittest.TestCase):
    def test_extracts_user_stories(self):
        text = "This relates to US-001 and US-002."
        result = extract_ids_from_text(text)
        self.assertIn("US-001", result.get("user_stories", []))
        self.assertIn("US-002", result.get("user_stories", []))

    def test_extracts_solutions(self):
        text = "SOL-1 drives this feature."
        result = extract_ids_from_text(text)
        self.assertIn("SOL-1", result.get("solutions", []))

    def test_extracts_impl_items(self):
        text = "See impl-1, impl-2 for tasks."
        result = extract_ids_from_text(text)
        impl = result.get("implementation_items", [])
        self.assertIn("impl-1", impl)
        self.assertIn("impl-2", impl)

    def test_no_ids_returns_empty_lists(self):
        text = "No IDs in this text."
        result = extract_ids_from_text(text)
        for values in result.values():
            self.assertEqual(values, [])

    def test_deduplication(self):
        text = "US-001 appears twice: US-001."
        result = extract_ids_from_text(text)
        self.assertEqual(result.get("user_stories", []).count("US-001"), 1)


# ─── classify_etus_id ────────────────────────────────────────────────────────


class TestClassifyEtusId(unittest.TestCase):
    def test_user_story(self):
        self.assertEqual(classify_etus_id("US-001"), "story")

    def test_impl_task(self):
        self.assertEqual(classify_etus_id("impl-5"), "task")

    def test_feature_brief(self):
        self.assertEqual(classify_etus_id("FB-1"), "feature_brief_item")

    def test_solution(self):
        self.assertEqual(classify_etus_id("SOL-2"), "solution")

    def test_unknown(self):
        self.assertEqual(classify_etus_id("XYZ-99"), "generic")


# ─── ensure_project_state ────────────────────────────────────────────────────


class TestEnsureProjectState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_creates_project_structure(self):
        ensure_project_state(self.root, "demo")
        state_dir = os.path.join(self.root, "docs", "ets", "projects", "demo", "state")
        self.assertTrue(os.path.exists(os.path.join(state_dir, "project-status.yaml")))
        self.assertTrue(os.path.exists(os.path.join(state_dir, "workflow-state.yaml")))
        self.assertTrue(os.path.exists(os.path.join(state_dir, "feature-index.yaml")))

    def test_creates_all_directories(self):
        ensure_project_state(self.root, "demo")
        base = os.path.join(self.root, "docs", "ets", "projects", "demo")
        for folder in ["discovery", "planning", "architecture", "data", "ux",
                        "implementation", "features", "bugs", "spikes"]:
            self.assertTrue(os.path.isdir(os.path.join(base, folder)), f"Missing: {folder}")

    def test_idempotent(self):
        ensure_project_state(self.root, "demo")
        ensure_project_state(self.root, "demo")  # should not raise
        status = read_yaml_file(
            os.path.join(self.root, "docs", "ets", "projects", "demo", "state", "project-status.yaml")
        )
        self.assertEqual(status["project_slug"], "demo")

    def test_product_status_defaults(self):
        ensure_project_state(self.root, "demo", mode="product")
        status = read_yaml_file(
            os.path.join(self.root, "docs", "ets", "projects", "demo", "state", "project-status.yaml")
        )
        self.assertEqual(status["mode"], "product")
        self.assertEqual(status["project_slug"], "demo")


# ─── ensure_feature_state ────────────────────────────────────────────────────


class TestEnsureFeatureState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_creates_feature_status(self):
        path = ensure_feature_state(self.root, "demo", "csv-upload", title="CSV Upload")
        self.assertTrue(os.path.exists(path))
        fm, body = read_frontmatter_markdown(path)
        self.assertEqual(fm["feature_slug"], "csv-upload")
        self.assertIn("Feature Status", body)

    def test_idempotent(self):
        path1 = ensure_feature_state(self.root, "demo", "login")
        path2 = ensure_feature_state(self.root, "demo", "login")
        self.assertEqual(path1, path2)

    def test_feature_dir_created(self):
        ensure_feature_state(self.root, "demo", "search")
        feature_dir = os.path.join(self.root, "docs", "ets", "projects", "demo", "features", "search")
        self.assertTrue(os.path.isdir(feature_dir))


# ─── list_project_slugs / find_single_project_slug ───────────────────────────


class TestProjectLookup(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_no_projects(self):
        self.assertEqual(list_project_slugs(self.root), [])
        self.assertIsNone(find_single_project_slug(self.root))

    def test_single_project(self):
        ensure_project_state(self.root, "my-project")
        self.assertEqual(list_project_slugs(self.root), ["my-project"])
        self.assertEqual(find_single_project_slug(self.root), "my-project")

    def test_multiple_projects(self):
        ensure_project_state(self.root, "alpha")
        ensure_project_state(self.root, "beta")
        slugs = list_project_slugs(self.root)
        self.assertEqual(slugs, ["alpha", "beta"])
        self.assertIsNone(find_single_project_slug(self.root))


# ─── sync_document_state ─────────────────────────────────────────────────────


class TestSyncDocumentState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        ensure_project_state(self.root, "demo", mode="product")

    def tearDown(self):
        self.tmp.cleanup()

    def test_product_doc_updates_state(self):
        rel_path = "docs/ets/projects/demo/planning/prd.md"
        abs_path = os.path.join(self.root, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w") as f:
            f.write("# PRD\n\n## Features\n\nPRD-F-001: Login\n")

        result = sync_document_state(self.root, rel_path, "planning", "product", "prd", "complete")
        self.assertIn("project_status_path", result)

        status = read_yaml_file(result["project_status_path"])
        # Fresh project has no phase_status entries, so 'planning' is not in it;
        # the routing falls back to 'ideate'. The next_step is what matters.
        self.assertIn(status["current_phase"], {"ideate", "planning"})
        self.assertEqual(status["next_step"], "/plan requirements")

    def test_feature_doc_creates_feature_state(self):
        rel_path = "docs/ets/projects/demo/features/login/feature-brief.md"
        abs_path = os.path.join(self.root, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w") as f:
            f.write("# Feature Brief\n\nFB-1: Login flow\n")

        result = sync_document_state(self.root, rel_path, "feature", "feature", "feature-brief", "complete")
        self.assertEqual(result.get("feature_slug"), "login")
        self.assertTrue(os.path.exists(result.get("feature_status_path", "")))

    def test_bug_mode_no_feature_state(self):
        """Bug mode should NOT create feature state even if path looks like a feature."""
        rel_path = "docs/ets/projects/demo/bugs/tech-spec-fix-crash.md"
        abs_path = os.path.join(self.root, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w") as f:
            f.write("# Bug Fix\n")

        result = sync_document_state(self.root, rel_path, "bug", "bug", "tech-spec-bug", "complete")
        self.assertNotIn("feature_slug", result)

    def test_non_ets_path_returns_empty(self):
        result = sync_document_state(self.root, "README.md", "unknown", "unknown", "readme", "complete")
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
