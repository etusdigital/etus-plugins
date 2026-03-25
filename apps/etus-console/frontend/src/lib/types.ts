export type GateSummary = {
  gates: Record<string, string>;
  last_gate?: string | null;
};

export type ArtifactSummary = {
  key: string;
  path: string;
  kind: string;
  phase: string;
  exists: boolean;
  status: string;
  updated_at?: string | null;
};

export type FeatureSummary = {
  slug: string;
  title: string;
  discovery_state: string;
  delivery_state: string;
  release_state: string;
  governance_state: string;
  next_recommended_step: string;
  risk_summary: Record<string, string>;
};

export type ValidationSummary = {
  gate_status: Record<string, string>;
  missing_artifacts: string[];
  traceability_warnings: string[];
  sst_warnings: string[];
};

export type ProjectSummary = {
  slug: string;
  mode: string;
  current_phase: string;
  next_step: string;
  gate_summary: GateSummary;
  feature_count: number;
  has_warnings: boolean;
};

export type ProjectDetail = {
  summary: ProjectSummary;
  status: Record<string, unknown>;
  workflow: Record<string, unknown>;
  documents: ArtifactSummary[];
  features: FeatureSummary[];
  validation: ValidationSummary;
};

export type FeatureDetail = {
  summary: FeatureSummary;
  frontmatter: Record<string, unknown>;
  linked_docs: Record<string, string>;
  traceability: Record<string, string[]>;
  artifact_summaries: ArtifactSummary[];
};

export type ArtifactDetail = {
  summary: ArtifactSummary;
  frontmatter?: Record<string, unknown> | null;
  content: string;
  excerpt: string;
  content_type: string;
};

export type MemoryDocument = {
  name: string;
  path: string;
  content: string;
};

export type MemoryResponse = {
  documents: MemoryDocument[];
};

