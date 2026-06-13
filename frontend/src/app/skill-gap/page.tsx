"use client";

import { Sidebar } from "@/components/Sidebar";
import { SkillGapCard } from "@/components/SkillGapCard";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

const currentSkills = ["Python", "SQL", "React", "APIs", "Git", "Data cleaning"];

export default function SkillGapPage() {
  const { skillGaps, loading, error } = useCareerBuilder();

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Skill Gap Analysis</h1>
          <p className="text-muted-foreground">Compare current skills against your target AI career path.</p>
        </div>
        {loading ? <LoadingSpinner label="Loading skill gaps" /> : null}
        {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
        <Card>
          <CardHeader>
            <CardTitle>Current skills</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            {currentSkills.map((skill) => (
              <span key={skill} className="rounded-md bg-secondary px-3 py-1 text-sm">{skill}</span>
            ))}
          </CardContent>
        </Card>
        <div className="grid gap-4 lg:grid-cols-3">
          {skillGaps.map((gap) => <SkillGapCard key={gap.id} gap={gap} />)}
        </div>
      </main>
    </div>
  );
}
