"""Resume analysis and ATS scoring utilities."""

from __future__ import annotations

import re
from typing import Any

from utils.ai import ai_json
from utils.knowledge import (
    detect_resume_sections,
    extract_skills_from_text,
    find_career,
    missing_skills_for_target,
    required_keywords_for_career,
    text_has_skill,
)

ACTION_WORDS = (
    "achieved",
    "analyzed",
    "automated",
    "built",
    "created",
    "deployed",
    "designed",
    "developed",
    "improved",
    "implemented",
    "led",
    "optimized",
    "reduced",
    "shipped",
)
CONTACT_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
METRIC_RE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:%|x|k|m|users|hours|days|projects|models|apis|dashboards)\b", re.I)


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def _summary(text: str, career_title: str, score: int, detected: list[str], missing: list[str]) -> str:
    sentences = _sentences(text)
    lead = sentences[0][:220] if sentences else "The resume has limited readable text."
    return (
        f"{lead} Overall, it scores {score}% for {career_title}. "
        f"Detected role signals include {', '.join(detected[:5]) if detected else 'no strong target skills yet'}, "
        f"with {len(missing)} important skill gap(s) to close."
    )


def analyze_resume_text(
    resume_text: str, target_career: str, profile_skills: list[str] | None = None
) -> dict[str, Any]:
    """Analyze resume text using deterministic, explainable ATS rules."""
    profile_skills = profile_skills or []
    text = resume_text.strip()
    lowered = text.lower()
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.-]+", text)
    word_count = len(words)
    career = find_career(target_career)
    sections = detect_resume_sections(text)
    detected_skills = extract_skills_from_text(text)
    profile_and_resume = sorted(set(detected_skills + profile_skills))
    missing_skills = missing_skills_for_target(profile_and_resume, career.title)
    role_keywords = required_keywords_for_career(career)
    missing_keywords = [
        keyword
        for keyword in role_keywords
        if not text_has_skill(text, keyword) and keyword.lower() not in lowered
    ]

    has_email = bool(CONTACT_RE.search(text))
    has_metrics = bool(METRIC_RE.search(text))
    action_hits = sorted({word for word in ACTION_WORDS if re.search(rf"\b{word}\b", lowered)})
    section_score = sum(1 for present in sections.values() if present) * 5
    skill_score = min(28, sum(1 for skill in career.required_skills if skill in detected_skills) * 5)
    keyword_score = min(16, (len(role_keywords) - len(missing_keywords)) * 2)
    length_score = 12 if 250 <= word_count <= 900 else 8 if word_count >= 120 else 3
    contact_score = 8 if has_email else 0
    impact_score = 12 if has_metrics else 4 if action_hits else 0
    action_score = min(12, len(action_hits) * 3)
    ats_score = max(10, min(100, section_score + skill_score + keyword_score + length_score + contact_score + impact_score + action_score))

    strengths = []
    if has_email:
        strengths.append("Contact email is visible for recruiter follow-up.")
    if sections["skills"]:
        strengths.append("Skills section is easy for ATS parsing.")
    if sections["projects"] or sections["experience"]:
        strengths.append("Project or experience evidence is present.")
    if has_metrics:
        strengths.append("Resume includes measurable impact, which strengthens ranking.")
    if action_hits:
        strengths.append(f"Uses action verbs such as {', '.join(action_hits[:5])}.")
    if detected_skills:
        strengths.append(f"Relevant technical signals found: {', '.join(detected_skills[:6])}.")

    weaknesses = []
    if not has_email:
        weaknesses.append("Missing clear email/contact information.")
    if word_count < 120:
        weaknesses.append("Resume text is too short for strong ATS matching.")
    for section, present in sections.items():
        if not present and section in {"skills", "projects", "experience", "education"}:
            weaknesses.append(f"Missing or unclear {section} section.")
    if not has_metrics:
        weaknesses.append("Achievements need measurable outcomes such as accuracy, users, time saved, or revenue impact.")
    if missing_skills:
        weaknesses.append(f"Missing target skills for {career.title}: {', '.join(missing_skills[:5])}.")

    suggestions = [
        "Use standard headings: Summary, Skills, Experience, Projects, Education, Certifications.",
        "Rewrite bullets as action verb + tool/skill + business or technical outcome.",
        f"Add a targeted {career.title} project that demonstrates {', '.join((missing_skills or list(career.required_skills))[:2])}.",
    ]
    if missing_keywords:
        suggestions.append(f"Add role keywords naturally: {', '.join(missing_keywords[:6])}.")
    if not has_metrics:
        suggestions.append("Add at least three quantified bullets, for example accuracy improved, time reduced, or users served.")
    if word_count < 250:
        suggestions.append("Expand the resume with concise project responsibilities, tools used, and outcomes.")

    fallback = {
        "ats_score": ats_score,
        "strengths": strengths or ["Readable resume text was detected."],
        "weaknesses": weaknesses or ["No major ATS weakness detected for the selected target."],
        "missing_skills": missing_skills,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "summary": _summary(text, career.title, ats_score, detected_skills, missing_skills),
    }
    if word_count < 40:
        return fallback

    prompt = json_prompt(
        {
            "resume_text": text[:8000],
            "target_career": career.title,
            "profile_skills": profile_skills,
            "rule_based_analysis": fallback,
            "required_output": {
                "ats_score": "integer 0-100",
                "strengths": "list of strings",
                "weaknesses": "list of strings",
                "missing_skills": "list of strings",
                "missing_keywords": "list of strings",
                "suggestions": "list of actionable strings",
                "summary": "one concise paragraph",
            },
        }
    )
    result = ai_json(task="resume analysis", prompt=prompt, fallback=fallback, expected_type=dict)
    return _valid_resume_analysis(result, fallback)


def json_prompt(payload: dict[str, Any]) -> str:
    """Serialize prompt payload consistently."""
    import json

    return json.dumps(payload, ensure_ascii=True)


def _string_list(value: Any, fallback: list[str]) -> list[str]:
    if not isinstance(value, list):
        return fallback
    cleaned = [str(item).strip() for item in value if str(item).strip()]
    return cleaned or fallback


def _valid_resume_analysis(result: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        score = int(result.get("ats_score", fallback["ats_score"]))
    except (TypeError, ValueError):
        score = int(fallback["ats_score"])
    return {
        "ats_score": max(0, min(100, score)),
        "strengths": _string_list(result.get("strengths"), fallback["strengths"]),
        "weaknesses": _string_list(result.get("weaknesses"), fallback["weaknesses"]),
        "missing_skills": _string_list(result.get("missing_skills"), fallback["missing_skills"]),
        "missing_keywords": _string_list(result.get("missing_keywords"), fallback["missing_keywords"]),
        "suggestions": _string_list(result.get("suggestions"), fallback["suggestions"]),
        "summary": str(result.get("summary") or fallback["summary"]).strip(),
    }
