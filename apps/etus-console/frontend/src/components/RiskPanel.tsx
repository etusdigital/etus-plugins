type RiskPanelProps = {
  risks: Record<string, string>;
};

export function RiskPanel({ risks }: RiskPanelProps) {
  const entries = Object.entries(risks);

  return (
    <div className="card-surface p-4">
      <h3 className="text-sm font-semibold text-stone-900">Riscos</h3>
      {entries.length === 0 ? (
        <p className="mt-3 text-sm text-stone-600">Nenhum risco estruturado encontrado.</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {entries.map(([key, value]) => (
            <li key={key} className="flex items-center justify-between rounded-xl bg-stone-50 px-3 py-2">
              <span className="text-sm text-stone-700">{key}</span>
              <span className="text-sm font-medium text-stone-900">{value}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

