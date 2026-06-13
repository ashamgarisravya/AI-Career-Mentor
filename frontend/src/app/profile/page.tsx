"use client";

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

const profileSchema = z.object({
  name: z.string().min(2, "Name is required"),
  email: z.string().email("Use a valid email"),
  currentRole: z.string().min(2, "Current role is required"),
  targetRole: z.string().min(2, "Target role is required"),
  location: z.string().min(2, "Location is required"),
  skills: z.string().min(3, "Skills are required")
});

type ProfileValues = z.infer<typeof profileSchema>;

export default function ProfilePage() {
  const form = useForm<ProfileValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: "Sravya",
      email: "sravya@example.com",
      currentRole: "Student Developer",
      targetRole: "Machine Learning Engineer",
      location: "Hyderabad, India",
      skills: "Python, SQL, React, APIs"
    }
  });

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      <Sidebar />
      <main className="page-shell space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-normal">Profile</h1>
          <p className="text-muted-foreground">Manage the profile used by career recommendations.</p>
        </div>
        <Card className="max-w-2xl">
          <CardHeader>
            <CardTitle>User profile management</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={form.handleSubmit(() => undefined)}>
              {(["name", "email", "currentRole", "targetRole", "location"] as const).map((field) => (
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
              <Button>
                <Save className="h-4 w-4" />
                Save Profile
              </Button>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
