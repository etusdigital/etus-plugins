import { StatusBadge } from "./StatusBadge";

type GateBadgeProps = {
  label: string;
  value: string;
};

export function GateBadge({ label, value }: GateBadgeProps) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-xl border border-stone-200 bg-stone-50 px-3 py-2">
      <span className="text-sm text-stone-700">{label}</span>
      <StatusBadge value={value} />
    </div>
  );
}

