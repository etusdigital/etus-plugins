#!/usr/bin/env python3
"""
linear_sync.py — Linear integration: mapping sync and cycle projection.
"""

from __future__ import annotations

from typing import Any

from yaml_io import read_yaml_file, write_yaml_file
from state_defaults import (
    default_execution_status,
    default_execution_sync,
    execution_status_path,
    execution_sync_path,
    normalize_execution_status,
    normalize_execution_sync,
    normalize_project_status,
    now_iso,
    state_dir,
)
from feature_lifecycle import classify_etus_id, ensure_project_state

import os


def sync_linear_mapping(
    project_root: str,
    project_slug: str,
    etus_id: str,
    linear_id: str,
    title: str = "",
    item_type: str = "",
    status: str = "",
) -> str:
    ensure_project_state(project_root, project_slug, execution_adapter="linear", mode="product")
    execution_sync_file = execution_sync_path(project_root, project_slug)
    project_status_path = os.path.join(state_dir(project_root, project_slug), "project-status.yaml")
    execution_status_file = execution_status_path(project_root, project_slug)
    execution_sync = normalize_execution_sync(
        read_yaml_file(execution_sync_file, {}),
        "linear",
    )
    project_status = normalize_project_status(
        read_yaml_file(project_status_path, {}),
        project_slug,
        "product",
    )
    execution_status = normalize_execution_status(
        read_yaml_file(execution_status_file, {}),
        project_slug,
        "linear",
    )

    execution_sync["execution_adapter"] = "linear"
    execution_sync["last_sync_at"] = now_iso()
    execution_sync["sync_status"] = "healthy"
    execution_sync.setdefault("source_of_truth", {"documentation_core": "local", "execution_projection": "linear"})
    execution_sync.setdefault("projection", {"stories": {}, "tasks": {}})
    execution_sync.setdefault("external_units", {})
    execution_sync.setdefault("mappings", {})
    execution_sync.setdefault("runs", [])
    execution_sync.setdefault("conflicts", [])
    entity_kind = classify_etus_id(etus_id)
    execution_sync["mappings"][etus_id] = {
        "linear_id": linear_id,
        "title": title,
        "type": item_type or entity_kind,
        "status": status,
        "updated_at": now_iso(),
    }
    execution_sync["runs"].append(
        {
            "at": now_iso(),
            "kind": "mapping_update",
            "etus_id": etus_id,
            "linear_id": linear_id,
            "entity_kind": entity_kind,
        }
    )

    if entity_kind == "story":
        execution_sync["projection"].setdefault("stories", {})
        execution_sync["projection"]["stories"][etus_id] = {
            "linear_id": linear_id,
            "status": status,
            "title": title,
            "updated_at": now_iso(),
        }
        execution_status.setdefault("item_status", {})
        execution_status["item_status"].setdefault(
            etus_id,
            {"entity_type": "story", "state": "tracked_in_external", "unit": "", "owner": "", "progress": 0},
        )
        execution_status["item_status"][etus_id]["external_id"] = linear_id
        execution_status["item_status"][etus_id]["external_status"] = status
        execution_status["item_status"][etus_id]["source"] = "linear"
        execution_status["item_status"][etus_id]["updated_at"] = now_iso()

    if entity_kind == "task":
        execution_sync["projection"].setdefault("tasks", {})
        execution_sync["projection"]["tasks"][etus_id] = {
            "linear_id": linear_id,
            "status": status,
            "title": title,
            "updated_at": now_iso(),
        }
        execution_status.setdefault("item_status", {})
        execution_status["item_status"].setdefault(
            etus_id,
            {"entity_type": "task", "state": "tracked_in_external", "unit": "", "owner": "", "estimate": "", "actual": ""},
        )
        execution_status["item_status"][etus_id]["external_id"] = linear_id
        execution_status["item_status"][etus_id]["external_status"] = status
        execution_status["item_status"][etus_id]["source"] = "linear"
        execution_status["item_status"][etus_id]["updated_at"] = now_iso()

    project_status["execution_adapter"] = "linear"
    execution_status["execution_adapter"] = "linear"
    execution_status["updated_at"] = now_iso()
    write_yaml_file(execution_sync_file, execution_sync)
    write_yaml_file(project_status_path, project_status)
    write_yaml_file(execution_status_file, execution_status)
    return execution_sync_file


def sync_linear_cycle(
    project_root: str,
    project_slug: str,
    cycle_id: str,
    cycle_name: str = "",
    state: str = "active",
    start: str = "",
    end: str = "",
    story_ids: list[str] | None = None,
    task_ids: list[str] | None = None,
) -> str:
    story_ids = story_ids or []
    task_ids = task_ids or []

    ensure_project_state(project_root, project_slug, execution_adapter="linear", mode="product")
    execution_sync_file = execution_sync_path(project_root, project_slug)
    project_status_path = os.path.join(state_dir(project_root, project_slug), "project-status.yaml")
    execution_status_file = execution_status_path(project_root, project_slug)

    execution_sync = normalize_execution_sync(
        read_yaml_file(execution_sync_file, {}),
        "linear",
    )
    project_status = normalize_project_status(
        read_yaml_file(project_status_path, {}),
        project_slug,
        "product",
    )
    execution_status = normalize_execution_status(
        read_yaml_file(execution_status_file, {}),
        project_slug,
        "linear",
    )

    execution_sync["execution_adapter"] = "linear"
    execution_sync["last_sync_at"] = now_iso()
    execution_sync["sync_status"] = "healthy"
    execution_sync.setdefault("external_units", {})
    execution_sync.setdefault("runs", [])
    execution_sync["external_units"][cycle_id] = {
        "name": cycle_name or cycle_id,
        "state": state,
        "start": start,
        "end": end,
        "story_ids": sorted(set(story_ids)),
        "task_ids": sorted(set(task_ids)),
        "updated_at": now_iso(),
    }
    execution_sync["runs"].append(
        {
            "at": now_iso(),
            "kind": "cycle_projection",
            "cycle_id": cycle_id,
            "story_count": len(story_ids),
            "task_count": len(task_ids),
        }
    )

    project_status["execution_adapter"] = "linear"

    execution_status["execution_adapter"] = "linear"
    execution_status["current_unit"] = cycle_id
    execution_status.setdefault("units", {})
    execution_status["units"][cycle_id] = {
        "state": state,
        "start": start,
        "end": end,
        "capacity": "",
        "velocity": "",
        "source": "linear",
        "stories": sorted(set(story_ids)),
        "tasks": sorted(set(task_ids)),
    }
    execution_status.setdefault("item_status", {})
    for story_id in story_ids:
        execution_status["item_status"].setdefault(
            story_id,
            {"entity_type": "story", "state": "tracked_in_external", "unit": cycle_id, "owner": "", "progress": 0},
        )
        execution_status["item_status"][story_id]["unit"] = cycle_id
        execution_status["item_status"][story_id]["source"] = "linear"
        execution_status["item_status"][story_id]["updated_at"] = now_iso()

    for task_id in task_ids:
        execution_status["item_status"].setdefault(
            task_id,
            {"entity_type": "task", "state": "tracked_in_external", "unit": cycle_id, "owner": "", "estimate": "", "actual": ""},
        )
        execution_status["item_status"][task_id]["unit"] = cycle_id
        execution_status["item_status"][task_id]["source"] = "linear"
        execution_status["item_status"][task_id]["updated_at"] = now_iso()

    execution_status["updated_at"] = now_iso()

    write_yaml_file(execution_sync_file, execution_sync)
    write_yaml_file(project_status_path, project_status)
    write_yaml_file(execution_status_file, execution_status)
    return execution_sync_file
