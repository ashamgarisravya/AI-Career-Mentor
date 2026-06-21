export type SkillPriority = "High" | "Medium" | "Low";

export interface UserProfile {
  name: string;
  education: string;
  degree: string;
  branch: string;
  experienceLevel: string;
  currentSkills: string[];
  interests: string[];
  preferredRoles: string[];
  resumeText?: string;
}

export interface ProfileAnalysis {
  readinessScore: number;
  strengths: string[];
  weaknesses: string[];
  mentorSummary: string;
}

export interface CareerRecommendation {
  id: string;
  title: string;
  matchScore: number;
  salaryRange: string;
  growthRate: string;
  description: string;
  skills: string[];
  mentorFeedback: string;
}

export interface SkillGap {
  id: string;
  skill: string;
  priority: SkillPriority;
  currentLevel: number;
  targetLevel: number;
  resources: string[];
}

export interface LearningResource {
  title: string;
  type: "Course" | "Project" | "Article" | "Practice";
  duration: string;
  url?: string;
}

export interface RoadmapMonth {
  month: string;
  title: string;
  goals: string[];
  resources: LearningResource[];
}

export interface ResumeAnalysis {
  atsScore: number;
  strengths: string[];
  missingSkills: string[];
  suggestions: string[];
  summary: string;
}

export interface InterviewQuestion {
  question: string;
  focusArea: string;
  answerTips: string[];
}

export interface InterviewPreparation {
  targetRole: string;
  readinessScore: number;
  practicePlan: string[];
  questions: InterviewQuestion[];
  tips: string[];
}

export interface DashboardSummary {
  careerFit: number;
  atsScore: number;
  mentorSummary: string;
  topCareers: CareerRecommendation[];
  skillGaps: SkillGap[];
  roadmap: RoadmapMonth[];
  strengths: string[];
  weaknesses: string[];
  nextSteps: string[];
  resumeSuggestions: string[];
}
