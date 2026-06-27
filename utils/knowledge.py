"""Career knowledge base and deterministic recommendation helpers."""

from __future__ import annotations

from dataclasses import dataclass


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
        "High",
        ("Python", "SQL", "Statistics", "Machine Learning", "Visualization"),
        ("Kaggle Learn", "Google Data Analytics", "Hands-on ML projects"),
    ),
    Career(
        "AI Engineer",
        "Artificial Intelligence",
        "INR 10-30 LPA",
        "Very High",
        ("Python", "Machine Learning", "Deep Learning", "LLMs", "APIs"),
        ("DeepLearning.AI", "Fast.ai", "Build an LLM chatbot"),
    ),
    Career(
        "Full Stack Developer",
        "Software Engineering",
        "INR 6-22 LPA",
        "High",
        ("Python", "JavaScript", "SQL", "APIs", "Git"),
        ("Full Stack Open", "Django/Flask projects", "System design basics"),
    ),
    Career(
        "Product Analyst",
        "Product and Analytics",
        "INR 6-18 LPA",
        "High",
        ("SQL", "Analytics", "Experimentation", "Visualization", "Communication"),
        ("Mode SQL Tutorial", "A/B testing practice", "Product teardown notes"),
    ),
    Career(
        "Cloud Data Engineer",
        "Cloud and Data",
        "INR 8-26 LPA",
        "Very High",
        ("Python", "SQL", "ETL", "Cloud", "Data Warehousing"),
        ("AWS Skill Builder", "dbt fundamentals", "ETL portfolio pipeline"),
    ),
)


def normalize(values: list[str]) -> set[str]:
    """Normalize skill strings for matching."""
    return {value.strip().lower() for value in values if value.strip()}


def find_career(target: str) -> Career:
    """Find the best career by title, falling back to AI Engineer."""
    target_lower = target.strip().lower()
    for career in CAREERS:
        if career.title.lower() == target_lower:
            return career
    for career in CAREERS:
        if target_lower and target_lower in career.title.lower():
            return career
    return CAREERS[1]


def recommend_careers(
    skills: list[str], interests: list[str], education: str, industry: str
) -> list[dict[str, object]]:
    """Generate deterministic career recommendations."""
    skill_set = normalize(skills)
    interest_set = normalize(interests)
    industry_lower = industry.lower()
    education_bonus = 8 if education.strip() else 0
    recommendations: list[dict[str, object]] = []
    for career in CAREERS:
        required = normalize(list(career.required_skills))
        skill_hits = len(required & skill_set)
        interest_hits = sum(token in career.title.lower() for token in interest_set)
        industry_bonus = 12 if industry_lower and industry_lower in career.industry.lower() else 0
        score = min(98, 30 + skill_hits * 12 + interest_hits * 5 + industry_bonus + education_bonus)
        missing = [skill for skill in career.required_skills if skill.lower() not in skill_set]
        recommendations.append(
            {
                "title": career.title,
                "industry": career.industry,
                "match": score,
                "salary_range": career.salary_range,
                "growth": career.growth,
                "required_skills": list(career.required_skills),
                "missing_skills": missing,
                "why": (
                    f"Matches {skill_hits} core skills and aligns with "
                    f"{industry or career.industry} opportunities."
                ),
                "resources": list(career.resources),
            }
        )
    return sorted(recommendations, key=lambda item: int(item["match"]), reverse=True)


def missing_skills_for_target(current_skills: list[str], target_career: str) -> list[str]:
    """Return required skills missing for a target career."""
    career = find_career(target_career)
    current = normalize(current_skills)
    return [skill for skill in career.required_skills if skill.lower() not in current]
