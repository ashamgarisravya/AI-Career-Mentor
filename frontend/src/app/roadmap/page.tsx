"use client";

import { LoadingSpinner } from "@/components/LoadingSpinner";
import { RoadmapTimeline } from "@/components/RoadmapTimeline";
import { Sidebar } from "@/components/Sidebar";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

export default function RoadmapPage() {
  const { roadmap, loading, error } = useCareerBuilder();

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Learning Roadmap</h1>
          <p className="text-muted-foreground">A monthly path from current skills to interview-ready projects.</p>
        </div>
        {loading ? <LoadingSpinner label="Loading roadmap" /> : null}
        {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
        <RoadmapTimeline roadmap={roadmap} />
      </main>
    </div>
  );
}
