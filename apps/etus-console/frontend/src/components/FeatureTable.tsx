import { Link, useParams } from "react-router-dom";

import type { FeatureSummary } from "../lib/types";
import { StatusBadge } from "./StatusBadge";

type FeatureTableProps = {
  features: FeatureSummary[];
};

export function FeatureTable({ features }: FeatureTableProps) {
  const { projectSlug } = useParams();

  return (
    <div className="card-surface overflow-hidden">
      <table className="min-w-full divide-y divide-stone-200 text-sm">
        <thead className="bg-stone-50">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-stone-600">Feature</th>
            <th className="px-4 py-3 text-left font-medium text-stone-600">Discovery</th>
            <th className="px-4 py-3 text-left font-medium text-stone-600">Delivery</th>
            <th className="px-4 py-3 text-left font-medium text-stone-600">Próximo passo</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-stone-100 bg-white">
          {features.map((feature) => (
            <tr key={feature.slug}>
              <td className="px-4 py-3">
                <Link className="font-medium text-stone-900 hover:text-sky-700" to={`/projects/${projectSlug}/features/${feature.slug}`}>
                  {feature.title}
                </Link>
              </td>
              <td className="px-4 py-3">
                <StatusBadge value={feature.discovery_state} />
              </td>
              <td className="px-4 py-3">
                <StatusBadge value={feature.delivery_state} />
              </td>
              <td className="px-4 py-3 text-stone-700">{feature.next_recommended_step || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

