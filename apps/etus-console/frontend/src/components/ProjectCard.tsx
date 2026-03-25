import { Link } from "react-router-dom";

import type { ProjectSummary } from "../lib/types";
import { StatusBadge } from "./StatusBadge";

type ProjectCardProps = {
  project: ProjectSummary;
};

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <Link
      to={`/projects/${project.slug}`}
      className="card-surface block p-5 transition hover:-translate-y-0.5 hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-stone-500">{project.mode}</p>
          <h2 className="mt-2 text-lg font-semibold text-stone-900">{project.slug}</h2>
          <p className="mt-2 text-sm text-stone-600">Fase atual: {project.current_phase}</p>
        </div>
        <StatusBadge value={project.has_warnings ? "iterate" : "go"} />
      </div>
      <div className="mt-4 space-y-2 text-sm text-stone-700">
        <p>Proximo passo: {project.next_step || "—"}</p>
        <p>Features: {project.feature_count}</p>
        <p>Ultimo gate: {project.gate_summary.last_gate ?? "nenhum"}</p>
      </div>
    </Link>
  );
}

