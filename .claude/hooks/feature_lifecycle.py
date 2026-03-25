#!/usr/bin/env python3
"""
feature_lifecycle.py — Feature state management, ID extraction, and phase routing.
"""

from __future__ import annotations

import os
import re
from typing import Any

from path_utils import split_ets_path
from yaml_io import read_frontmatter_markdown, read_yaml_file, write_frontmatter_markdown, write_yaml_file
from state_defaults import (
    FEATURE_DOC_KEYS,
    ID_PATTERNS,
    REPORT_DOC_TYPES,
    default_execution_status,
    default_feature_index,
    default_feature_status,
    default_project_status,
    default_workflow_state,
    docs_project_root,
    execution_status_path,
    execution_sync_path,
    feature_dir,
    normalize_execution_status,
    normalize_feature_index,
    normalize_feature_status,
    normalize_project_status,
    now_iso,
    rel_project_path,
    state_dir,
    title_from_slug,
)


# ─────────────────────────────────────────────────────────────────────────────
# Directory scaffolding
# ─────────────────────────────────────────────────────────────────────────────

def _default_elicitation_state() -> dict:
    """Minimal elicitation state — used as fallback if template is missing."""
    modules = {}
    for mod in ["ingest", "problem", "actors", "jobs", "journeys", "cases", "edges", "assumptions", "brainstorm", "synth"]:
        modules[mod] = {"status": "not_started", "questions_asked": 0}
        if mod not in ("ingest", "brainstorm", "synth"):
            modules[mod]["stories_collected"] = 0
            modules[mod]["snapshots"] = []
        if mod == "actors":
            modules[mod]["archetype_probes_done"] = False
        if mod == "brainstorm":
            modules[mod]["blocked_by"] = "Minimum coverage not met"
    return {
        "meta": {"mode": "product", "session_id": "", "started_at": "", "last_activity": ""},
        "current_module": "ingest",
        "current_probe": "",
        "questions_asked": 0,
        "stories_collected": 0,
        "module_state": modules,
        "response_quality": {"vague_count": 0, "escalated_count": 0, "dont_know_count": 0, "dont_know_classified": 0},
        "fatigue": {"threshold": 15, "current": 0, "offered_pause": False},
        "pending_probes": [],
        "unresolved_dimensions": [],
        "reflection_due": False,
        "active_archetypes": [],
        "checkpoints": [],
    }


def _ensure_project_dirs(project_root: str, project_slug: str) -> None:
    base = docs_project_root(project_root, project_slug)
    for folder in [
        "discovery",
        "planning",
        os.path.join("planning", "feature-specs"),
        "architecture",
        "data",
        "ux",
        "implementation",
        "features",
        "bugs",
        "spikes",
        "adrs",
        "learnings",
        "reports",
        "state",
        os.path.join("state", "reports"),
    ]:
        os.makedirs(os.path.join(base, folder), exist_ok=True)


def ensure_project_state(project_root: str, project_slug: str, execution_adapter: str = "none", mode: str = "product") -> None:
    _ensure_project_dirs(project_root, project_slug)
    project_status_path = os.path.join(state_dir(project_root, project_slug), "project-status.yaml")
    workflow_state_path = os.path.join(state_dir(project_root, project_slug), "workflow-state.yaml")
    feature_index_path = os.path.join(state_dir(project_root, project_slug), "feature-index.yaml")
    exec_status = execution_status_path(project_root, project_slug)
    exec_sync = execution_sync_path(project_root, project_slug)

    if not os.path.exists(project_status_path):
        write_yaml_file(project_status_path, default_project_status(project_slug, execution_adapter, mode))
    if not os.path.exists(workflow_state_path):
        write_yaml_file(workflow_state_path, default_workflow_state(project_slug))
    if not os.path.exists(feature_index_path):
        write_yaml_file(feature_index_path, default_feature_index(project_slug))
    # Elicitation state for interview resumability
    elicitation_state_path = os.path.join(state_dir(project_root, project_slug), "elicitation-state.yaml")
    if not os.path.exists(elicitation_state_path):
        template_path = os.path.join(
            project_root, ".claude", "skills", "discovery", "ideate", "knowledge", "elicitation-state.yaml"
        )
        if os.path.exists(template_path):
            import shutil
            shutil.copy2(template_path, elicitation_state_path)
        else:
            write_yaml_file(elicitation_state_path, _default_elicitation_state())
    if execution_adapter != "none" and not os.path.exists(exec_status):
        write_yaml_file(exec_status, default_execution_status(project_slug, execution_adapter))
    if execution_adapter == "linear" and not os.path.exists(exec_sync):
        from state_defaults import default_execution_sync
        write_yaml_file(exec_sync, default_execution_sync(execution_adapter))


