from pydantic import BaseModel, Field


class CareerRecommendation(BaseModel):
    id: str
    title: str
    match_score: int = Field(serialization_alias="matchScore")
    salary_range: str = Field(serialization_alias="salaryRange")
    growth: str = Field(serialization_alias="growthRate")
    description: str
    skills: list[str]
    mentor_feedback: str = Field(serialization_alias="mentorFeedback")

    model_config = {"populate_by_name": True}


class SkillGap(BaseModel):
    id: str
    skill: str
    priority: str
    current_level: int = Field(serialization_alias="currentLevel")
    target_level: int = Field(serialization_alias="targetLevel")
    resources: list[str]

    model_config = {"populate_by_name": True}


class LearningResource(BaseModel):
    title: str
    type: str
    duration: str
    url: str | None = None


class RoadmapMonth(BaseModel):
    month: str
    title: str
    goals: list[str]
    resources: list[LearningResource]


class ResumeAnalysis(BaseModel):
    ats_score: int = Field(serialization_alias="atsScore")
    strengths: list[str]
    missing_skills: list[str] = Field(serialization_alias="missingSkills")
    suggestions: list[str]
    summary: str

    model_config = {"populate_by_name": True}


class InterviewQuestion(BaseModel):
    question: str
    focus_area: str = Field(serialization_alias="focusArea")
    answer_tips: list[str] = Field(serialization_alias="answerTips")

    model_config = {"populate_by_name": True}


class InterviewPreparation(BaseModel):
    target_role: str = Field(serialization_alias="targetRole")
    readiness_score: int = Field(serialization_alias="readinessScore")
    practice_plan: list[str] = Field(serialization_alias="practicePlan")
    questions: list[InterviewQuestion]
    tips: list[str]

    model_config = {"populate_by_name": True}


class DashboardSummary(BaseModel):
    career_fit: int = Field(serialization_alias="careerFit")
    ats_score: int = Field(serialization_alias="atsScore")
    mentor_summary: str = Field(serialization_alias="mentorSummary")
    top_careers: list[CareerRecommendation] = Field(serialization_alias="topCareers")
    skill_gaps: list[SkillGap] = Field(serialization_alias="skillGaps")
    roadmap: list[RoadmapMonth]
    strengths: list[str]
    weaknesses: list[str]
    next_steps: list[str] = Field(serialization_alias="nextSteps")
    resume_suggestions: list[str] = Field(serialization_alias="resumeSuggestions")

    model_config = {"populate_by_name": True}
