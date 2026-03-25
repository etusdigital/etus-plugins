import type { ValidationSummary } from "../lib/types";
import { GateBadge } from "./GateBadge";

type ValidationPanelProps = {
  validation: ValidationSummary;
};

export function ValidationPanel({ validation }: ValidationPanelProps) {
  return (
    <div className="card-surface p-4">
      <h3 className="text-sm font-semibold text-stone-900">Validação e Health</h3>
      <div className="mt-4 space-y-2">
        {Object.entries(validation.gate_status).map(([key, value]) => (
          <GateBadge key={key} label={key} value={value} />
        ))}
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">Artefatos faltando</h4>
          <ul className="mt-2 space-y-1 text-sm text-stone-700">
            {validation.missing_artifacts.length === 0 ? <li>Nenhum</li> : validation.missing_artifacts.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">Traceability</h4>
          <ul className="mt-2 space-y-1 text-sm text-stone-700">
            {validation.traceability_warnings.length === 0 ? <li>Nenhum warning</li> : validation.traceability_warnings.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">SST</h4>
          <ul className="mt-2 space-y-1 text-sm text-stone-700">
            {validation.sst_warnings.length === 0 ? <li>Nenhum warning</li> : validation.sst_warnings.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
}

