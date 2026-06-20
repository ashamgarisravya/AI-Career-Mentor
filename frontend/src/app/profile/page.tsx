"use client";

import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { Save } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Sidebar } from "@/components/Sidebar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useCareerBuilder } from "@/hooks/useCareerBuilder";
import type { UserProfile } from "@/types/career";

const profileSchema = z.object({
  name: z.string().min(2, "Name is required"),
  education: z.string().min(2, "Education is required"),
  degree: z.string().min(2, "Degree is required"),
  branch: z.string().min(2, "Branch is required"),
  experienceLevel: z.string().min(2, "Experience level is required"),
  currentSkills: z.string().min(2, "Add at least one skill"),
  interests: z.string().min(2, "Add at least one interest"),
  preferredRoles: z.string().min(2, "Add at least one preferred role")
});

type ProfileValues = z.infer<typeof profileSchema>;

function splitList(value: string) {
  return value.split(",").map((item) => item.trim()).filter(Boolean);
}

export default function ProfilePage() {
  const { profile, profileAnalysis, loading, error, loadProfile, saveUserProfile } = useCareerBuilder();
  const form = useForm<ProfileValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: "",
      education: "",
      degree: "",
      branch: "",
      experienceLevel: "",
      currentSkills: "",
      interests: "",
      preferredRoles: ""
    }
  });

  useEffect(() => {
    void loadProfile();
  }, [loadProfile]);

  useEffect(() => {
    if (!profile) return;
    form.reset({
      name: profile.name,
      education: profile.education,
      degree: profile.degree,
      branch: profile.branch,
      experienceLevel: profile.experienceLevel,
      currentSkills: profile.currentSkills.join(", "),
      interests: profile.interests.join(", "),
      preferredRoles: profile.preferredRoles.join(", ")
    });
  }, [profile, form]);

  async function onSubmit(values: ProfileValues) {
    const payload: UserProfile = {
      name: values.name,
      education: values.education,
      degree: values.degree,
      branch: values.branch,
      experienceLevel: values.experienceLevel,
      currentSkills: splitList(values.currentSkills),
      interests: splitList(values.interests),
      preferredRoles: splitList(values.preferredRoles)
    };
    await saveUserProfile(payload);
  }

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Profile</h1>
          <p className="text-muted-foreground">Create the profile your AI mentor will use for coaching, recommendations, and roadmap planning.</p>
        </div>
        {error ? <p className="rounded-md border border-destructive/30 bg-destructive/10 p-3 text-sm text-destructive">{error}</p> : null}
        <div className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
          <Card>
            <CardHeader>
              <CardTitle>User profile management</CardTitle>
            </CardHeader>
            <CardContent>
              <form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
                {(["name", "education", "degree", "branch", "experienceLevel"] as const).map((field) => (
                  <div key={field} className="space-y-2">
                    <Label htmlFor={field}>{field.replace(/([A-Z])/g, " $1")}</Label>
                    <Input id={field} {...form.register(field)} />
                    <p className="text-xs text-destructive">{form.formState.errors[field]?.message}</p>
                  </div>
                ))}
                {(["currentSkills", "interests", "preferredRoles"] as const).map((field) => (
                  <div key={field} className="space-y-2">
                    <Label htmlFor={field}>{field}</Label>
                    <Textarea id={field} {...form.register(field)} />
                    <p className="text-xs text-destructive">{form.formState.errors[field]?.message}</p>
                  </div>
                ))}
                <Button disabled={loading}>
                  <Save className="h-4 w-4" />
                  Save Profile
                </Button>
              </form>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Mentor summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <div className="rounded-md bg-muted p-4">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">Readiness score</p>
                <p className="mt-2 text-3xl font-semibold">{profileAnalysis?.readinessScore ?? 0}%</p>
              </div>
              <p className="text-muted-foreground">{profileAnalysis?.mentorSummary ?? "Save your profile to receive a personalized mentor summary."}</p>
              <div>
                <p className="mb-2 font-medium">Strengths</p>
                <div className="flex flex-wrap gap-2">
                  {(profileAnalysis?.strengths ?? []).map((item) => (
                    <span key={item} className="rounded-md bg-primary/10 px-3 py-1 text-xs text-primary">{item}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="mb-2 font-medium">Weaknesses</p>
                <div className="space-y-2 text-muted-foreground">
                  {(profileAnalysis?.weaknesses ?? []).map((item) => <p key={item}>{item}</p>)}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
