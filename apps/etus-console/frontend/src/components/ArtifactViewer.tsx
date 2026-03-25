import type { ArtifactDetail } from "../lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { StatusBadge } from "./StatusBadge";

type ArtifactViewerProps = {
  artifact: ArtifactDetail;
};

export function ArtifactViewer({ artifact }: ArtifactViewerProps) {
  return (
    <div className="card-surface overflow-hidden">
      <div className="border-b border-stone-200 px-4 py-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold text-stone-900">{artifact.summary.kind}</h2>
            <p className="mt-1 text-xs text-stone-500">{artifact.summary.path}</p>
          </div>
          <StatusBadge value={artifact.summary.status} />
        </div>
      </div>
      {artifact.frontmatter ? (
        <div className="border-b border-stone-100 bg-stone-50 px-4 py-3">
          <h3 className="text-sm font-semibold text-stone-800">Frontmatter</h3>
          <pre className="mt-2 whitespace-pre-wrap text-xs text-stone-700">{JSON.stringify(artifact.frontmatter, null, 2)}</pre>
        </div>
      ) : null}
      <div className="prose-console px-4 py-4">
        {artifact.content_type === "md" ? (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{artifact.content}</ReactMarkdown>
        ) : (
          <pre className="whitespace-pre-wrap">{artifact.content}</pre>
        )}
      </div>
    </div>
  );
}
