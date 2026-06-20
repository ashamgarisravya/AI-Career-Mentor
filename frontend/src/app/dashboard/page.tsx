"use client";

import { Award, BookOpenCheck, Gauge, Target } from "lucide-react";
import { CareerCard } from "@/components/CareerCard";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { RoadmapTimeline } from "@/components/RoadmapTimeline";
import { Sidebar } from "@/components/Sidebar";
import { SkillGapCard } from "@/components/SkillGapCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

export default function DashboardPage() {
  const { dashboard, careers, skillGaps, roadmap, loading, error } = useCareerBuilder();

  const stats = [
    { label: "Career fit", value: `${dashboard?.careerFit ?? 0}%`, icon: Award },
    { label: "ATS score", value: `${dashboard?.atsScore ?? 0}%`, icon: Gauge },
    { label: "Skill gaps", value: skillGaps.length.toString(), icon: Target },
    { label: "Roadmap months", value: roadmap.length.toString(), icon: BookOpenCheck }
  ];

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Dashboard</h1>
          <p className="text-muted-foreground">Your complete career coaching snapshot across fit, resume readiness, skill gaps, roadmap, and mentor advice.</p>
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
        <section className="grid gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
          <Card>
            <CardHeader>
              <CardTitle>AI Mentor Advice</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">{dashboard?.mentorSummary ?? "Create your profile to start receiving mentor advice."}</p>
              <div>
                <p className="mb-2 text-sm font-medium">Strengths</p>
                <div className="flex flex-wrap gap-2">
                  {(dashboard?.strengths ?? []).map((item) => (
                    <span key={item} className="rounded-md bg-primary/10 px-3 py-1 text-xs text-primary">{item}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="mb-2 text-sm font-medium">Weaknesses</p>
                <div className="space-y-2 text-sm text-muted-foreground">
                  {(dashboard?.weaknesses ?? []).map((item) => <p key={item}>{item}</p>)}
                </div>
              </div>
              <div>
                <p className="mb-2 text-sm font-medium">Next steps</p>
                <div className="space-y-2 text-sm text-muted-foreground">
                  {(dashboard?.nextSteps ?? []).map((item) => <p key={item}>{item}</p>)}
                </div>
              </div>
              <div>
                <p className="mb-2 text-sm font-medium">Resume suggestions</p>
                <div className="space-y-2 text-sm text-muted-foreground">
                  {(dashboard?.resumeSuggestions ?? []).map((item) => <p key={item}>{item}</p>)}
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Top careers</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {careers.map((career) => (
                <div key={career.id} className="rounded-md bg-muted p-3">
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-medium">{career.title}</span>
                    <span className="text-sm text-primary">{career.matchScore}%</span>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground">{career.mentorFeedback}</p>
                </div>
              ))}
            </CardContent>
          </Card>
        </section>
        <section className="grid gap-4 lg:grid-cols-3">
          {careers.map((career) => <CareerCard key={career.id} career={career} />)}
        </section>
        <section className="grid gap-4 lg:grid-cols-3">
          {skillGaps.map((gap) => <SkillGapCard key={gap.id} gap={gap} />)}
        </section>
        <RoadmapTimeline roadmap={roadmap} />
      </main>
    </div>
  );
}
