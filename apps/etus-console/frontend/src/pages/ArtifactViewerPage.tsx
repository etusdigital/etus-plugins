import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";
import { ArtifactViewer } from "../components/ArtifactViewer";
import { ErrorState } from "../components/ErrorState";
import { Spinner } from "../components/Spinner";

export function ArtifactViewerPage() {
  const params = useParams();
  const projectSlug = params.projectSlug ?? "";
  const artifactKey = params["*"] ?? "";

  const artifactQuery = useQuery({
    queryKey: ["artifact", projectSlug, artifactKey],
    queryFn: () => api.artifact(projectSlug, artifactKey),
    enabled: Boolean(projectSlug && artifactKey),
  });

  if (artifactQuery.isLoading) {
    return <Spinner label="Carregando artefato..." />;
  }

  if (artifactQuery.isError) {
    return <ErrorState message={(artifactQuery.error as Error).message} />;
  }

  return <ArtifactViewer artifact={artifactQuery.data!} />;
}

