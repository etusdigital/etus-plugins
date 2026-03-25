import { Link, useParams } from "react-router-dom";

import type { ArtifactSummary } from "../lib/types";
import { StatusBadge } from "./StatusBadge";

type ArtifactListProps = {
  artifacts: ArtifactSummary[];
};

export function ArtifactList({ artifacts }: ArtifactListProps) {
  const { projectSlug } = useParams();

  return (
    <div className="card-surface overflow-hidden">
      <div className="border-b border-stone-200 px-4 py-3">
        <h3 className="text-sm font-semibold text-stone-900">Artefatos</h3>
      </div>
      <ul className="divide-y divide-stone-100">
        {artifacts.map((artifact) => (
          <li key={artifact.key} className="flex items-center justify-between gap-3 px-4 py-3">
            <div className="min-w-0">
              <Link
                to={`/projects/${projectSlug}/artifacts/${artifact.key}`}
                className="truncate font-medium text-stone-900 hover:text-sky-700"
              >
                {artifact.kind}
              </Link>
              <p className="truncate text-xs text-stone-500">{artifact.path}</p>
            </div>
            <StatusBadge value={artifact.status} />
          </li>
        ))}
      </ul>
    </div>
  );
}

