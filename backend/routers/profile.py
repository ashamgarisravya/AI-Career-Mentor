from fastapi import APIRouter

from backend.models.profile import ProfileAnalysis, UserProfile
from backend.services.career_service import career_service

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("")
def get_profile() -> UserProfile:
    return career_service.get_profile()


@router.post("")
def save_profile(profile: UserProfile) -> ProfileAnalysis:
    return career_service.save_profile(profile)
