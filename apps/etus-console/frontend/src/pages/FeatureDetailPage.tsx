import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";
import { ArtifactList } from "../components/ArtifactList";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { RiskPanel } from "../components/RiskPanel";
import { Spinner } from "../components/Spinner";
import { StatusBadge } from "../components/StatusBadge";

export function FeatureDetailPage() {
  const { projectSlug = "", featureSlug = "" } = useParams();
  const featureQuery = useQuery({
    queryKey: ["feature", projectSlug, featureSlug],
    queryFn: () => api.feature(projectSlug, featureSlug),
    enabled: Boolean(projectSlug && featureSlug),
  });

  if (featureQuery.isLoading) {
    return <Spinner label="Carregando feature..." />;
  }

  if (featureQuery.isError) {
    return <ErrorState message={(featureQuery.error as Error).message} />;
  }

  const feature = featureQuery.data;
  if (!feature) {
    return <EmptyState title="Feature não encontrada" description="Verifique o slug e o diretório em docs/ets/projects/{project}/features/." />;
  }

  return (
    <div className="space-y-6">
      <section className="card-surface p-5">
        <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Feature</p>
        <h2 className="mt-1 text-2xl font-semibold text-stone-950">{feature.summary.title}</h2>
        <div className="mt-4 flex flex-wrap gap-2">
          <StatusBadge value={feature.summary.discovery_state} />
          <StatusBadge value={feature.summary.delivery_state} />
          <StatusBadge value={feature.summary.release_state} />
          <StatusBadge value={feature.summary.governance_state} />
        </div>
        <p className="mt-4 text-sm text-stone-600">Próximo passo: {feature.summary.next_recommended_step || "—"}</p>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.9fr,1.1fr]">
        <RiskPanel risks={feature.summary.risk_summary} />
        <div className="card-surface p-4">
          <h3 className="text-sm font-semibold text-stone-900">Traceability</h3>
          <pre className="mt-3 whitespace-pre-wrap rounded-xl bg-stone-50 p-3 text-xs text-stone-700">
            {JSON.stringify(feature.traceability, null, 2)}
          </pre>
        </div>
      </section>

      <ArtifactList artifacts={feature.artifact_summaries} />
    </div>
  );
}

