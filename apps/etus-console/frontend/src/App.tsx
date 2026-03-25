import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { AppShell } from "./components/AppShell";
import { ArtifactViewerPage } from "./pages/ArtifactViewerPage";
import { FeatureDetailPage } from "./pages/FeatureDetailPage";
import { ProjectOverviewPage } from "./pages/ProjectOverviewPage";
import { ValidationPage } from "./pages/ValidationPage";
import { WorkspaceDashboardPage } from "./pages/WorkspaceDashboardPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <WorkspaceDashboardPage /> },
      { path: "projects/:projectSlug", element: <ProjectOverviewPage /> },
      { path: "projects/:projectSlug/validation", element: <ValidationPage /> },
      { path: "projects/:projectSlug/features/:featureSlug", element: <FeatureDetailPage /> },
      { path: "projects/:projectSlug/artifacts/*", element: <ArtifactViewerPage /> },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}

