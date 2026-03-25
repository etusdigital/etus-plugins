type StatusBadgeProps = {
  value: string;
};

const toneByValue: Record<string, string> = {
  complete: "bg-emerald-100 text-emerald-700",
  completed: "bg-emerald-100 text-emerald-700",
  draft: "bg-amber-100 text-amber-800",
  missing: "bg-rose-100 text-rose-700",
  pending: "bg-stone-200 text-stone-700",
  iterate: "bg-orange-100 text-orange-700",
  no_go: "bg-rose-100 text-rose-700",
  go: "bg-emerald-100 text-emerald-700",
};

export function StatusBadge({ value }: StatusBadgeProps) {
  const tone = toneByValue[value] ?? "bg-sky-100 text-sky-700";
  return <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${tone}`}>{value}</span>;
}

