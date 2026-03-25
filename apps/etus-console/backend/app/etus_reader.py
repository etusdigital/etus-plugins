from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from .models import (
    ArtifactDetail,
    ArtifactSummary,
    FeatureDetail,
    FeatureSummary,
    GateSummary,
    MemoryDocument,
    MemoryResponse,
    ProjectDetail,
    ProjectSummary,
    ValidationSummary,
)


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".claude" / "hooks" / "state_utils.py").exists() and (parent / "docs" / "ets").exists():
            return parent
    raise RuntimeError("Nao foi possivel localizar a raiz do repo do ETUS.")


REPO_ROOT = find_repo_root()
HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"

if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))

from state_utils import read_frontmatter_markdown, read_yaml_file  # noqa: E402


DOCS_ROOT = REPO_ROOT / "docs" / "ets"
PROJECTS_ROOT = DOCS_ROOT / "projects"
MEMORY_ROOT = DOCS_ROOT / ".memory"


PROJECT_ARTIFACTS: list[tuple[str, str, str]] = [
    ("opportunity-pack", "discovery", "discovery/opportunity-pack.md"),
    ("project-context", "discovery", "discovery/project-context.md"),
    ("baseline", "discovery", "discovery/baseline.md"),
    ("discovery-report", "discovery", "discovery/discovery-report.md"),
    ("product-vision", "discovery", "discovery/product-vision.md"),
    ("ost", "planning", "planning/ost.md"),
    ("prioritization", "planning", "planning/prioritization.md"),
    ("solution-discovery", "planning", "planning/solution-discovery.md"),
    ("prd", "planning", "planning/prd.md"),
    ("user-stories", "planning", "planning/user-stories.md"),
    ("architecture-diagram", "design", "architecture/architecture-diagram.md"),
    ("tech-spec", "design", "architecture/tech-spec.md"),
    ("api-spec", "implementation", "implementation/api-spec.md"),
    ("implementation-plan", "implementation", "implementation/implementation-plan.md"),
    ("quality-checklist", "implementation", "implementation/quality-checklist.md"),
    ("release-plan", "implementation", "implementation/release-plan.md"),
]

FEATURE_ARTIFACTS: list[tuple[str, str]] = [
    ("feature-status", "feature-status.md"),
    ("solution-discovery", "solution-discovery.md"),
    ("feature-brief", "feature-brief.md"),
    ("user-stories", "user-stories.md"),
    ("design-delta", "design-delta.md"),
    ("impl-plan", "impl-plan.md"),
]


def project_dir(project_slug: str) -> Path:
    return PROJECTS_ROOT / project_slug


def ensure_project_exists(project_slug: str) -> Path:
    path = project_dir(project_slug)
    if not path.is_dir():
        raise FileNotFoundError(f"Projeto '{project_slug}' nao encontrado.")
    return path


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def file_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    head = load_text(path)[:2000].lower()
    if "status: draft" in head:
        return "draft"
    return "complete"


