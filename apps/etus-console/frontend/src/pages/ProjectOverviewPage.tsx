import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";
import { ArtifactList } from "../components/ArtifactList";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { FeatureTable } from "../components/FeatureTable";
import { Spinner } from "../components/Spinner";
import { ValidationPanel } from "../components/ValidationPanel";

export function ProjectOverviewPage() {
  const { projectSlug = "" } = useParams();
  const projectQuery = useQuery({
    queryKey: ["project", projectSlug],
    queryFn: () => api.project(projectSlug),
    enabled: Boolean(projectSlug),
  });

  if (projectQuery.isLoading) {
    return <Spinner label="Carregando projeto..." />;
  }

  if (projectQuery.isError) {
    return <ErrorState message={(projectQuery.error as Error).message} />;
  }

  const project = projectQuery.data;
  if (!project) {
    return <EmptyState title="Projeto não encontrado" description="Verifique o slug do projeto e o conteúdo em docs/ets/projects/." />;
  }

  return (
    <div className="space-y-6">
      <section className="card-surface p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-stone-500">{project.summary.mode}</p>
            <h2 className="mt-1 text-2xl font-semibold text-stone-950">{project.summary.slug}</h2>
            <p className="mt-2 text-sm text-stone-600">Fase atual: {project.summary.current_phase}</p>
            <p className="mt-1 text-sm text-stone-600">Próximo passo: {project.summary.next_step || "—"}</p>
          </div>
          <Link
            to={`/projects/${projectSlug}/validation`}
            className="rounded-xl bg-stone-900 px-4 py-2 text-sm font-medium text-white hover:bg-stone-800"
          >
            Ver validação
          </Link>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.2fr,0.8fr]">
        <div className="space-y-6">
          <FeatureTable features={project.features} />
          <ArtifactList artifacts={project.documents} />
        </div>
        <ValidationPanel validation={project.validation} />
      </section>
    </div>
  );
}

