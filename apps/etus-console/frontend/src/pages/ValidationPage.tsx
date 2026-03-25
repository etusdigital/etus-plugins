import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";
import { ErrorState } from "../components/ErrorState";
import { Spinner } from "../components/Spinner";
import { ValidationPanel } from "../components/ValidationPanel";

export function ValidationPage() {
  const { projectSlug = "" } = useParams();
  const validationQuery = useQuery({
    queryKey: ["validation", projectSlug],
    queryFn: () => api.validation(projectSlug),
    enabled: Boolean(projectSlug),
  });

  if (validationQuery.isLoading) {
    return <Spinner label="Carregando validação..." />;
  }

  if (validationQuery.isError) {
    return <ErrorState message={(validationQuery.error as Error).message} />;
  }

  return <ValidationPanel validation={validationQuery.data!} />;
}

