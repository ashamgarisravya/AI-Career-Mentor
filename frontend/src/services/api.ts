import type {
  CareerRecommendation,
  DashboardSummary,
  InterviewPreparation,
  ProfileAnalysis,
  ResumeAnalysis,
  RoadmapMonth,
  SkillGap,
  UserProfile
} from "@/types/career";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options?.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(options?.headers ?? {})
    },
    cache: "no-store"
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function toBackendProfile(profile: Partial<UserProfile>) {
  return {
    name: profile.name ?? "",
    education: profile.education ?? "",
    degree: profile.degree ?? "",
    branch: profile.branch ?? "",
    experience_level: profile.experienceLevel ?? "",
    current_skills: profile.currentSkills ?? [],
    interests: profile.interests ?? [],
    preferred_roles: profile.preferredRoles ?? [],
    resume_text: profile.resumeText ?? ""
  };
}

function fromBackendProfile(data: Record<string, unknown>): UserProfile {
  return {
    name: String(data.name ?? ""),
    education: String(data.education ?? ""),
    degree: String(data.degree ?? ""),
    branch: String(data.branch ?? ""),
    experienceLevel: String(data.experience_level ?? ""),
    currentSkills: Array.isArray(data.current_skills) ? data.current_skills.map(String) : [],
    interests: Array.isArray(data.interests) ? data.interests.map(String) : [],
    preferredRoles: Array.isArray(data.preferred_roles) ? data.preferred_roles.map(String) : [],
    resumeText: String(data.resume_text ?? "")
  };
}

function fromBackendProfileAnalysis(data: Record<string, unknown>): ProfileAnalysis {
  return {
    readinessScore: Number(data.readiness_score ?? 0),
    strengths: Array.isArray(data.strengths) ? data.strengths.map(String) : [],
    weaknesses: Array.isArray(data.weaknesses) ? data.weaknesses.map(String) : [],
    mentorSummary: String(data.mentor_summary ?? "")
  };
}

export async function getProfile() {
  const data = await request<Record<string, unknown>>("/profile");
  return fromBackendProfile(data);
}

export async function saveProfile(profile: UserProfile) {
  const data = await request<Record<string, unknown>>("/profile", {
    method: "POST",
    body: JSON.stringify(toBackendProfile(profile))
  });
  return fromBackendProfileAnalysis(data);
}

export async function getCareerRecommendations(profile: Partial<UserProfile>) {
  return request<CareerRecommendation[]>("/careers/recommend", {
    method: "POST",
    body: JSON.stringify(toBackendProfile(profile))
  });
}

export async function analyzeResume(file?: File, resumeText?: string) {
  const formData = new FormData();
  if (file) formData.append("resume", file);
  if (resumeText) formData.append("resume_text", resumeText);
  return request<ResumeAnalysis>("/resume/analyze", {
    method: "POST",
    body: formData
  });
}

export async function getSkillGaps() {
  return request<SkillGap[]>("/skills/gaps");
}

export async function getRoadmap() {
  return request<RoadmapMonth[]>("/roadmap");
}

export async function getInterviewPreparation() {
  return request<InterviewPreparation>("/interview/prep");
}

export async function getDashboard() {
  return request<DashboardSummary>("/dashboard");
}
