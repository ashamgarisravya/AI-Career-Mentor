from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    name: str = ""
    education: str = ""
    degree: str = ""
    branch: str = ""
    experience_level: str = ""
    current_skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    preferred_roles: list[str] = Field(default_factory=list)
    resume_text: str = ""


class ProfileAnalysis(BaseModel):
    readiness_score: int
    strengths: list[str]
    weaknesses: list[str]
    mentor_summary: str


class MentorAdvice(BaseModel):
    career_fit: int
    mentor_message: str
    strengths: list[str]
    weaknesses: list[str]
    next_steps: list[str]
