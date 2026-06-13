import Link from "next/link";
import { ArrowRight, FileSearch, Map, Sparkles, Target } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const features = [
  { title: "Discover careers", description: "Match your skills, interests, and goals to high-fit career paths.", icon: Sparkles },
  { title: "Analyze resumes", description: "Review ATS score, missing keywords, and stronger evidence bullets.", icon: FileSearch },
  { title: "Close skill gaps", description: "Prioritize the skills that move you fastest toward your target role.", icon: Target },
  { title: "Build roadmaps", description: "Turn recommendations into monthly projects, courses, and practice.", icon: Map }
];

export default function HomePage() {
  return (
    <main>
      <section className="border-b">
        <div className="page-shell grid min-h-[calc(100vh-4rem)] items-center gap-10 py-12 md:grid-cols-[1.1fr_0.9fr]">
          <div>
            <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-primary">AI-powered career coach</p>
            <h1 className="max-w-3xl text-4xl font-bold tracking-normal sm:text-5xl lg:text-6xl">
              Build a career plan that knows where you are starting.
            </h1>
            <p className="mt-5 max-w-2xl text-lg text-muted-foreground">
              AI Career Builder helps students and job seekers discover roles, improve resumes, close skill gaps, and follow focused learning roadmaps.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg">
                <Link href="/dashboard">
                  Open Dashboard <ArrowRight className="h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="/careers">Find Careers</Link>
              </Button>
            </div>
          </div>
          <div className="rounded-lg border bg-card p-5 shadow-sm">
            <div className="grid gap-4">
              {["Career fit 94%", "ATS score 78%", "High priority skills 2", "Roadmap 3 months"].map((stat) => (
                <div key={stat} className="rounded-md bg-muted p-4 text-lg font-semibold">
                  {stat}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
      <section className="page-shell py-12">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Card key={feature.title}>
                <CardHeader>
                  <Icon className="h-6 w-6 text-primary" />
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>
    </main>
  );
}
