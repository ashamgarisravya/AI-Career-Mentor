"use client";

import { useCallback, useEffect, useState } from "react";
import { analyzeResume, getCareerRecommendations, getRoadmap, getSkillGaps } from "@/services/api";
import type { CareerRecommendation, ResumeAnalysis, RoadmapMonth, SkillGap, UserProfile } from "@/types/career";

export function useCareerBuilder() {
  const [careers, setCareers] = useState<CareerRecommendation[]>([]);
  const [skillGaps, setSkillGaps] = useState<SkillGap[]>([]);
  const [roadmap, setRoadmap] = useState<RoadmapMonth[]>([]);
  const [resumeAnalysis, setResumeAnalysis] = useState<ResumeAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [careerData, gapData, roadmapData] = await Promise.all([
        getCareerRecommendations(),
        getSkillGaps(),
        getRoadmap()
      ]);
      setCareers(careerData);
      setSkillGaps(gapData);
      setRoadmap(roadmapData);
    } catch {
      setError("Unable to load career builder data.");
    } finally {
      setLoading(false);
    }
  }, []);

  const discoverCareers = async (profile: Partial<UserProfile>) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCareerRecommendations(profile);
      setCareers(data);
    } catch {
      setError("Unable to generate career recommendations.");
    } finally {
      setLoading(false);
    }
  };

  const runResumeAnalysis = async (file?: File) => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeResume(file);
      setResumeAnalysis(data);
    } catch {
      setError("Resume analysis failed. Try another PDF.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  return {
    careers,
    skillGaps,
    roadmap,
    resumeAnalysis,
    loading,
    error,
    loadDashboard,
    discoverCareers,
    runResumeAnalysis
  };
}
