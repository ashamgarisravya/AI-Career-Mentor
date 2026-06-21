"use client";

import { useEffect } from "react";
import { MessageSquareText } from "lucide-react";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Sidebar } from "@/components/Sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

export default function InterviewPage() {
  const { interviewPreparation, loading, error, loadInterviewPreparation } = useCareerBuilder();

  useEffect(() => {
    void loadInterviewPreparation();
  }, [loadInterviewPreparation]);

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Interview Preparation</h1>
          <p className="text-muted-foreground">Role-specific practice questions, answer tips, and a focused plan based on your profile.</p>
        </div>
        {loading ? <LoadingSpinner label="Loading interview preparation" /> : null}
        {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
        <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)]">
          <Card>
            <CardHeader>
              <CardTitle>Practice Plan</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-md bg-muted p-4">
                <p className="text-sm text-muted-foreground">Target role</p>
                <p className="text-xl font-semibold">{interviewPreparation?.targetRole ?? "Not set"}</p>
              </div>
              <div className="rounded-md bg-muted p-4">
                <p className="text-sm text-muted-foreground">Readiness</p>
                <p className="text-xl font-semibold">{interviewPreparation?.readinessScore ?? 0}%</p>
              </div>
              <div className="space-y-2 text-sm text-muted-foreground">
                {(interviewPreparation?.practicePlan ?? []).map((item) => <p key={item}>{item}</p>)}
              </div>
            </CardContent>
          </Card>
          <div className="space-y-4">
            {(interviewPreparation?.questions ?? []).map((item) => (
              <Card key={item.question}>
                <CardHeader>
                  <div className="flex items-center gap-3">
                    <MessageSquareText className="h-5 w-5 text-primary" />
                    <div>
                      <CardTitle className="text-lg">{item.focusArea}</CardTitle>
                      <p className="text-sm text-muted-foreground">{item.question}</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-2 text-sm text-muted-foreground">
                  {item.answerTips.map((tip) => <p key={tip}>{tip}</p>)}
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
        <Card>
          <CardHeader>
            <CardTitle>Interview Tips</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-2 text-sm text-muted-foreground md:grid-cols-3">
            {(interviewPreparation?.tips ?? []).map((tip) => <p key={tip}>{tip}</p>)}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
