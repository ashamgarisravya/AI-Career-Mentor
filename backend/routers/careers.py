from fastapi import APIRouter

from backend.models.career import CareerRecommendation, DashboardSummary, SkillGap
from backend.models.profile import UserProfile
from backend.services.career_service import career_service

router = APIRouter(prefix="/api", tags=["careers"])


@router.post(
    "/careers/recommend",
    response_model_by_alias=True,
)
def recommend_careers(profile: UserProfile) -> list[CareerRecommendation]:
    return career_service.recommend_careers(profile)


@router.get(
    "/skills/gaps",
    response_model_by_alias=True,
)
def skill_gaps() -> list[SkillGap]:
    return career_service.identify_skill_gaps()


@router.get(
    "/dashboard",
    response_model_by_alias=True,
)
def dashboard() -> DashboardSummary:
    return career_service.dashboard_summary()
