import { Outlet } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";
import { ErrorState } from "./ErrorState";
import { Sidebar } from "./Sidebar";

export function AppShell() {
  const projectsQuery = useQuery({
    queryKey: ["projects"],
    queryFn: api.projects,
    refetchInterval: 10000,
  });

  if (projectsQuery.isError) {
    return (
      <div className="min-h-screen p-6">
        <ErrorState message={(projectsQuery.error as Error).message} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-stone-100 text-stone-900 lg:flex">
      <Sidebar projects={projectsQuery.data ?? []} />
      <main className="min-h-screen flex-1">
        <div className="mx-auto max-w-7xl p-4 md:p-6">
          <div className="mb-6 flex items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Documentation Core</p>
              <h1 className="text-2xl font-semibold text-stone-950">ETUS Local Console</h1>
            </div>
          </div>
          <Outlet />
        </div>
      </main>
    </div>
  );
}

