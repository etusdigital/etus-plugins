type ErrorStateProps = {
  message: string;
};

export function ErrorState({ message }: ErrorStateProps) {
  return (
    <div className="card-surface border-rose-200 bg-rose-50 p-6">
      <h2 className="text-base font-semibold text-rose-800">Nao foi possivel carregar o painel</h2>
      <p className="mt-2 text-sm text-rose-700">{message}</p>
    </div>
  );
}

