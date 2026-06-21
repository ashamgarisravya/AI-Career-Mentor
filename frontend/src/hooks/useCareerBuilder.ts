"use client";

import { useCallback, useEffect, useState } from "react";
import {
  analyzeResume,
  getCareerRecommendations,
  getDashboard,
  getInterviewPreparation,
  getProfile,
  getRoadmap,
  getSkillGaps,
  saveProfile
} from "@/services/api";
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

const emptyProfile: UserProfile = {
  name: "",
  education: "",
  degree: "",
  branch: "",
  experienceLevel: "",
  currentSkills: [],
  interests: [],
  preferredRoles: [],
  resumeText: ""
};

export function useCareerBuilder() {
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [profile, setProfile] = useState<UserProfile>(emptyProfile);
  const [profileAnalysis, setProfileAnalysis] = useState<ProfileAnalysis | null>(null);
  const [careers, setCareers] = useState<CareerRecommendation[]>([]);
  const [skillGaps, setSkillGaps] = useState<SkillGap[]>([]);
  const [roadmap, setRoadmap] = useState<RoadmapMonth[]>([]);
  const [resumeAnalysis, setResumeAnalysis] = useState<ResumeAnalysis | null>(null);
  const [interviewPreparation, setInterviewPreparation] = useState<InterviewPreparation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [dashboardData, profileData] = await Promise.all([getDashboard(), getProfile()]);
      setDashboard(dashboardData);
      setProfile(profileData);
      setCareers(dashboardData.topCareers);
      setSkillGaps(dashboardData.skillGaps);
      setRoadmap(dashboardData.roadmap);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setProfile(await getProfile());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load profile.");
    } finally {
      setLoading(false);
    }
  }, []);

  const saveUserProfile = useCallback(async (nextProfile: UserProfile) => {
    setLoading(true);
    setError(null);
    try {
      const analysis = await saveProfile(nextProfile);
      setProfileAnalysis(analysis);
      setProfile(await getProfile());
      await loadDashboard();
      return analysis;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save profile.");
      return null;
    } finally {
      setLoading(false);
    }
  }, [loadDashboard]);

  const discoverCareers = useCallback(async (profileInput: Partial<UserProfile>) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCareerRecommendations(profileInput);
      setCareers(data);
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load career recommendations.");
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const runResumeAnalysis = useCallback(async (file?: File, resumeText?: string) => {
    setLoading(true);
    setError(null);
    try {
      const analysis = await analyzeResume(file, resumeText);
      const dashboardData = await getDashboard();
      setResumeAnalysis(analysis);
      setSkillGaps(await getSkillGaps());
      setRoadmap(await getRoadmap());
      setDashboard(dashboardData);
      setCareers(dashboardData.topCareers);
      setProfile(await getProfile());
      return analysis;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Resume analysis failed.");
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const loadSkillGaps = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setSkillGaps(await getSkillGaps());
      setProfile(await getProfile());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load skill gaps.");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadRoadmap = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setRoadmap(await getRoadmap());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load roadmap.");
    } finally {
      setLoading(false);
    }
  }, []);

  const loadInterviewPreparation = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setInterviewPreparation(await getInterviewPreparation());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load interview preparation.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDashboard();
  }, [loadDashboard]);

  return {
    dashboard,
    profile,
    profileAnalysis,
    careers,
    skillGaps,
    roadmap,
    resumeAnalysis,
    interviewPreparation,
    loading,
    error,
    loadDashboard,
    loadProfile,
    saveUserProfile,
    discoverCareers,
    runResumeAnalysis,
    loadSkillGaps,
    loadRoadmap,
    loadInterviewPreparation
  };
}
