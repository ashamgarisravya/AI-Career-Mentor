from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from backend.models.career import ResumeAnalysis
from backend.services.career_service import career_service

router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.post(
    "/analyze",
    response_model_by_alias=True,
)
async def analyze_resume(
    resume: Annotated[UploadFile | None, File()] = None,
    resume_text: Annotated[str | None, Form()] = None,
) -> ResumeAnalysis:
    return await career_service.analyze_resume(resume, resume_text)
