"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { CareerCard } from "@/components/CareerCard";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Sidebar } from "@/components/Sidebar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";

const careerFormSchema = z.object({
  currentRole: z.string().min(2, "Current role is required"),
  experienceLevel: z.string().min(2, "Experience level is required"),
  targetRole: z.string().min(2, "Target role is required"),
  skills: z.string().min(3, "Add at least one skill"),
  interests: z.string().min(3, "Add at least one interest")
});

type CareerFormValues = z.infer<typeof careerFormSchema>;

export default function CareersPage() {
  const { careers, loading, error, discoverCareers } = useCareerBuilder();
  const form = useForm<CareerFormValues>({
    resolver: zodResolver(careerFormSchema),
    defaultValues: {
      currentRole: "Computer Science Student",
      experienceLevel: "Entry level",
      targetRole: "Machine Learning Engineer",
      skills: "Python, SQL, React",
      interests: "AI products, data, automation"
    }
  });

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Career Discovery</h1>
          <p className="text-muted-foreground">Generate career recommendations from your profile.</p>
        </div>
        <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
          <Card>
            <CardHeader>
              <CardTitle>User profile</CardTitle>
            </CardHeader>
            <CardContent>
              <form
                className="space-y-4"
                onSubmit={form.handleSubmit((values) =>
                  discoverCareers({
                    ...values,
                    skills: values.skills.split(",").map((skill) => skill.trim()),
                    interests: values.interests.split(",").map((interest) => interest.trim())
                  })
                )}
              >
                {(["currentRole", "experienceLevel", "targetRole"] as const).map((field) => (
                  <div key={field} className="space-y-2">
                    <Label htmlFor={field}>{field.replace(/([A-Z])/g, " $1")}</Label>
                    <Input id={field} {...form.register(field)} />
                    <p className="text-xs text-destructive">{form.formState.errors[field]?.message}</p>
                  </div>
                ))}
                <div className="space-y-2">
                  <Label htmlFor="skills">Skills</Label>
                  <Textarea id="skills" {...form.register("skills")} />
                  <p className="text-xs text-destructive">{form.formState.errors.skills?.message}</p>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="interests">Interests</Label>
                  <Textarea id="interests" {...form.register("interests")} />
                  <p className="text-xs text-destructive">{form.formState.errors.interests?.message}</p>
                </div>
                <Button className="w-full" disabled={loading}>Generate Recommendations</Button>
              </form>
            </CardContent>
          </Card>
          <section className="space-y-4">
            {loading ? <LoadingSpinner label="Generating recommendations" /> : null}
            {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
            <div className="grid gap-4 xl:grid-cols-2">
              {careers.map((career) => <CareerCard key={career.id} career={career} />)}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
