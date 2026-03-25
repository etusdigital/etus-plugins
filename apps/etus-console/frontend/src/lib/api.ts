import type {
  ArtifactDetail,
  ArtifactSummary,
  FeatureDetail,
  FeatureSummary,
  MemoryResponse,
  ProjectDetail,
  ProjectSummary,
  ValidationSummary,
} from "./types";

const API_BASE = (import.meta.env.VITE_ETUS_API_BASE as string | undefined) ?? "http://127.0.0.1:8787/api";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Erro ao carregar ${path}: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => fetchJson<{ status: string; version: string; docs_root: string }>("/health"),
  projects: () => fetchJson<ProjectSummary[]>("/projects"),
  project: (projectSlug: string) => fetchJson<ProjectDetail>(`/projects/${projectSlug}`),
  features: (projectSlug: string) => fetchJson<FeatureSummary[]>(`/projects/${projectSlug}/features`),
  feature: (projectSlug: string, featureSlug: string) =>
    fetchJson<FeatureDetail>(`/projects/${projectSlug}/features/${featureSlug}`),
  artifacts: (projectSlug: string) => fetchJson<ArtifactSummary[]>(`/projects/${projectSlug}/artifacts`),
  artifact: (projectSlug: string, artifactKey: string) =>
    fetchJson<ArtifactDetail>(`/projects/${projectSlug}/artifacts/${encodeURIComponent(artifactKey).replace(/%2F/g, "/")}`),
  validation: (projectSlug: string) => fetchJson<ValidationSummary>(`/projects/${projectSlug}/validation`),
  memory: (projectSlug: string) => fetchJson<MemoryResponse>(`/projects/${projectSlug}/memory`),
};
