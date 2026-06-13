export type SkillPriority = "High" | "Medium" | "Low";

export interface CareerRecommendation {
  id: string;
  title: string;
  matchScore: number;
  salaryRange: string;
  growth: string;
  description: string;
  skills: string[];
}

export interface SkillGap {
  id: string;
  skill: string;
  priority: SkillPriority;
  currentLevel: number;
  targetLevel: number;
  resources: string[];
}

export interface RoadmapMonth {
  month: string;
  title: string;
  goals: string[];
  resources: LearningResource[];
}

export interface LearningResource {
  title: string;
  type: "Course" | "Project" | "Article" | "Practice";
  duration: string;
  url?: string;
}

export interface ResumeAnalysis {
  atsScore: number;
  strengths: string[];
  missingSkills: SkillGap[];
  summary: string;
}

export interface UserProfile {
  name: string;
  email: string;
  currentRole: string;
  experienceLevel: string;
  targetRole: string;
  location: string;
  skills: string[];
  interests: string[];
}
