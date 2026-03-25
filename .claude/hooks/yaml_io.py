#!/usr/bin/env python3
"""
yaml_io.py — Lightweight YAML parsing/dumping and frontmatter I/O.

Uses a small YAML subset so it runs with Python stdlib only (no PyYAML).
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from typing import Any


def _atomic_write(path: str, content: str) -> None:
    """Write content to a file atomically using tempfile + os.replace."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(path),
        prefix=".tmp_",
        suffix=os.path.splitext(path)[1],
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _safe_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return ""
    if raw in {"true", "false"}:
        return raw == "true"
    if raw in {"null", "~"}:
        return None
    if raw.startswith("[") or raw.startswith("{"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    if raw.startswith('"') and raw.endswith('"'):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw.strip('"')
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d+\.\d+", raw):
        return float(raw)
    return raw


def _parse_list_block(lines: list[str], start: int, indent: int) -> tuple[list[Any], int]:
    """Parse a YAML list block (lines starting with '- ')."""
    items: list[Any] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        current_indent = len(line) - len(line.lstrip(" "))
        if current_indent < indent:
            break
        if current_indent > indent:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("- "):
            break
        item_value = stripped[2:].strip()
        items.append(_safe_scalar(item_value))
        i += 1
    return items, i


def parse_simple_yaml(text: str) -> dict[str, Any]:
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != "---"]

    def parse_block(start: int, indent: int) -> tuple[dict[str, Any], int]:
        data: dict[str, Any] = {}
        i = start
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.lstrip().startswith("#"):
                i += 1
                continue
            current_indent = len(line) - len(line.lstrip(" "))
            if current_indent < indent:
                break
            if current_indent > indent:
                i += 1
                continue
            stripped = line.strip()
            # Skip bare list items at this level (they belong to a parent key)
            if stripped.startswith("- ") and ":" not in stripped.split("- ", 1)[1].split("#")[0]:
                i += 1
                continue
            if ":" not in stripped:
                i += 1
                continue
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()

            if raw_value == "":
                j = i + 1
                while j < len(lines) and (not lines[j].strip() or lines[j].lstrip().startswith("#")):
                    j += 1
                if j >= len(lines):
                    data[key] = {}
                    i = j
                    continue
                next_indent = len(lines[j]) - len(lines[j].lstrip(" "))
                if next_indent <= current_indent:
                    data[key] = {}
                    i = j
                    continue
                # Check if the next block is a list (starts with '- ')
                next_stripped = lines[j].strip()
                if next_stripped.startswith("- "):
                    value_list, j = _parse_list_block(lines, j, next_indent)
                    data[key] = value_list
                else:
                    value, j = parse_block(j, next_indent)
                    data[key] = value
                i = j
                continue

            data[key] = _safe_scalar(raw_value)
            i += 1
        return data, i

    parsed, _ = parse_block(0, 0)
    return parsed


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if value == "":
        return '""'
    if re.fullmatch(r"[A-Za-z0-9_./:@+-]+", str(value)) and value not in {"true", "false", "null"}:
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def dump_simple_yaml(data: dict[str, Any], indent: int = 0) -> str:
    lines: list[str] = []
    for key, value in data.items():
        prefix = " " * indent + f"{key}:"
        if isinstance(value, dict):
            if value:
                lines.append(prefix)
                lines.append(dump_simple_yaml(value, indent + 2).rstrip("\n"))
            else:
                lines.append(f"{prefix} {{}}")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix} []")
            else:
                lines.append(prefix)
                for item in value:
                    lines.append(" " * (indent + 2) + f"- {_format_scalar(item)}")
        else:
            lines.append(f"{prefix} {_format_scalar(value)}")
    return "\n".join(lines) + "\n"


def read_yaml_file(path: str, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not os.path.exists(path):
        return dict(default or {})
    with open(path, "r", encoding="utf-8") as fh:
        return parse_simple_yaml(fh.read())


def write_yaml_file(path: str, data: dict[str, Any]) -> None:
    _atomic_write(path, dump_simple_yaml(data))


FEATURE_BODY_TEMPLATE = """# Feature Status

## Summary

[Human-readable summary of the feature]

## Current Situation

[What is currently true about this feature]

## Key Risks

- [Risk 1]
- [Risk 2]

## Rollout Notes

[Rollout plan, flag state, environment notes]

## Cleanup Notes

[Cleanup/stale/archive notes]
"""


def read_frontmatter_markdown(path: str) -> tuple[dict[str, Any], str]:
    if not os.path.exists(path):
        return {}, FEATURE_BODY_TEMPLATE

    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    if not text.startswith("---"):
        return {}, text or FEATURE_BODY_TEMPLATE

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text or FEATURE_BODY_TEMPLATE

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return {}, text or FEATURE_BODY_TEMPLATE

    frontmatter = parse_simple_yaml("\n".join(lines[1:end_idx]))
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    return frontmatter, body or FEATURE_BODY_TEMPLATE


def write_frontmatter_markdown(path: str, frontmatter: dict[str, Any], body: str) -> None:
    content = "---\n" + dump_simple_yaml(frontmatter) + "---\n\n" + (body or FEATURE_BODY_TEMPLATE).rstrip() + "\n"
    _atomic_write(path, content)
