import { Link, useLocation } from "react-router-dom";

import type { ProjectSummary } from "../lib/types";

type SidebarProps = {
  projects: ProjectSummary[];
};

export function Sidebar({ projects }: SidebarProps) {
  const location = useLocation();

  return (
    <aside className="hidden w-72 border-r border-stone-200 bg-white lg:block">
      <div className="border-b border-stone-200 px-5 py-4">
        <p className="text-xs uppercase tracking-[0.18em] text-stone-500">ETUS Console</p>
        <h1 className="mt-1 text-lg font-semibold text-stone-900">Workspace</h1>
      </div>
      <nav className="p-3">
        <Link
          to="/"
          className={`mb-2 block rounded-xl px-3 py-2 text-sm ${location.pathname === "/" ? "bg-stone-900 text-white" : "text-stone-700 hover:bg-stone-100"}`}
        >
          Dashboard
        </Link>
        <div className="mt-4">
          <p className="px-3 text-xs uppercase tracking-[0.18em] text-stone-500">Projetos</p>
          <ul className="mt-2 space-y-1">
            {projects.map((project) => (
              <li key={project.slug}>
                <Link
                  to={`/projects/${project.slug}`}
                  className={`block rounded-xl px-3 py-2 text-sm ${
                    location.pathname.startsWith(`/projects/${project.slug}`)
                      ? "bg-stone-900 text-white"
                      : "text-stone-700 hover:bg-stone-100"
                  }`}
                >
                  {project.slug}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </nav>
    </aside>
  );
}

