from fastapi import APIRouter

from backend.models.career import InterviewPreparation
from backend.services.career_service import career_service

router = APIRouter(prefix="/api/interview", tags=["interview"])


@router.get("/prep", response_model_by_alias=True)
def interview_prep() -> InterviewPreparation:
    return career_service.generate_interview_preparation()