def ensure_feature_state(
    project_root: str,
    project_slug: str,
    feature_slug: str,
    execution_adapter: str = "none",
    title: str | None = None,
) -> str:
    ensure_project_state(project_root, project_slug, execution_adapter=execution_adapter, mode="feature")
    folder = feature_dir(project_root, project_slug, feature_slug)
    os.makedirs(folder, exist_ok=True)
    feature_status_path = os.path.join(folder, "feature-status.md")
    if not os.path.exists(feature_status_path):
        from yaml_io import FEATURE_BODY_TEMPLATE
        write_frontmatter_markdown(
            feature_status_path,
            default_feature_status(project_slug, feature_slug, execution_adapter, title=title),
            FEATURE_BODY_TEMPLATE,
        )
    return feature_status_path


# ─────────────────────────────────────────────────────────────────────────────
# ID extraction
# ─────────────────────────────────────────────────────────────────────────────

def extract_feature_slug(inner_path: str) -> str | None:
    parts = inner_path.split("/")
    if len(parts) >= 2 and parts[0] == "features" and parts[1]:
        if parts[1] not in {"README.md", "_templates"} and "." not in parts[1]:
            return parts[1]

    patterns = [
        r"features/feature-brief-([^.]+)\.(?:md|yaml)$",
        r"features/user-stories-([^.]+)\.(?:md|yaml)$",
        r"features/design-delta-([^.]+)\.(?:md|yaml)$",
        r"features/impl-plan-([^.]+)\.(?:md|yaml)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, inner_path)
        if match:
            return match.group(1)
    return None


def extract_ids_from_text(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for key, pattern in ID_PATTERNS.items():
        values = sorted(set(re.findall(pattern, text)))
        result[key] = values
    return result


def _merge_unique(existing: list[str], new_items: list[str]) -> list[str]:
    return sorted(set((existing or []) + (new_items or [])))


def classify_etus_id(etus_id: str) -> str:
    if re.fullmatch(r"US-\d+", etus_id):
        return "story"
    if re.fullmatch(r"impl-\d+", etus_id):
        return "task"
    if re.fullmatch(r"FB-\d+", etus_id):
        return "feature_brief_item"
    if re.fullmatch(r"SOL-\d+", etus_id):
        return "solution"
    return "generic"


# ─────────────────────────────────────────────────────────────────────────────
# Phase routing
# ─────────────────────────────────────────────────────────────────────────────

def _feature_phase_for(doc_type: str) -> str:
    if doc_type == "solution-discovery":
        return "solution"
    if doc_type in {"feature-brief", "user-stories"}:
        return "requirements"
    if doc_type == "design-delta":
        return "design"
    if doc_type in {"impl-plan", "execution-status"}:
        return "implementation"
    return "ideate"


def _feature_next_step(doc_type: str, feature_slug: str, execution_adapter: str) -> str:
    if doc_type == "solution-discovery":
        return f"/feature brief {feature_slug}"
    if doc_type == "feature-brief":
        return f"/feature stories {feature_slug}"
    if doc_type == "user-stories":
        return f"/feature delta {feature_slug}"
    if doc_type == "design-delta":
        return f"/feature impl {feature_slug}"
    if doc_type == "impl-plan":
        return "/validate"
    return f"/feature ideate {feature_slug}"


def _product_next_step(doc_type: str) -> str:
    mapping = {
        "coverage-matrix": "/discover",
        "product-vision": "/plan opportunities",
        "baseline": "/plan opportunities",
        "discovery-report": "/plan opportunities",
        "report-discovery": "/plan opportunities",
        "ost": "/plan opportunities",
        "prioritization": "/solution",
        "report-opportunities": "/solution",
        "solution-discovery": "/plan requirements",
        "report-solution": "/plan requirements",
        "prd": "/plan requirements",
        "user-stories": "/design",
        "report-planning": "/design",
        "tech-spec": "/implement",
        "report-design": "/implement",
        "implementation-plan": "/implement",
        "quality-checklist": "/implement",
        "release-plan": "/validate",
        "report-implementation": "/validate",
        "execution-status": "/validate",
    }
    return mapping.get(doc_type, "/help")


def _finalize_phase(doc_type: str, mode: str) -> tuple[str | None, str | None]:
    if mode == "feature":
        if doc_type == "solution-discovery":
            return ("solution", "completed")
        if doc_type == "user-stories":
            return ("requirements", "completed")
        if doc_type == "design-delta":
            return ("design", "completed")
        if doc_type == "impl-plan":
            return ("implementation", "completed")
        if doc_type == "feature-brief":
            return ("requirements", "in_progress")
        return ("ideate", "in_progress")

    if mode == "product":
        if doc_type == "coverage-matrix":
            return ("ideate", "completed")
        if doc_type in {"product-vision", "discovery-report"}:
            return ("discovery", "completed")
        if doc_type == "prioritization":
            return ("opportunities", "completed")
        if doc_type == "solution-discovery":
            return ("solution", "completed")
        if doc_type in {"prd", "user-stories"}:
            return ("requirements", "in_progress")
        if doc_type in {"tech-spec", "api-spec"}:
            return ("design", "in_progress")
        if doc_type in {"implementation-plan", "quality-checklist", "release-plan"}:
            return ("implementation", "in_progress")
    return (None, None)


# ─────────────────────────────────────────────────────────────────────────────
# Project lookup
# ─────────────────────────────────────────────────────────────────────────────

def list_project_slugs(project_root: str) -> list[str]:
    projects_root = os.path.join(project_root, "docs", "ets", "projects")
    if not os.path.isdir(projects_root):
        return []
    return sorted(
        name
        for name in os.listdir(projects_root)
        if os.path.isdir(os.path.join(projects_root, name)) and not name.startswith("_")
    )


def find_single_project_slug(project_root: str) -> str | None:
    slugs = list_project_slugs(project_root)
    if len(slugs) == 1:
        return slugs[0]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Main state sync orchestrator
# ─────────────────────────────────────────────────────────────────────────────

def sync_document_state(
    project_root: str,
    rel_path: str,
    phase: str,
    mode: str,
    doc_type: str,
    status: str,
) -> dict[str, Any]:
    info = split_ets_path(rel_path)
    if not info.is_new_root or not info.project_slug:
        return {}

    project_slug = info.project_slug
    ensure_project_state(project_root, project_slug)
    st_path = state_dir(project_root, project_slug)
    project_status_path = os.path.join(st_path, "project-status.yaml")
    workflow_state_path = os.path.join(st_path, "workflow-state.yaml")
    feature_index_path = os.path.join(st_path, "feature-index.yaml")
    execution_status_file = execution_status_path(project_root, project_slug)
    project_status = normalize_project_status(read_yaml_file(project_status_path, {}), project_slug)
    workflow_state = read_yaml_file(workflow_state_path, default_workflow_state(project_slug))
    feature_index = normalize_feature_index(read_yaml_file(feature_index_path, {}), project_slug)
    execution_status = normalize_execution_status(
        read_yaml_file(execution_status_file, {}),
        project_slug,
        project_status.get("execution_adapter", "none"),
    )

    feature_slug = extract_feature_slug(info.inner_path)

    # Guard: don't create feature state when operating in bug or spike mode.
    # Feature slugs extracted from paths in bugs/ or spikes/ are false positives.
    if feature_slug and mode in {"bug", "spike"}:
        feature_slug = None

    if mode in {"product", "feature", "bug", "spike"}:
        project_status["mode"] = mode

    execution_adapter = project_status.get("execution_adapter", "none")
    project_status["project_slug"] = project_slug

    if feature_slug:
        project_status["active_feature_slug"] = feature_slug

    if doc_type == "project-status":
        project_status = normalize_project_status(read_yaml_file(project_status_path, project_status), project_slug, project_status.get("mode", mode))
        execution_adapter = project_status.get("execution_adapter", execution_adapter)
    elif doc_type == "execution-sync":
        execution_adapter = "linear"
        project_status["execution_adapter"] = "linear"
    elif doc_type == "execution-status":
        execution_status["execution_adapter"] = execution_adapter

    if mode == "feature":
        current_phase = _feature_phase_for(doc_type)
        next_step = _feature_next_step(doc_type, feature_slug or "feature", execution_adapter)
    elif mode == "product":
        current_phase = phase if phase in workflow_state.get("phase_status", {}) else "ideate"
        next_step = _product_next_step(doc_type)
    elif mode == "bug":
        current_phase = "implementation"
        next_step = "/validate"
    elif mode == "spike":
        current_phase = "discovery"
        next_step = "/help"
    else:
        current_phase = project_status.get("current_phase", "ideate")
        next_step = project_status.get("next_step", "/help")

    project_status["current_phase"] = current_phase
    project_status["next_step"] = next_step

    finalized_phase, phase_state = _finalize_phase(doc_type, mode)
    if finalized_phase:
        workflow_state.setdefault("phase_status", {})
        workflow_state["phase_status"][finalized_phase] = phase_state
        workflow_state["current_step"] = current_phase
        workflow_state["next_recommended_step"] = next_step
        if phase_state == "completed":
            workflow_state["last_completed_step"] = finalized_phase
            project_status["last_completed_phase"] = finalized_phase

    if doc_type in REPORT_DOC_TYPES:
        report_phase, report_state = REPORT_DOC_TYPES[doc_type]
        workflow_state.setdefault("reports", {})
        workflow_state["reports"][report_phase] = rel_path
        workflow_state.setdefault("phase_status", {})
        workflow_state["phase_status"][report_phase] = report_state
        workflow_state["last_completed_step"] = report_phase

    feature_result: dict[str, Any] = {}
    if feature_slug:
        feature_status_path = ensure_feature_state(
            project_root,
            project_slug,
            feature_slug,
            execution_adapter=execution_adapter,
            title=title_from_slug(feature_slug),
        )
        frontmatter, body = read_frontmatter_markdown(feature_status_path)
        if not frontmatter:
            frontmatter = default_feature_status(project_slug, feature_slug, execution_adapter)
        frontmatter = normalize_feature_status(frontmatter, project_slug, feature_slug, title_from_slug(feature_slug))

        frontmatter["project_slug"] = project_slug
        frontmatter["feature_slug"] = feature_slug
        frontmatter["execution_adapter"] = execution_adapter
        frontmatter["title"] = frontmatter.get("title") or title_from_slug(feature_slug)

        abs_saved_path = os.path.join(project_root, rel_path)
        text = ""
        if os.path.exists(abs_saved_path):
            with open(abs_saved_path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()

        ids_found = extract_ids_from_text(text)
        frontmatter.setdefault("traceability", default_feature_status(project_slug, feature_slug)["traceability"])
        for key, values in ids_found.items():
            frontmatter["traceability"][key] = _merge_unique(frontmatter["traceability"].get(key, []), values)

        frontmatter.setdefault("linked_docs", {})
        if doc_type in FEATURE_DOC_KEYS:
            frontmatter["linked_docs"][FEATURE_DOC_KEYS[doc_type]] = rel_path

        frontmatter.setdefault("gates", {})
        if doc_type == "solution-discovery":
            frontmatter["discovery_state"] = "solution_selected"
            frontmatter["current_step"] = "solution"
            frontmatter["last_completed_step"] = "solution"
            frontmatter["next_recommended_step"] = _feature_next_step(doc_type, feature_slug, execution_adapter)
            frontmatter["gates"]["solution_readiness_gate"] = "go" if status == "complete" else "pending"
        elif doc_type == "feature-brief":
            frontmatter["delivery_state"] = "brief_ready"
            frontmatter["current_step"] = "brief"
            frontmatter["last_completed_step"] = "brief"
            frontmatter["next_recommended_step"] = _feature_next_step(doc_type, feature_slug, execution_adapter)
            frontmatter["gates"]["feature_requirements_gate"] = "pending"
        elif doc_type == "user-stories":
            frontmatter["delivery_state"] = "stories_ready"
            frontmatter["current_step"] = "stories"
            frontmatter["last_completed_step"] = "stories"
            frontmatter["next_recommended_step"] = _feature_next_step(doc_type, feature_slug, execution_adapter)
            frontmatter["gates"]["feature_requirements_gate"] = "go" if status == "complete" else "pending"
        elif doc_type == "design-delta":
            frontmatter["delivery_state"] = "delta_ready"
            frontmatter["current_step"] = "delta"
            frontmatter["last_completed_step"] = "delta"
            frontmatter["next_recommended_step"] = _feature_next_step(doc_type, feature_slug, execution_adapter)
            frontmatter["gates"]["feature_delivery_gate"] = "pending"
        elif doc_type == "impl-plan":
            frontmatter["delivery_state"] = "impl_ready"
            frontmatter["current_step"] = "impl"
            frontmatter["last_completed_step"] = "impl"
            frontmatter["next_recommended_step"] = _feature_next_step(doc_type, feature_slug, execution_adapter)
            frontmatter["gates"]["feature_delivery_gate"] = "go" if status == "complete" else "pending"

        write_frontmatter_markdown(feature_status_path, frontmatter, body)

        feature_index.setdefault("features", {})
        feature_index["features"][feature_slug] = {
            "title": frontmatter.get("title", title_from_slug(feature_slug)),
            "execution_adapter": execution_adapter,
            "status_path": rel_project_path(project_slug, "features", feature_slug, "feature-status.md"),
            "discovery_state": frontmatter.get("discovery_state", "intake"),
            "delivery_state": frontmatter.get("delivery_state", "not_started"),
            "release_state": frontmatter.get("release_state", "not_released"),
            "governance_state": frontmatter.get("governance_state", "active"),
            "next_recommended_step": frontmatter.get("next_recommended_step", f"/feature {feature_slug}"),
            "updated_at": now_iso(),
        }

        if execution_adapter != "none":
            execution_status.setdefault("feature_rollups", {})
            execution_status["feature_rollups"][feature_slug] = {
                "execution_adapter": execution_adapter,
                "delivery_state": frontmatter.get("delivery_state", "not_started"),
                "release_state": frontmatter.get("release_state", "not_released"),
                "next_recommended_step": frontmatter.get("next_recommended_step", ""),
                "story_ids": frontmatter.get("traceability", {}).get("user_stories", []),
                "task_ids": frontmatter.get("traceability", {}).get("implementation_items", []),
                "status_path": rel_project_path(project_slug, "features", feature_slug, "feature-status.md"),
            }

            if doc_type == "user-stories":
                execution_status.setdefault("item_status", {})
                for story_id in frontmatter.get("traceability", {}).get("user_stories", []):
                    execution_status["item_status"].setdefault(
                        story_id,
                        {
                            "entity_type": "story",
                            "state": "todo" if execution_adapter == "local" else "tracked_in_external",
                            "unit": "",
                            "owner": "",
                            "progress": 0,
                            "feature_slug": feature_slug,
                            "source": execution_adapter,
                        },
                    )

            if doc_type == "impl-plan":
                execution_status.setdefault("item_status", {})
                for task_id in frontmatter.get("traceability", {}).get("implementation_items", []):
                    execution_status["item_status"].setdefault(
                        task_id,
                        {
                            "entity_type": "task",
                            "state": "todo" if execution_adapter == "local" else "tracked_in_external",
                            "unit": "",
                            "owner": "",
                            "estimate": "",
                            "actual": "",
                            "feature_slug": feature_slug,
                            "source": execution_adapter,
                        },
                    )
            execution_status["updated_at"] = now_iso()

        feature_result = {
            "feature_slug": feature_slug,
            "feature_status_path": feature_status_path,
            "next_recommended_step": frontmatter.get("next_recommended_step", ""),
        }

    write_yaml_file(project_status_path, project_status)
    write_yaml_file(workflow_state_path, workflow_state)
    write_yaml_file(feature_index_path, feature_index)
    if execution_adapter != "none":
        write_yaml_file(execution_status_file, execution_status)

    return {
        "project_status_path": project_status_path,
        "workflow_state_path": workflow_state_path,
        "feature_index_path": feature_index_path,
        "execution_status_path": execution_status_file if execution_adapter != "none" else "",
        "execution_adapter": execution_adapter,
        **feature_result,
    }