def iso_mtime(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def excerpt(text: str, limit: int = 500) -> str:
    compact = text.strip()
    return compact[:limit] + ("..." if len(compact) > limit else "")


def discover_project_slugs() -> list[str]:
    if not PROJECTS_ROOT.exists():
        return []
    return sorted(
        item.name
        for item in PROJECTS_ROOT.iterdir()
        if item.is_dir() and not item.name.startswith("_")
    )


def load_project_status(project_slug: str) -> dict[str, Any]:
    return read_yaml_file(project_dir(project_slug) / "state" / "project-status.yaml", {})


def load_workflow_state(project_slug: str) -> dict[str, Any]:
    return read_yaml_file(project_dir(project_slug) / "state" / "workflow-state.yaml", {})


def load_feature_index(project_slug: str) -> dict[str, Any]:
    return read_yaml_file(project_dir(project_slug) / "state" / "feature-index.yaml", {})


def load_feature_status(project_slug: str, feature_slug: str) -> tuple[dict[str, Any], str]:
    return read_frontmatter_markdown(project_dir(project_slug) / "features" / feature_slug / "feature-status.md")


def build_gate_summary(workflow: dict[str, Any]) -> GateSummary:
    gates = workflow.get("gates", {}) if workflow else {}
    blocked = [f"{name}:{value}" for name, value in gates.items() if value not in {"pending", "go"}]
    last_gate = " | ".join(blocked) if blocked else None
    return GateSummary(gates=gates, last_gate=last_gate)


def build_project_artifacts(project_slug: str) -> list[ArtifactSummary]:
    base = ensure_project_exists(project_slug)
    artifacts: list[ArtifactSummary] = []
    for kind, phase, rel_path in PROJECT_ARTIFACTS:
        path = base / rel_path
        artifacts.append(
            ArtifactSummary(
                key=rel_path,
                path=str(path),
                kind=kind,
                phase=phase,
                exists=path.exists(),
                status=file_status(path),
                updated_at=iso_mtime(path),
            )
        )
    return artifacts


def build_feature_summaries(project_slug: str) -> list[FeatureSummary]:
    ensure_project_exists(project_slug)
    feature_index = load_feature_index(project_slug)
    features = feature_index.get("features", {}) or {}
    summaries: list[FeatureSummary] = []
    for slug, item in sorted(features.items()):
        summaries.append(
            FeatureSummary(
                slug=slug,
                title=item.get("title", slug),
                discovery_state=item.get("discovery_state", "unknown"),
                delivery_state=item.get("delivery_state", "unknown"),
                release_state=item.get("release_state", "unknown"),
                governance_state=item.get("governance_state", "unknown"),
                next_recommended_step=item.get("next_recommended_step", ""),
                risk_summary={},
            )
        )
    return summaries


def build_validation_summary(project_slug: str, artifacts: list[ArtifactSummary], workflow: dict[str, Any]) -> ValidationSummary:
    missing = [artifact.key for artifact in artifacts if not artifact.exists]
    gates = workflow.get("gates", {}) if workflow else {}
    traceability_warnings = []
    sst_warnings: list[str] = []
    if not any(item.kind == "solution-discovery" and item.exists for item in artifacts):
        traceability_warnings.append("solution-discovery ausente no projeto")

    for artifact in artifacts:
        if not artifact.exists:
            continue
        path = Path(artifact.path)
        text = load_text(path)
        if artifact.kind != "user-stories" and all(token in text for token in ["Given", "When", "Then"]):
            sst_warnings.append(f"Possível Given/When/Then fora de user-stories em {artifact.key}")
        if artifact.kind != "tech-spec" and any(line.strip().startswith("NFR-") for line in text.splitlines()):
            sst_warnings.append(f"Possível definição de NFR fora de tech-spec em {artifact.key}")
        if artifact.kind != "database-spec" and "CREATE TABLE" in text:
            sst_warnings.append(f"Possível DDL fora de database-spec em {artifact.key}")

    return ValidationSummary(
        gate_status=gates,
        missing_artifacts=missing,
        traceability_warnings=traceability_warnings,
        sst_warnings=sst_warnings,
    )


def build_project_summary(project_slug: str) -> ProjectSummary:
    status = load_project_status(project_slug)
    workflow = load_workflow_state(project_slug)
    features = build_feature_summaries(project_slug)
    artifacts = build_project_artifacts(project_slug)
    validation = build_validation_summary(project_slug, artifacts, workflow)
    gate_summary = build_gate_summary(workflow)
    return ProjectSummary(
        slug=project_slug,
        mode=status.get("mode", "unknown"),
        current_phase=status.get("current_phase", "unknown"),
        next_step=status.get("next_step", ""),
        gate_summary=gate_summary,
        feature_count=len(features),
        has_warnings=bool(validation.missing_artifacts or validation.traceability_warnings or validation.sst_warnings),
    )


def list_projects() -> list[ProjectSummary]:
    return [build_project_summary(slug) for slug in discover_project_slugs()]


def get_project_detail(project_slug: str) -> ProjectDetail:
    ensure_project_exists(project_slug)
    summary = build_project_summary(project_slug)
    status = load_project_status(project_slug)
    workflow = load_workflow_state(project_slug)
    artifacts = build_project_artifacts(project_slug)
    features = build_feature_summaries(project_slug)
    validation = build_validation_summary(project_slug, artifacts, workflow)
    return ProjectDetail(
        summary=summary,
        status=status,
        workflow=workflow,
        documents=artifacts,
        features=features,
        validation=validation,
    )


def get_feature_detail(project_slug: str, feature_slug: str) -> FeatureDetail:
    ensure_project_exists(project_slug)
    frontmatter, _body = load_feature_status(project_slug, feature_slug)
    feature_dir = project_dir(project_slug) / "features" / feature_slug
    if not feature_dir.is_dir():
        raise FileNotFoundError(f"Feature '{feature_slug}' nao encontrada no projeto '{project_slug}'.")
    summaries: list[ArtifactSummary] = []
    for kind, rel in FEATURE_ARTIFACTS:
        path = feature_dir / rel
        summaries.append(
            ArtifactSummary(
                key=f"features/{feature_slug}/{rel}",
                path=str(path),
                kind=kind,
                phase="feature",
                exists=path.exists(),
                status=file_status(path),
                updated_at=iso_mtime(path),
            )
        )

    summary = FeatureSummary(
        slug=feature_slug,
        title=frontmatter.get("title", feature_slug),
        discovery_state=frontmatter.get("discovery_state", "unknown"),
        delivery_state=frontmatter.get("delivery_state", "unknown"),
        release_state=frontmatter.get("release_state", "unknown"),
        governance_state=frontmatter.get("governance_state", "unknown"),
        next_recommended_step=frontmatter.get("next_recommended_step", ""),
        risk_summary=frontmatter.get("risk_state", {}) or {},
    )

    return FeatureDetail(
        summary=summary,
        frontmatter=frontmatter,
        linked_docs=frontmatter.get("linked_docs", {}) or {},
        traceability=frontmatter.get("traceability", {}) or {},
        artifact_summaries=summaries,
    )


def list_project_artifacts(project_slug: str) -> list[ArtifactSummary]:
    ensure_project_exists(project_slug)
    artifacts = build_project_artifacts(project_slug)
    feature_index = load_feature_index(project_slug)
    for feature_slug in sorted((feature_index.get("features", {}) or {}).keys()):
        feature_dir = project_dir(project_slug) / "features" / feature_slug
        for kind, rel in FEATURE_ARTIFACTS:
            path = feature_dir / rel
            artifacts.append(
                ArtifactSummary(
                    key=f"features/{feature_slug}/{rel}",
                    path=str(path),
                    kind=kind,
                    phase="feature",
                    exists=path.exists(),
                    status=file_status(path),
                    updated_at=iso_mtime(path),
                )
            )
    return artifacts


def resolve_artifact_path(project_slug: str, artifact_key: str) -> Path:
    base = ensure_project_exists(project_slug).resolve()
    rel_path = Path(artifact_key)
    candidate = (base / rel_path).resolve()
    if not str(candidate).startswith(str(base)):
        raise FileNotFoundError("Artifact key invalido.")
    if not candidate.exists():
        raise FileNotFoundError(f"Artefato '{artifact_key}' nao encontrado.")
    return candidate


def get_artifact_detail(project_slug: str, artifact_key: str) -> ArtifactDetail:
    path = resolve_artifact_path(project_slug, artifact_key)
    rel_path = path.relative_to(project_dir(project_slug))
    content = load_text(path)
    frontmatter: dict[str, Any] | None = None
    if path.suffix == ".md" and content.startswith("---"):
        frontmatter, body = read_frontmatter_markdown(path)
        content = body

    summary = ArtifactSummary(
        key=artifact_key,
        path=str(path),
        kind=path.stem,
        phase=rel_path.parts[0] if rel_path.parts else "unknown",
        exists=path.exists(),
        status=file_status(path),
        updated_at=iso_mtime(path),
    )

    return ArtifactDetail(
        summary=summary,
        frontmatter=frontmatter,
        content=content,
        excerpt=excerpt(content),
        content_type=path.suffix.lstrip("."),
    )


def get_validation(project_slug: str) -> ValidationSummary:
    ensure_project_exists(project_slug)
    artifacts = build_project_artifacts(project_slug)
    workflow = load_workflow_state(project_slug)
    return build_validation_summary(project_slug, artifacts, workflow)


def get_memory(project_slug: str) -> MemoryResponse:
    ensure_project_exists(project_slug)
    documents: list[MemoryDocument] = []
    if MEMORY_ROOT.exists():
        for path in sorted(MEMORY_ROOT.glob("*.md")):
            documents.append(MemoryDocument(name=path.name, path=str(path), content=load_text(path)))
    return MemoryResponse(documents=documents)
