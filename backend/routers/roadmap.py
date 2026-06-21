from fastapi import APIRouter

from backend.models.career import RoadmapMonth
from backend.services.career_service import career_service

router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])


@router.get("")
def roadmap() -> list[RoadmapMonth]:
    return career_service.generate_learning_roadmap()
