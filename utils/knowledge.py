"""Career knowledge base and deterministic recommendation helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from utils.ai import ai_json

@dataclass(frozen=True)
class Career:
    title: str
    industry: str
    salary_range: str
    growth: str
    required_skills: tuple[str, ...]
    resources: tuple[str, ...]


CAREERS: tuple[Career, ...] = (
    Career(
        "Data Scientist",
        "Data and AI",
        "INR 8-24 LPA",
        "High growth across product, finance, health, and AI teams",
        ("Python", "SQL", "Statistics", "Machine Learning", "Visualization", "Experimentation"),
        ("Kaggle Learn", "Google Data Analytics", "Hands-on ML projects", "Storytelling with Data"),
    ),
    Career(
        "AI Engineer",
        "Artificial Intelligence",
        "INR 10-30 LPA",
        "Very high growth driven by LLM, automation, and applied AI adoption",
        ("Python", "Machine Learning", "Deep Learning", "LLMs", "APIs", "Vector Databases"),
        ("DeepLearning.AI", "Fast.ai", "Build an LLM chatbot", "Open-source model deployment"),
    ),
    Career(
        "Full Stack Developer",
        "Software Engineering",
        "INR 6-22 LPA",
        "High growth for builders who can ship reliable web products",
        ("Python", "JavaScript", "SQL", "APIs", "Git", "Testing"),
        ("Full Stack Open", "Django/Flask projects", "System design basics", "Testing practice"),
    ),
    Career(
        "Product Analyst",
        "Product and Analytics",
        "INR 6-18 LPA",
        "High growth in SaaS, fintech, marketplace, and consumer product teams",
        ("SQL", "Analytics", "Experimentation", "Visualization", "Communication", "Product Metrics"),
        ("Mode SQL Tutorial", "A/B testing practice", "Product teardown notes", "Metric design case studies"),
    ),
    Career(
        "Cloud Data Engineer",
        "Cloud and Data",
        "INR 8-26 LPA",
        "Very high growth as companies modernize data platforms",
        ("Python", "SQL", "ETL", "Cloud", "Data Warehousing", "Orchestration"),
        ("AWS Skill Builder", "dbt fundamentals", "ETL portfolio pipeline", "Airflow project"),
    ),
    Career(
        "Cybersecurity Analyst",
        "Security",
        "INR 7-20 LPA",
        "High growth as organizations expand security operations",
        ("Networking", "Linux", "SIEM", "Incident Response", "Python", "Risk Analysis"),
        ("TryHackMe SOC paths", "Blue Team Labs", "Security+ objectives", "Incident report practice"),
    ),
    Career(
        "DevOps Engineer",
        "Cloud and Infrastructure",
        "INR 8-28 LPA",
        "Very high growth for automation, deployment, and reliability work",
        ("Linux", "Git", "CI/CD", "Docker", "Cloud", "Monitoring"),
        ("Docker docs", "GitHub Actions labs", "AWS Skill Builder", "SRE workbook"),
    ),
)

SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "APIs": ("api", "rest", "fastapi", "flask", "django rest", "endpoint"),
    "Analytics": ("analytics", "analysis", "insights", "dashboard"),
    "CI/CD": ("ci/cd", "github actions", "jenkins", "deployment pipeline"),
    "Cloud": ("aws", "azure", "gcp", "cloud"),
    "Communication": ("communication", "stakeholder", "presentation", "storytelling"),
    "Data Warehousing": ("warehouse", "snowflake", "bigquery", "redshift"),
    "Deep Learning": ("deep learning", "neural network", "cnn", "rnn", "transformer"),
    "Docker": ("docker", "container", "containerization"),
    "ETL": ("etl", "elt", "pipeline", "data ingestion"),
    "Experimentation": ("a/b", "ab test", "experiment", "hypothesis"),
    "Git": ("git", "github", "version control"),
    "Incident Response": ("incident response", "triage", "security incident"),
    "LLMs": ("llm", "large language model", "rag", "prompt engineering", "generative ai"),
    "Linux": ("linux", "shell", "bash", "ubuntu"),
    "Machine Learning": ("machine learning", "ml", "scikit", "model training", "classification"),
    "Monitoring": ("monitoring", "observability", "prometheus", "grafana", "logging"),
    "Networking": ("networking", "tcp/ip", "dns", "firewall"),
    "Orchestration": ("airflow", "prefect", "orchestration", "dag"),
    "Product Metrics": ("activation", "retention", "conversion", "north star"),
    "Python": ("python", "pandas", "numpy"),
    "Risk Analysis": ("risk", "threat", "vulnerability", "compliance"),
    "SIEM": ("siem", "splunk", "sentinel", "security monitoring"),
    "SQL": ("sql", "mysql", "postgres", "postgresql", "sqlite"),
    "Statistics": ("statistics", "probability", "regression", "hypothesis testing"),
    "Testing": ("testing", "pytest", "unit test", "integration test"),
    "Vector Databases": ("vector database", "faiss", "pinecone", "chroma", "embeddings"),
    "Visualization": ("visualization", "tableau", "power bi", "plotly", "matplotlib", "chart"),
}

RESUME_SECTIONS = {
    "summary": ("summary", "objective", "profile"),
    "skills": ("skills", "technical skills", "tools"),
    "experience": ("experience", "work experience", "internship"),
    "projects": ("projects", "portfolio"),
    "education": ("education", "academic"),
    "certifications": ("certification", "certifications", "courses"),
}


def normalize(values: list[str]) -> set[str]:
    """Normalize skill strings for matching."""
    return {value.strip().lower() for value in values if value.strip()}


def normalize_text(value: str) -> str:
    """Return lowercase text with collapsed whitespace."""
    return re.sub(r"\s+", " ", value or "").strip().lower()


def skill_terms(skill: str) -> tuple[str, ...]:
    """Return searchable aliases for a canonical skill."""
    return SKILL_ALIASES.get(skill, (skill.lower(),))


def text_has_skill(text: str, skill: str) -> bool:
    """Check whether text contains a skill or one of its aliases."""
    lowered = normalize_text(text)
    for term in skill_terms(skill):
        pattern = r"(?<![a-z0-9+#])" + re.escape(term.lower()) + r"(?![a-z0-9+#])"
        if re.search(pattern, lowered):
            return True
    return False


def extract_skills_from_text(text: str) -> list[str]:
    """Detect known career skills from resume or profile text."""
    found = []
    for skill in sorted(SKILL_ALIASES):
        if text_has_skill(text, skill):
            found.append(skill)
    return found


def merge_skills(*groups: list[str]) -> list[str]:
    """Merge skill lists while preserving readable canonical casing."""
    seen: set[str] = set()
    merged: list[str] = []
    for group in groups:
        for skill in group:
            key = skill.strip().lower()
            if key and key not in seen:
                seen.add(key)
                merged.append(skill.strip())
    return merged


def find_career(target: str) -> Career:
    """Find the best career by title, falling back to AI Engineer."""
    target_lower = normalize_text(target)
    for career in CAREERS:
        if career.title.lower() == target_lower:
            return career
    for career in CAREERS:
        if target_lower and (target_lower in career.title.lower() or career.title.lower() in target_lower):
            return career
    return CAREERS[1]


def missing_skills_for_target(current_skills: list[str], target_career: str) -> list[str]:
    """Return required skills missing for a target career."""
    career = find_career(target_career)
    current_text = ", ".join(current_skills)
    current = normalize(current_skills)
    missing = []
    for skill in career.required_skills:
        if skill.lower() not in current and not text_has_skill(current_text, skill):
            missing.append(skill)
    return missing


def required_keywords_for_career(career: Career) -> list[str]:
    """Return role-specific ATS keywords that should appear in a resume."""
    keywords = list(career.required_skills)
    keywords.extend(["project", "impact", "metrics", career.industry.split()[0]])
    return keywords


def detect_resume_sections(text: str) -> dict[str, bool]:
    """Detect standard resume sections."""
    lowered = normalize_text(text)
    return {
        section: any(re.search(rf"\b{re.escape(term)}\b", lowered) for term in terms)
        for section, terms in RESUME_SECTIONS.items()
    }


def recommend_careers(
    skills: list[str],
    interests: list[str],
    education: str,
    industry: str,
    resume_text: str = "",
    resume_missing_skills: list[str] | None = None,
) -> list[dict[str, object]]:
    """Generate career recommendations from profile and latest resume signals."""
    resume_skills = extract_skills_from_text(resume_text)
    skill_set = normalize(merge_skills(skills, resume_skills))
    interest_text = normalize_text(" ".join(interests))
    industry_lower = normalize_text(industry)
    education_lower = normalize_text(education)
    resume_lower = normalize_text(resume_text)
    known_gaps = normalize(resume_missing_skills or [])

    recommendations: list[dict[str, object]] = []
    for career in CAREERS:
        required = normalize(list(career.required_skills))
        skill_hits = len(required & skill_set)
        missing = [skill for skill in career.required_skills if skill.lower() not in skill_set]
        interest_hits = sum(
            token in career.title.lower() or token in career.industry.lower()
            for token in interest_text.split()
            if len(token) > 2
        )
        industry_bonus = 10 if industry_lower and industry_lower in career.industry.lower() else 0
        education_bonus = 6 if education_lower else 0
        resume_bonus = min(14, sum(1 for skill in career.required_skills if text_has_skill(resume_lower, skill)) * 3)
        gap_penalty = min(10, len(required & known_gaps) * 2)
        score = max(25, min(98, 28 + skill_hits * 9 + interest_hits * 3 + industry_bonus + education_bonus + resume_bonus - gap_penalty))
        matched = [skill for skill in career.required_skills if skill.lower() in skill_set or text_has_skill(resume_lower, skill)]

        if matched:
            reason = f"Strongest fit because your profile/resume shows {', '.join(matched[:4])}."
        elif interest_hits:
            reason = f"Good exploratory fit because your interests align with {career.industry} work."
        else:
            reason = f"Potential fit if you build evidence for {', '.join(career.required_skills[:3])}."

        recommendations.append(
            {
                "title": career.title,
                "industry": career.industry,
                "match": score,
                "salary_range": career.salary_range,
                "growth": career.growth,
                "required_skills": list(career.required_skills),
                "missing_skills": missing,
                "why": reason,
                "resources": list(career.resources),
            }
        )
    fallback = sorted(recommendations, key=lambda item: int(item["match"]), reverse=True)
    prompt = _json_prompt(
        {
            "profile_skills": skills,
            "interests": interests,
            "education": education,
            "target_industry": industry,
            "resume_excerpt": resume_text[:6000],
            "resume_missing_skills": resume_missing_skills or [],
            "available_careers": [
                {
                    "title": career.title,
                    "industry": career.industry,
                    "salary_range": career.salary_range,
                    "growth": career.growth,
                    "required_skills": list(career.required_skills),
                    "resources": list(career.resources),
                }
                for career in CAREERS
            ],
            "rule_based_recommendations": fallback,
            "required_output": {
                "recommendations": "list of role objects with title, industry, match, salary_range, growth, required_skills, missing_skills, why, resources",
            },
        }
    )
    result = ai_json(task="career recommendation", prompt=prompt, fallback={"recommendations": fallback}, expected_type=dict)
    return _valid_recommendations(result.get("recommendations"), fallback)


def analyze_skill_gap(current_skills: list[str], target_career: str, resume_text: str = "") -> list[dict[str, Any]]:
    """Build prioritized skill-gap rows for a selected target career."""
    career = find_career(target_career)
    detected = extract_skills_from_text(resume_text)
    available = merge_skills(current_skills, detected)
    missing = missing_skills_for_target(available, career.title)
    rows: list[dict[str, Any]] = []
    total = max(len(missing), 1)
    for index, skill in enumerate(missing):
        priority = "High" if index < 2 else "Medium" if index < 4 else "Low"
        weeks = 4 if priority == "High" else 3 if priority == "Medium" else 2
        if skill in {"Deep Learning", "LLMs", "Cloud", "Data Warehousing", "Orchestration", "Incident Response"}:
            difficulty = "Intermediate"
            weeks += 1
        else:
            difficulty = "Beginner to Intermediate"
        rows.append(
            {
                "Missing Skill": skill,
                "Priority": priority,
                "Difficulty": difficulty,
                "Estimated Learning Time": f"{weeks}-{weeks + 2} weeks",
                "Recommended Learning Path": (
                    f"Learn {skill} fundamentals, complete one guided lab, then add a "
                    f"{career.title} portfolio task that demonstrates {skill}."
                ),
                "Progress Weight": round(100 / total),
            }
        )
    prompt = _json_prompt(
        {
            "current_skills": current_skills,
            "target_career": career.title,
            "resume_excerpt": resume_text[:6000],
            "rule_based_gaps": rows,
            "required_output": {
                "gaps": "list with Missing Skill, Priority, Difficulty, Estimated Learning Time, Recommended Learning Path, Progress Weight",
            },
        }
    )
    result = ai_json(task="skill gap analysis", prompt=prompt, fallback={"gaps": rows}, expected_type=dict)
    return _valid_gap_rows(result.get("gaps"), rows)


def _json_prompt(payload: dict[str, Any]) -> str:
    import json

    return json.dumps(payload, ensure_ascii=True)


def _valid_recommendations(value: Any, fallback: list[dict[str, object]]) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return fallback
    valid = []
    fallback_by_title = {str(item["title"]).lower(): item for item in fallback}
    for item in value:
        if not isinstance(item, dict) or not item.get("title"):
            continue
        base = fallback_by_title.get(str(item["title"]).lower(), {})
        try:
            match = max(0, min(100, int(item.get("match", base.get("match", 50)))))
        except (TypeError, ValueError):
            match = int(base.get("match", 50))
        valid.append(
            {
                "title": str(item.get("title", base.get("title", ""))),
                "industry": str(item.get("industry", base.get("industry", ""))),
                "match": match,
                "salary_range": str(item.get("salary_range", base.get("salary_range", ""))),
                "growth": str(item.get("growth", base.get("growth", ""))),
                "required_skills": _as_list(item.get("required_skills"), list(base.get("required_skills", []))),
                "missing_skills": _as_list(item.get("missing_skills"), list(base.get("missing_skills", []))),
                "why": str(item.get("why", base.get("why", ""))),
                "resources": _as_list(item.get("resources"), list(base.get("resources", []))),
            }
        )
    return sorted(valid, key=lambda item: int(item["match"]), reverse=True) or fallback


def _valid_gap_rows(value: Any, fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return fallback
    valid = []
    for item in value:
        if not isinstance(item, dict) or not item.get("Missing Skill"):
            continue
        valid.append(
            {
                "Missing Skill": str(item.get("Missing Skill", "")),
                "Priority": str(item.get("Priority", "Medium")),
                "Difficulty": str(item.get("Difficulty", "Intermediate")),
                "Estimated Learning Time": str(item.get("Estimated Learning Time", "2-4 weeks")),
                "Recommended Learning Path": str(item.get("Recommended Learning Path", "Learn fundamentals, complete a guided lab, and build one portfolio task.")),
                "Progress Weight": item.get("Progress Weight", 10),
            }
        )
    return valid or fallback


def _as_list(value: Any, fallback: list[str]) -> list[str]:
    if not isinstance(value, list):
        return fallback
    cleaned = [str(item).strip() for item in value if str(item).strip()]
    return cleaned or fallback
