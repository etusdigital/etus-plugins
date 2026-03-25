#!/usr/bin/env python3
"""
state_defaults.py — Default state templates, normalization, path helpers, and constants.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any


# ─────────────────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "feature"


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.replace("_", "-").split("-") if part)


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

ID_PATTERNS = {
    "actors": r"\bACT-\d+\b",
    "jtbd": r"\bJTBD-\d+\b",
    "journeys": r"\bJOUR-\d+\b",
    "use_cases": r"\bUC-\d+\b",
    "edge_cases": r"\bEDGE-\d+\b",
    "assumptions": r"\bASM-\d+\b",
    "non_goals": r"\bNG-\d+\b",
    "solutions": r"\bSOL-\d+\b",
    "feature_brief_items": r"\bFB-\d+\b",
    "user_stories": r"\bUS-\d+\b",
    "implementation_items": r"\bimpl-\d+\b",
}

FEATURE_DOC_KEYS = {
    "solution-discovery": "solution_discovery",
    "feature-brief": "feature_brief",
    "user-stories": "user_stories",
    "design-delta": "design_delta",
    "impl-plan": "implementation_plan",
}

SEMANTIC_DIMENSIONS = {
    "problem_clarity": "missing",
    "trigger_and_preconditions": "missing",
    "core_behavior": "missing",
    "success_signal": "missing",
    "anti_requirements": "missing",
    "actors_and_permissions": "missing",
    "failure_modes": "missing",
    "data_mutations": "missing",
    "degraded_behavior": "missing",
    "side_effects": "missing",
    "observability": "missing",
}

MODE_DIMENSION_RULES = {
    "product": {
        "required": ["problem_clarity", "trigger_and_preconditions", "core_behavior", "success_signal", "anti_requirements", "actors_and_permissions", "failure_modes"],
        "conditional": ["data_mutations"],
        "recommended": ["degraded_behavior", "side_effects", "observability"],
    },
    "feature": {
        "required": ["problem_clarity", "trigger_and_preconditions", "core_behavior", "success_signal"],
        "conditional": ["anti_requirements", "actors_and_permissions", "failure_modes", "data_mutations", "side_effects", "observability"],
        "recommended": ["degraded_behavior"],
    },
    "bug": {
        "required": ["problem_clarity", "trigger_and_preconditions", "core_behavior", "success_signal", "failure_modes"],
        "conditional": ["actors_and_permissions", "data_mutations", "degraded_behavior", "side_effects", "observability"],
        "recommended": [],
    },
    "spike": {
        "required": ["problem_clarity"],
        "conditional": ["failure_modes"],
        "recommended": ["success_signal"],
    },
}

REPORT_DOC_TYPES = {
    "report-discovery": ("discovery", "completed"),
    "report-opportunities": ("opportunities", "completed"),
    "report-solution": ("solution", "completed"),
    "report-planning": ("requirements", "completed"),
    "report-design": ("design", "completed"),
    "report-implementation": ("implementation", "completed"),
}


# ─────────────────────────────────────────────────────────────────────────────
# Path helpers
# ─────────────────────────────────────────────────────────────────────────────

def docs_project_root(project_root: str, project_slug: str) -> str:
    return os.path.join(project_root, "docs", "ets", "projects", project_slug)


def state_dir(project_root: str, project_slug: str) -> str:
    return os.path.join(docs_project_root(project_root, project_slug), "state")


def execution_status_path(project_root: str, project_slug: str) -> str:
    return os.path.join(state_dir(project_root, project_slug), "execution-status.yaml")


def execution_sync_path(project_root: str, project_slug: str) -> str:
    return os.path.join(state_dir(project_root, project_slug), "execution-sync.yaml")


def feature_dir(project_root: str, project_slug: str, feature_slug: str) -> str:
    return os.path.join(docs_project_root(project_root, project_slug), "features", feature_slug)


def rel_project_path(project_slug: str, *parts: str) -> str:
    return "/".join(["docs/ets/projects", project_slug, *parts])


# ─────────────────────────────────────────────────────────────────────────────
# Default state factories
# ─────────────────────────────────────────────────────────────────────────────

def default_gate_state() -> dict[str, Any]:
    """Expanded gate decision state — stores feedback, rejected approaches,
    and iteration history so downstream phases know what was already tried."""
    return {
        "status": "pending",
        "feedback": "",
        "timestamp": "",
        "rejected_approaches": [],
        "iteration_count": 0,
        "unresolved_objections": [],
    }


def default_project_status(project_slug: str, execution_adapter: str = "none", mode: str = "product") -> dict[str, Any]:
    return {
        "schema": "etus/project-status@v1",
        "workflow_version": "6.0",
        "project_slug": project_slug,
        "mode": mode,
        "execution_adapter": execution_adapter,
        "current_phase": "ideate",
        "last_completed_phase": "",
        "next_step": "/ideate",
        "sync_blocked": False,
    }


def default_workflow_state(project_slug: str) -> dict[str, Any]:
    return {
        "schema": "etus/workflow-state@v1",
        "project_slug": project_slug,
        "gates": {
            "ideation_readiness": default_gate_state(),
            "discovery_gate": default_gate_state(),
            "opportunity_focus_gate": default_gate_state(),
            "solution_readiness_gate": default_gate_state(),
            "requirements_gate": default_gate_state(),
            "implementation_readiness_gate": default_gate_state(),
        },
        "phase_status": {
            "ideate": "not_started",
            "discovery": "not_started",
            "opportunities": "not_started",
            "solution": "not_started",
            "requirements": "not_started",
            "design": "not_started",
            "implementation": "not_started",
            "release": "not_started",
            "retrospective": "not_started",
        },
        "reports": {},
        "current_step": "ideate",
        "last_completed_step": "",
        "next_recommended_step": "/ideate",
    }


def default_feature_index(project_slug: str) -> dict[str, Any]:
    return {
        "schema": "etus/feature-index@v1",
        "project_slug": project_slug,
        "features": {},
    }


def default_execution_status(project_slug: str, execution_adapter: str = "none") -> dict[str, Any]:
    return {
        "schema": "etus/execution-status@v1",
        "project_slug": project_slug,
        "execution_adapter": execution_adapter,
        "current_unit": "",
        "units": {},
        "item_status": {},
        "feature_rollups": {},
        "updated_at": now_iso(),
    }


def default_execution_sync(execution_adapter: str = "linear") -> dict[str, Any]:
    return {
        "schema": "etus/execution-sync@v1",
        "execution_adapter": execution_adapter,
        "workspace": "",
        "team": "",
        "precedence": "documentation_core_wins",
        "sync_direction": "bidirectional",
        "source_of_truth": {
            "documentation_core": "local",
            "execution_projection": execution_adapter,
        },
        "last_sync_at": "",
        "sync_status": "healthy",
        "external_units": {},
        "projection": {
            "stories": {},
            "tasks": {},
        },
        "mappings": {},
        "conflicts": [],
        "runs": [],
    }


def default_feature_status(
    project_slug: str,
    feature_slug: str,
    execution_adapter: str = "none",
    title: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": "etus/feature-status@v1",
        "workflow_version": "6.0",
        "project_slug": project_slug,
        "feature_slug": feature_slug,
        "title": title or title_from_slug(feature_slug),
        "mode": "feature",
        "execution_adapter": execution_adapter,
        "discovery_state": "intake",
        "delivery_state": "not_started",
        "release_state": "not_released",
        "governance_state": "active",
        "risk_state": {
            "value": "open",
            "usability": "open",
            "viability": "open",
            "feasibility": "open",
        },
        "current_step": "ideate",
        "last_completed_step": "",
        "next_recommended_step": f"/feature ideate {feature_slug}",
        "linked_docs": {
            "solution_discovery": "",
            "feature_brief": "",
            "user_stories": "",
            "design_delta": "",
            "implementation_plan": "",
        },
        "traceability": {
            "actors": [],
            "jtbd": [],
            "journeys": [],
            "use_cases": [],
            "edge_cases": [],
            "assumptions": [],
            "non_goals": [],
            "solutions": [],
            "feature_brief_items": [],
            "user_stories": [],
            "implementation_items": [],
        },
        "gates": {
            "solution_readiness_gate": default_gate_state(),
            "feature_requirements_gate": default_gate_state(),
            "feature_delivery_gate": default_gate_state(),
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Normalization
# ─────────────────────────────────────────────────────────────────────────────

def normalize_project_status(data: dict[str, Any], project_slug: str = "", mode: str = "product") -> dict[str, Any]:
    merged = default_project_status(project_slug or data.get("project_slug", ""), mode=mode)
    merged.update(data or {})
    if merged.get("execution_adapter") in {"", None}:
        merged["execution_adapter"] = "none"
    return merged


def normalize_feature_status(
    data: dict[str, Any],
    project_slug: str,
    feature_slug: str,
    title: str | None = None,
) -> dict[str, Any]:
    merged = default_feature_status(project_slug, feature_slug, title=title)
    merged.update(data or {})
    if title and not merged.get("title"):
        merged["title"] = title
    return merged


def normalize_feature_index(data: dict[str, Any], project_slug: str) -> dict[str, Any]:
    merged = default_feature_index(project_slug)
    merged.update(data or {})
    merged.setdefault("features", {})
    return merged


def normalize_execution_status(data: dict[str, Any], project_slug: str, execution_adapter: str = "none") -> dict[str, Any]:
    if not data:
        return default_execution_status(project_slug, execution_adapter)
    merged = default_execution_status(project_slug, execution_adapter)
    merged.update(data)
    return merged


def normalize_execution_sync(data: dict[str, Any], execution_adapter: str = "linear") -> dict[str, Any]:
    if not data:
        return default_execution_sync(execution_adapter)
    merged = default_execution_sync(execution_adapter)
    merged.update(data)
    return merged
