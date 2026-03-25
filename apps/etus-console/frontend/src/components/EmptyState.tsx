type EmptyStateProps = {
  title: string;
  description: string;
};

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="card-surface p-8 text-center">
      <h2 className="text-lg font-semibold text-stone-900">{title}</h2>
      <p className="mt-2 text-sm text-stone-600">{description}</p>
    </div>
  );
}

