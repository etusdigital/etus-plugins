#!/usr/bin/env python3
"""Tests for yaml_io.py — the stdlib-only YAML parser/dumper."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

# Ensure hooks directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from yaml_io import (
    _atomic_write,
    _format_scalar,
    _parse_list_block,
    _safe_scalar,
    dump_simple_yaml,
    parse_simple_yaml,
    read_frontmatter_markdown,
    read_yaml_file,
    write_frontmatter_markdown,
    write_yaml_file,
    FEATURE_BODY_TEMPLATE,
)


# ─── _safe_scalar ────────────────────────────────────────────────────────────


class TestSafeScalar(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(_safe_scalar(""), "")

    def test_true(self):
        self.assertIs(_safe_scalar("true"), True)

    def test_false(self):
        self.assertIs(_safe_scalar("false"), False)

    def test_null(self):
        self.assertIsNone(_safe_scalar("null"))

    def test_tilde_null(self):
        self.assertIsNone(_safe_scalar("~"))

    def test_integer(self):
        self.assertEqual(_safe_scalar("42"), 42)

    def test_negative_integer(self):
        self.assertEqual(_safe_scalar("-7"), -7)

    def test_float(self):
        self.assertAlmostEqual(_safe_scalar("3.14"), 3.14)

    def test_negative_float(self):
        self.assertAlmostEqual(_safe_scalar("-0.5"), -0.5)

    def test_json_array_inline(self):
        self.assertEqual(_safe_scalar('["a","b"]'), ["a", "b"])

    def test_json_object_inline(self):
        self.assertEqual(_safe_scalar('{"k":"v"}'), {"k": "v"})

    def test_quoted_string(self):
        self.assertEqual(_safe_scalar('"hello world"'), "hello world")

    def test_plain_string(self):
        self.assertEqual(_safe_scalar("hello"), "hello")

    def test_string_with_spaces(self):
        self.assertEqual(_safe_scalar("  hello  "), "hello")

    def test_string_that_looks_like_number_but_isnt(self):
        self.assertEqual(_safe_scalar("12abc"), "12abc")


# ─── parse_simple_yaml ───────────────────────────────────────────────────────


class TestParseSimpleYaml(unittest.TestCase):
    def test_flat_key_values(self):
        text = "name: my-project\nversion: 1\nenabled: true\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["name"], "my-project")
        self.assertEqual(result["version"], 1)
        self.assertIs(result["enabled"], True)

    def test_nested_dict(self):
        text = "parent:\n  child1: a\n  child2: b\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["parent"], {"child1": "a", "child2": "b"})

    def test_deeply_nested(self):
        text = "a:\n  b:\n    c: deep\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["a"]["b"]["c"], "deep")

    def test_empty_value_becomes_empty_dict(self):
        text = "parent:\nsibling: ok\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["parent"], {})
        self.assertEqual(result["sibling"], "ok")

    def test_comments_ignored(self):
        text = "# comment\nkey: value\n  # another comment\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["key"], "value")

    def test_blank_lines_ignored(self):
        text = "a: 1\n\n\nb: 2\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_frontmatter_separators_stripped(self):
        text = "---\nkey: value\n---\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["key"], "value")

    def test_list_items(self):
        text = "tags:\n  - alpha\n  - beta\n  - gamma\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["tags"], ["alpha", "beta", "gamma"])

    def test_empty_list_inline(self):
        text = "items: []\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["items"], [])

    def test_list_with_numbers(self):
        text = "scores:\n  - 10\n  - 20\n  - 30\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["scores"], [10, 20, 30])

    def test_list_with_booleans(self):
        text = "flags:\n  - true\n  - false\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["flags"], [True, False])

    def test_nested_dict_with_list(self):
        text = "config:\n  name: test\n  items:\n    - one\n    - two\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["config"]["name"], "test")
        self.assertEqual(result["config"]["items"], ["one", "two"])

    def test_multiple_lists(self):
        text = "fruits:\n  - apple\n  - banana\ncolors:\n  - red\n  - blue\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["fruits"], ["apple", "banana"])
        self.assertEqual(result["colors"], ["red", "blue"])

    def test_null_value(self):
        text = "key: null\n"
        result = parse_simple_yaml(text)
        self.assertIsNone(result["key"])

    def test_colon_in_value(self):
        text = "url: https://example.com\n"
        result = parse_simple_yaml(text)
        self.assertEqual(result["url"], "https://example.com")


# ─── dump_simple_yaml ────────────────────────────────────────────────────────


class TestDumpSimpleYaml(unittest.TestCase):
    def test_flat(self):
        data = {"name": "test", "version": 1}
        result = dump_simple_yaml(data)
        self.assertIn("name: test\n", result)
        self.assertIn("version: 1\n", result)

    def test_nested(self):
        data = {"parent": {"child": "value"}}
        result = dump_simple_yaml(data)
        self.assertIn("parent:\n", result)
        self.assertIn("  child: value\n", result)

    def test_empty_dict(self):
        data = {"empty": {}}
        result = dump_simple_yaml(data)
        self.assertIn("empty: {}\n", result)

    def test_list_multiline(self):
        data = {"items": ["a", "b", "c"]}
        result = dump_simple_yaml(data)
        self.assertIn("items:\n", result)
        self.assertIn("  - a\n", result)
        self.assertIn("  - b\n", result)
        self.assertIn("  - c\n", result)

    def test_empty_list(self):
        data = {"items": []}
        result = dump_simple_yaml(data)
        self.assertIn("items: []\n", result)

    def test_boolean_values(self):
        data = {"enabled": True, "disabled": False}
        result = dump_simple_yaml(data)
        self.assertIn("enabled: true\n", result)
        self.assertIn("disabled: false\n", result)

    def test_null_value(self):
        data = {"key": None}
        result = dump_simple_yaml(data)
        self.assertIn("key: null\n", result)

    def test_empty_string_quoted(self):
        data = {"key": ""}
        result = dump_simple_yaml(data)
        self.assertIn('key: ""\n', result)

    def test_string_with_spaces_quoted(self):
        data = {"key": "hello world"}
        result = dump_simple_yaml(data)
        self.assertIn('key: "hello world"\n', result)


# ─── Round-trip ──────────────────────────────────────────────────────────────


class TestRoundTrip(unittest.TestCase):
    def _roundtrip(self, data):
        dumped = dump_simple_yaml(data)
        parsed = parse_simple_yaml(dumped)
        self.assertEqual(parsed, data, f"Round-trip failed.\nDumped:\n{dumped}\nParsed: {parsed}")

    def test_flat(self):
        self._roundtrip({"name": "test", "version": 1, "enabled": True})

    def test_nested(self):
        self._roundtrip({"config": {"db": "postgres", "port": 5432}})

    def test_lists(self):
        self._roundtrip({"tags": ["a", "b", "c"]})

    def test_mixed(self):
        self._roundtrip({
            "project": "demo",
            "mode": "feature",
            "features": {"login": {"status": "ready"}},
            "tags": ["auth", "mvp"],
            "count": 3,
            "active": True,
            "notes": None,
        })

    def test_nested_list(self):
        self._roundtrip({
            "config": {
                "name": "test",
                "items": ["one", "two", "three"],
                "enabled": True,
            }
        })

    def test_empty_structures(self):
        self._roundtrip({"empty_dict": {}, "empty_list": []})

    def test_numeric_list(self):
        self._roundtrip({"scores": [10, 20, 30]})


# ─── File I/O ────────────────────────────────────────────────────────────────


class TestFileIO(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_and_read_yaml(self):
        path = os.path.join(self.root, "test.yaml")
        data = {"name": "project", "version": 2, "tags": ["a", "b"]}
        write_yaml_file(path, data)
        result = read_yaml_file(path)
        self.assertEqual(result, data)

    def test_read_missing_file_returns_default(self):
        result = read_yaml_file("/nonexistent/path.yaml", {"fallback": True})
        self.assertEqual(result, {"fallback": True})

    def test_read_missing_file_returns_empty_dict(self):
        result = read_yaml_file("/nonexistent/path.yaml")
        self.assertEqual(result, {})

    def test_write_creates_directories(self):
        path = os.path.join(self.root, "a", "b", "c", "test.yaml")
        write_yaml_file(path, {"key": "value"})
        self.assertTrue(os.path.exists(path))

    def test_frontmatter_write_and_read(self):
        path = os.path.join(self.root, "feature-status.md")
        fm = {"title": "Login", "status": "active", "tags": ["auth", "mvp"]}
        body = "# My Feature\n\nSome description.\n"
        write_frontmatter_markdown(path, fm, body)
        result_fm, result_body = read_frontmatter_markdown(path)
        self.assertEqual(result_fm, fm)
        self.assertIn("# My Feature", result_body)

    def test_frontmatter_missing_file(self):
        fm, body = read_frontmatter_markdown("/nonexistent/path.md")
        self.assertEqual(fm, {})
        self.assertEqual(body, FEATURE_BODY_TEMPLATE)

    def test_frontmatter_no_frontmatter(self):
        path = os.path.join(self.root, "plain.md")
        with open(path, "w") as f:
            f.write("# Just markdown\n\nNo frontmatter here.\n")
        fm, body = read_frontmatter_markdown(path)
        self.assertEqual(fm, {})
        self.assertIn("# Just markdown", body)

    def test_frontmatter_unclosed(self):
        path = os.path.join(self.root, "broken.md")
        with open(path, "w") as f:
            f.write("---\ntitle: broken\nNo closing separator\n")
        fm, body = read_frontmatter_markdown(path)
        self.assertEqual(fm, {})


# ─── Atomic writes ───────────────────────────────────────────────────────────


class TestAtomicWrite(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_basic_write(self):
        path = os.path.join(self.root, "test.txt")
        _atomic_write(path, "hello")
        with open(path) as f:
            self.assertEqual(f.read(), "hello")

    def test_creates_parent_dirs(self):
        path = os.path.join(self.root, "a", "b", "test.txt")
        _atomic_write(path, "deep")
        self.assertTrue(os.path.exists(path))

    def test_no_temp_files_left(self):
        path = os.path.join(self.root, "clean.txt")
        _atomic_write(path, "content")
        files = os.listdir(self.root)
        self.assertEqual(files, ["clean.txt"])

    def test_overwrites_existing(self):
        path = os.path.join(self.root, "overwrite.txt")
        _atomic_write(path, "first")
        _atomic_write(path, "second")
        with open(path) as f:
            self.assertEqual(f.read(), "second")


# ─── _format_scalar ──────────────────────────────────────────────────────────


class TestFormatScalar(unittest.TestCase):
    def test_bool_true(self):
        self.assertEqual(_format_scalar(True), "true")

    def test_bool_false(self):
        self.assertEqual(_format_scalar(False), "false")

    def test_none(self):
        self.assertEqual(_format_scalar(None), "null")

    def test_int(self):
        self.assertEqual(_format_scalar(42), "42")

    def test_float(self):
        self.assertEqual(_format_scalar(3.14), "3.14")

    def test_simple_string(self):
        self.assertEqual(_format_scalar("hello"), "hello")

    def test_string_with_spaces_gets_quoted(self):
        result = _format_scalar("hello world")
        self.assertTrue(result.startswith('"') and result.endswith('"'))

    def test_empty_string(self):
        self.assertEqual(_format_scalar(""), '""')

    def test_url_unquoted(self):
        self.assertEqual(_format_scalar("https://example.com"), "https://example.com")

    def test_reserved_words_get_quoted(self):
        result = _format_scalar("true")
        self.assertTrue(result.startswith('"'))


if __name__ == "__main__":
    unittest.main()
