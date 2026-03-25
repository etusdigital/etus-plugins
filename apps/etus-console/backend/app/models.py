from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GateSummary(BaseModel):
    gates: dict[str, str] = Field(default_factory=dict)
    last_gate: str | None = None


class ArtifactSummary(BaseModel):
    key: str
    path: str
    kind: str
    phase: str
    exists: bool
    status: str
    updated_at: str | None = None


class FeatureSummary(BaseModel):
    slug: str
    title: str
    discovery_state: str
    delivery_state: str
    release_state: str
    governance_state: str
    next_recommended_step: str
    risk_summary: dict[str, str] = Field(default_factory=dict)


class ValidationSummary(BaseModel):
    gate_status: dict[str, str] = Field(default_factory=dict)
    missing_artifacts: list[str] = Field(default_factory=list)
    traceability_warnings: list[str] = Field(default_factory=list)
    sst_warnings: list[str] = Field(default_factory=list)


class ProjectSummary(BaseModel):
    slug: str
    mode: str
    current_phase: str
    next_step: str
    gate_summary: GateSummary
    feature_count: int
    has_warnings: bool


class ProjectDetail(BaseModel):
    summary: ProjectSummary
    status: dict[str, Any]
    workflow: dict[str, Any]
    documents: list[ArtifactSummary]
    features: list[FeatureSummary]
    validation: ValidationSummary


class FeatureDetail(BaseModel):
    summary: FeatureSummary
    frontmatter: dict[str, Any]
    linked_docs: dict[str, str] = Field(default_factory=dict)
    traceability: dict[str, list[str]] = Field(default_factory=dict)
    artifact_summaries: list[ArtifactSummary] = Field(default_factory=list)


class ArtifactDetail(BaseModel):
    summary: ArtifactSummary
    frontmatter: dict[str, Any] | None = None
    content: str
    excerpt: str
    content_type: str


class MemoryDocument(BaseModel):
    name: str
    path: str
    content: str


class MemoryResponse(BaseModel):
    documents: list[MemoryDocument] = Field(default_factory=list)

