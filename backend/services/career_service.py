from __future__ import annotations

from io import BytesIO

from fastapi import UploadFile

from backend.agents.career_mentor import CareerMentorAgent
from backend.models.career import (
    CareerRecommendation,
    DashboardSummary,
    InterviewPreparation,
    ResumeAnalysis,
    RoadmapMonth,
    SkillGap,
)
from backend.models.profile import MentorAdvice, ProfileAnalysis, UserProfile


class CareerService:
    def __init__(self) -> None:
        self._agent = CareerMentorAgent()
        self._profile = UserProfile()
        self._resume_analysis: ResumeAnalysis | None = None

    def save_profile(self, profile: UserProfile) -> ProfileAnalysis:
        self._profile = self._clean_profile(profile)
        return self._agent.analyze_profile(self._profile)

    def get_profile(self) -> UserProfile:
        return self._profile

    def recommend_careers(
        self, profile: UserProfile | None = None
    ) -> list[CareerRecommendation]:
        if profile is not None:
            self._profile = self._clean_profile(profile)
        return self._agent.recommend_careers(self._profile)

    def identify_skill_gaps(self) -> list[SkillGap]:
        return self._agent.identify_skill_gaps(self._profile)

    def generate_learning_roadmap(self) -> list[RoadmapMonth]:
        return self._agent.generate_roadmap(self._profile)

    def generate_interview_preparation(self) -> InterviewPreparation:
        return self._agent.generate_interview_prep(self._profile)

    def mentor_user(self) -> MentorAdvice:
        return self._agent.mentor(self._profile)

    async def analyze_resume(
        self,
        file: UploadFile | None = None,
        resume_text: str | None = None,
    ) -> ResumeAnalysis:
        extracted_text = (resume_text or "").strip()
        if file is not None:
            content = await file.read()
            if (file.filename or "").lower().endswith(".pdf"):
                try:
                    extracted_text = self._agent.extract_resume_text(
                        BytesIO(content).read()
                    )
                except Exception:
                    extracted_text = content.decode("utf-8", errors="ignore").strip()
            else:
                extracted_text = content.decode("utf-8", errors="ignore").strip()
        if extracted_text:
            self._profile = self._profile.model_copy(
                update={"resume_text": extracted_text}
            )
        self._resume_analysis = self._agent.generate_resume_feedback(
            self._profile.resume_text, self._profile
        )
        return self._resume_analysis

    def dashboard_summary(self) -> DashboardSummary:
        mentor = self.mentor_user()
        careers = self.recommend_careers()
        skill_gaps = self.identify_skill_gaps()
        roadmap = self.generate_learning_roadmap()
        resume_analysis = self._resume_analysis or self._agent.generate_resume_feedback(
            self._profile.resume_text, self._profile
        )
        return DashboardSummary(
            career_fit=mentor.career_fit,
            ats_score=resume_analysis.ats_score,
            mentor_summary=mentor.mentor_message,
            top_careers=careers[:3],
            skill_gaps=skill_gaps,
            roadmap=roadmap,
            strengths=mentor.strengths,
            weaknesses=mentor.weaknesses,
            next_steps=mentor.next_steps,
            resume_suggestions=resume_analysis.suggestions,
        )

    def _clean_profile(self, profile: UserProfile) -> UserProfile:
        return profile.model_copy(
            update={
                "name": profile.name.strip(),
                "education": profile.education.strip(),
                "degree": profile.degree.strip(),
                "branch": profile.branch.strip(),
                "experience_level": profile.experience_level.strip(),
                "current_skills": self._clean_list(profile.current_skills),
                "interests": self._clean_list(profile.interests),
                "preferred_roles": self._clean_list(profile.preferred_roles),
                "resume_text": profile.resume_text.strip(),
            }
        )

    def _clean_list(self, values: list[str]) -> list[str]:
        return [value.strip() for value in values if value.strip()]


career_service = CareerService()
