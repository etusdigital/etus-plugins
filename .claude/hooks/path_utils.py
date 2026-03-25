#!/usr/bin/env python3
"""
Shared path helpers for ETUS PMDocs hooks.

Supports:
- docs/ets/projects/{project-slug}/...
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class EtsPathInfo:
    docs_root: str | None
    project_slug: str | None
    inner_path: str
    is_new_root: bool


def project_root_from(path_file: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(path_file), "../.."))


def resolve_docs_root(project_root: str) -> str:
    return os.path.join(project_root, "docs", "ets")


def resolve_memory_dir(project_root: str) -> str:
    return os.path.join(resolve_docs_root(project_root), ".memory")


def split_ets_path(rel_path: str) -> EtsPathInfo:
    rel_path = rel_path.replace("\\", "/")
    while rel_path.startswith("./"):
        rel_path = rel_path[2:]

    if rel_path.startswith("docs/ets/projects/"):
        remainder = rel_path[len("docs/ets/projects/") :]
        parts = remainder.split("/", 1)
        if len(parts) == 2:
            project_slug, inner = parts
            return EtsPathInfo(
                docs_root="docs/ets",
                project_slug=project_slug,
                inner_path=inner,
                is_new_root=True,
            )

    if rel_path.startswith("docs/ets/"):
        inner = rel_path[len("docs/ets/") :]
        return EtsPathInfo(
            docs_root="docs/ets",
            project_slug=None,
            inner_path=inner,
            is_new_root=True,
        )

    return EtsPathInfo(
        docs_root=None,
        project_slug=None,
        inner_path=rel_path,
        is_new_root=False,
    )
