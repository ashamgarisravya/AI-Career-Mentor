"use client";

import { Award, BookOpenCheck, Gauge, Target } from "lucide-react";
import { CareerCard } from "@/components/CareerCard";
import { Sidebar } from "@/components/Sidebar";
import { SkillGapCard } from "@/components/SkillGapCard";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

export default function DashboardPage() {
  const { careers, skillGaps, roadmap, loading, error } = useCareerBuilder();

  const stats = [
    { label: "Top match", value: `${careers[0]?.matchScore ?? 0}%`, icon: Award },
    { label: "ATS score", value: "78%", icon: Gauge },
    { label: "Skill gaps", value: skillGaps.length.toString(), icon: Target },
    { label: "Roadmap months", value: roadmap.length.toString(), icon: BookOpenCheck }
  ];

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Dashboard</h1>
          <p className="text-muted-foreground">Your career readiness snapshot and next best moves.</p>
        </div>
        {loading ? <LoadingSpinner label="Loading dashboard" /> : null}
        {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <Card key={stat.label}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
                  <Icon className="h-4 w-4 text-primary" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                </CardContent>
              </Card>
            );
          })}
        </div>
        <section className="grid gap-4 lg:grid-cols-3">
          {careers.map((career) => <CareerCard key={career.id} career={career} />)}
        </section>
        <section className="grid gap-4 lg:grid-cols-3">
          {skillGaps.map((gap) => <SkillGapCard key={gap.id} gap={gap} />)}
        </section>
      </main>
    </div>
  );
}
