"""Resume analysis and ATS scoring utilities."""

from __future__ import annotations

import re
from typing import Any

from utils.knowledge import find_career, missing_skills_for_target, normalize


ACTION_WORDS = ("built", "created", "developed", "led", "improved", "deployed", "analyzed")
BASE_KEYWORDS = ("education", "skills", "project", "experience", "certification", "email")


def analyze_resume_text(
    resume_text: str, target_career: str, profile_skills: list[str] | None = None
) -> dict[str, Any]:
    """Analyze resume text using deterministic, explainable rules."""
    profile_skills = profile_skills or []
    text = resume_text.strip()
    lowered = text.lower()
    career = find_career(target_career)
    detected_skills = [
        skill for skill in career.required_skills if skill.lower() in lowered
    ]
    combined_skills = sorted(set(detected_skills + profile_skills))
    missing_skills = missing_skills_for_target(combined_skills, career.title)
    missing_keywords = [keyword for keyword in BASE_KEYWORDS if keyword not in lowered]

    has_email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
    has_metrics = bool(re.search(r"\b\d+%|\b\d+\+|\b\d+x\b", lowered))
    has_projects = "project" in lowered or any(word in lowered for word in ACTION_WORDS)
    score = 25
    score += 10 if has_email else 0
    score += 15 if "education" in lowered else 0
    score += 20 if has_projects else 0
    score += 15 if has_metrics else 0
    score += min(25, len(detected_skills) * 5)
    ats_score = max(20, min(98, score))

    strengths = []
    if has_email:
        strengths.append("Contact information is visible.")
    if has_projects:
        strengths.append("Project or action-oriented experience is present.")
    if has_metrics:
        strengths.append("Measurable impact is included.")
    if detected_skills:
        strengths.append(f"Relevant skills found: {', '.join(detected_skills[:5])}.")

    weaknesses = []
    if not has_email:
        weaknesses.append("Add professional email/contact details.")
    if not has_projects:
        weaknesses.append("Add project work with tools, outcomes, and responsibilities.")
    if not has_metrics:
        weaknesses.append("Add numbers such as accuracy, users, time saved, or impact.")
    if missing_skills:
        weaknesses.append(f"Missing target skills: {', '.join(missing_skills[:4])}.")

    suggestions = [
        "Use clear section headings: Summary, Skills, Projects, Education, Experience.",
        "Rewrite bullets with action verb + tool + measurable result.",
        f"Add evidence for {career.title} skills through projects or coursework.",
    ]
    if missing_skills:
        suggestions.append(f"Prioritize adding {missing_skills[0]} to your next project.")

    summary = (
        f"This resume is currently scoring {ats_score}% for {career.title}. "
        f"It has {len(detected_skills)} target-skill signals and "
        f"{len(missing_skills)} notable skill gaps."
    )

    return {
        "ats_score": ats_score,
        "strengths": strengths or ["Resume content was detected and can be improved."],
        "weaknesses": weaknesses or ["No major structural weakness detected."],
        "missing_skills": missing_skills,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "summary": summary,
    }
