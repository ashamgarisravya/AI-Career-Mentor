"use client";

import { ResumeUploader } from "@/components/ResumeUploader";
import { Sidebar } from "@/components/Sidebar";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

export default function ResumePage() {
  const { resumeAnalysis, loading, error, runResumeAnalysis } = useCareerBuilder();

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Resume Analysis</h1>
          <p className="text-muted-foreground">Upload a PDF or paste resume text to get ATS score, strengths, missing skills, and revision guidance.</p>
        </div>
        <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
          <ResumeUploader onAnalyze={runResumeAnalysis} loading={loading} />
          <section className="space-y-4">
            {loading ? <LoadingSpinner label="Analyzing resume" /> : null}
            {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
            {resumeAnalysis ? (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>ATS score</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="text-4xl font-bold">{resumeAnalysis.atsScore}%</div>
                    <Progress value={resumeAnalysis.atsScore} />
                    <p className="text-sm text-muted-foreground">{resumeAnalysis.summary}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Strengths</CardTitle>
                  </CardHeader>
                  <CardContent className="flex flex-wrap gap-2">
                    {resumeAnalysis.strengths.map((strength) => (
                      <span key={strength} className="rounded-md bg-primary/10 px-3 py-1 text-sm text-primary">
                        {strength}
                      </span>
                    ))}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Missing skills</CardTitle>
                  </CardHeader>
                  <CardContent className="flex flex-wrap gap-2">
                    {resumeAnalysis.missingSkills.map((skill) => (
                      <span key={skill} className="rounded-md bg-secondary px-3 py-1 text-sm">{skill}</span>
                    ))}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Suggestions</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2 text-sm text-muted-foreground">
                    {resumeAnalysis.suggestions.map((suggestion) => <p key={suggestion}>{suggestion}</p>)}
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card>
                <CardContent className="p-6 text-sm text-muted-foreground">Run an analysis to see ATS score and personalized resume suggestions.</CardContent>
              </Card>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
