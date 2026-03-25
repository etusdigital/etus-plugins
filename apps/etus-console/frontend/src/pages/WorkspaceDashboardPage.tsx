import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { ProjectCard } from "../components/ProjectCard";
import { Spinner } from "../components/Spinner";

export function WorkspaceDashboardPage() {
  const projectsQuery = useQuery({
    queryKey: ["projects"],
    queryFn: api.projects,
    refetchInterval: 10000,
  });

  if (projectsQuery.isLoading) {
    return <Spinner label="Carregando projetos..." />;
  }

  if (projectsQuery.isError) {
    return <ErrorState message={(projectsQuery.error as Error).message} />;
  }

  const projects = projectsQuery.data ?? [];

  if (projects.length === 0) {
    return <EmptyState title="Nenhum projeto encontrado" description="Crie um projeto em docs/ets/projects/{project-slug}/ para aparecer aqui." />;
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {projects.map((project) => (
        <ProjectCard key={project.slug} project={project} />
      ))}
    </div>
  );
}

