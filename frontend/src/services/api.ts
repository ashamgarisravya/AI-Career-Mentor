import axios from "axios";
import type { CareerRecommendation, ResumeAnalysis, RoadmapMonth, SkillGap, UserProfile } from "@/types/career";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api",
  timeout: 15000
});

export const mockCareers: CareerRecommendation[] = [
  {
    id: "ml-engineer",
    title: "Machine Learning Engineer",
    matchScore: 94,
    salaryRange: "$115k - $175k",
    growth: "+23%",
    description: "Build production AI systems, model pipelines, and intelligent product features.",
    skills: ["Python", "MLOps", "Deep Learning", "APIs"]
  },
  {
    id: "data-scientist",
    title: "Data Scientist",
    matchScore: 89,
    salaryRange: "$100k - $155k",
    growth: "+18%",
    description: "Turn raw data into predictions, insights, experiments, and business decisions.",
    skills: ["Statistics", "SQL", "Python", "Experimentation"]
  },
  {
    id: "ai-product-manager",
    title: "AI Product Manager",
    matchScore: 82,
    salaryRange: "$125k - $190k",
    growth: "+21%",
    description: "Shape AI products by connecting user needs, data strategy, and model capabilities.",
    skills: ["Product Strategy", "Analytics", "Prompting", "Roadmapping"]
  }
];

export const mockSkillGaps: SkillGap[] = [
  {
    id: "mlops",
    skill: "MLOps",
    priority: "High",
    currentLevel: 35,
    targetLevel: 80,
    resources: ["Deploy a model API", "Learn Docker basics", "Study CI/CD for ML"]
  },
  {
    id: "system-design",
    skill: "AI System Design",
    priority: "High",
    currentLevel: 45,
    targetLevel: 85,
    resources: ["Design a recommender system", "Read vector database patterns"]
  },
  {
    id: "statistics",
    skill: "Applied Statistics",
    priority: "Medium",
    currentLevel: 60,
    targetLevel: 78,
    resources: ["Practice A/B testing", "Review regression diagnostics"]
  }
];

export const mockResumeAnalysis: ResumeAnalysis = {
  atsScore: 78,
  summary: "Strong software background with solid Python experience. Add measurable AI project outcomes and production deployment details to improve match quality.",
  strengths: ["Clear project ownership", "Relevant Python skills", "Good technical keywords"],
  missingSkills: mockSkillGaps
};

export const mockRoadmap: RoadmapMonth[] = [
  {
    month: "Month 1",
    title: "Foundation and Positioning",
    goals: ["Refresh Python for data workflows", "Rewrite resume bullets with metrics", "Ship a portfolio landing page"],
    resources: [
      { title: "Python ML Crash Path", type: "Course", duration: "12 hrs" },
      { title: "Resume Metrics Rewrite", type: "Practice", duration: "2 hrs" }
    ]
  },
  {
    month: "Month 2",
    title: "Modeling and Evaluation",
    goals: ["Train baseline models", "Compare evaluation metrics", "Publish one notebook case study"],
    resources: [
      { title: "Classification Project", type: "Project", duration: "1 week" },
      { title: "Model Metrics Guide", type: "Article", duration: "45 min" }
    ]
  },
  {
    month: "Month 3",
    title: "Deployment and Interview Prep",
    goals: ["Deploy a model API", "Practice system design", "Complete five targeted applications"],
    resources: [
      { title: "FastAPI Model API", type: "Project", duration: "1 week" },
      { title: "AI System Design Drills", type: "Practice", duration: "6 hrs" }
    ]
  }
];

export async function getCareerRecommendations(profile?: Partial<UserProfile>) {
  if (!process.env.NEXT_PUBLIC_API_URL) return mockCareers;
  const { data } = await api.post<CareerRecommendation[]>("/careers/recommend", profile ?? {});
  return data;
}

export async function analyzeResume(file?: File) {
  if (!process.env.NEXT_PUBLIC_API_URL) return mockResumeAnalysis;
  const formData = new FormData();
  if (file) formData.append("resume", file);
  const { data } = await api.post<ResumeAnalysis>("/resume/analyze", formData);
  return data;
}

export async function getSkillGaps() {
  if (!process.env.NEXT_PUBLIC_API_URL) return mockSkillGaps;
  const { data } = await api.get<SkillGap[]>("/skills/gaps");
  return data;
}

export async function getRoadmap() {
  if (!process.env.NEXT_PUBLIC_API_URL) return mockRoadmap;
  const { data } = await api.get<RoadmapMonth[]>("/roadmap");
  return data;
}
