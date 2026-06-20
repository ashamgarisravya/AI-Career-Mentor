"use client";

import { useEffect } from "react";
import { CareerCard } from "@/components/CareerCard";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Sidebar } from "@/components/Sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

export default function CareersPage() {
  const { careers, profile, loading, error, loadProfile, discoverCareers } = useCareerBuilder();

  useEffect(() => {
    void loadProfile();
  }, [loadProfile]);

  useEffect(() => {
    if (profile) {
      void discoverCareers(profile);
    }
  }, [discoverCareers, profile]);

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Career Discovery</h1>
          <p className="text-muted-foreground">Dynamic recommendations generated from your saved profile, projects, interests, and target role.</p>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Recommendation inputs</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 text-sm md:grid-cols-2 xl:grid-cols-4">
            <div>
              <p className="text-muted-foreground">Education</p>
              <p className="font-medium">{profile?.education || "Not set"}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Preferred roles</p>
              <p className="font-medium">{profile?.preferredRoles.join(", ") || "Not set"}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Skills</p>
              <p className="font-medium">{profile?.currentSkills.join(", ") || "Not set"}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Interests</p>
              <p className="font-medium">{profile?.interests.join(", ") || "Not set"}</p>
            </div>
          </CardContent>
        </Card>
        {loading ? <LoadingSpinner label="Generating recommendations" /> : null}
        {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
        <section className="grid gap-4 xl:grid-cols-2">
          {careers.map((career) => <CareerCard key={career.id} career={career} />)}
        </section>
      </main>
    </div>
  );
}
