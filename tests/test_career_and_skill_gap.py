from utils.knowledge import (
    analyze_skill_gap,
    detect_resume_sections,
    extract_skills_from_text,
    find_career,
    merge_skills,
    missing_skills_for_target,
    normalize,
    recommend_careers,
    required_keywords_for_career,
    text_has_skill,
)

RESUME_TEXT = """
Summary
Python developer with SQL analytics experience.
Skills
Python, SQL, pandas, APIs, Git, pytest
Projects
Built dashboards and REST APIs for product metrics.
Education
B.Tech
"""


def test_skill_detection_and_resume_sections() -> None:
    assert normalize([" Python ", "", "SQL"]) == {"python", "sql"}
    assert text_has_skill("Built REST endpoints with FastAPI", "APIs")
    assert "Python" in extract_skills_from_text(RESUME_TEXT)
    assert merge_skills(["Python"], ["python", "SQL"]) == ["Python", "SQL"]

    sections = detect_resume_sections(RESUME_TEXT)

    assert sections["summary"]
    assert sections["skills"]
    assert sections["projects"]
    assert not sections["certifications"]


def test_career_lookup_and_missing_skills() -> None:
    career = find_career("data")

    assert career.title == "Data Scientist"
    assert "Python" in required_keywords_for_career(career)
    assert missing_skills_for_target(["Python", "SQL"], "Data Scientist") == [
        "Statistics",
        "Machine Learning",
        "Visualization",
        "Experimentation",
    ]
    assert find_career("unknown role").title == "AI Engineer"


def test_career_recommendation_ranks_relevant_roles() -> None:
    recommendations = recommend_careers(
        skills=["Python", "SQL", "Machine Learning", "Visualization"],
        interests=["data", "ai", "experimentation"],
        education="B.Tech Computer Science",
        industry="Data",
        resume_text=RESUME_TEXT,
    )

    assert recommendations[0]["match"] >= recommendations[-1]["match"]
    assert recommendations[0]["title"]
    assert recommendations[0]["match"] >= 70
    assert recommendations[0]["salary_range"]
    assert recommendations[0]["resources"]
    assert "why" in recommendations[0]


def test_career_recommendation_validates_ai_output(monkeypatch) -> None:
    monkeypatch.setattr(
        "utils.knowledge.ai_json",
        lambda **kwargs: {
            "recommendations": [
                {
                    "title": "AI Engineer",
                    "industry": "Artificial Intelligence",
                    "match": "99",
                    "salary_range": "INR 10-30 LPA",
                    "growth": "Very high",
                    "required_skills": ["Python", "LLMs"],
                    "missing_skills": ["Vector Databases"],
                    "why": "Strong AI alignment.",
                    "resources": ["DeepLearning.AI"],
                }
            ]
        },
    )

    recommendations = recommend_careers(
        skills=["Python"],
        interests=["ai"],
        education="B.Tech",
        industry="Artificial Intelligence",
        resume_text=RESUME_TEXT,
    )

    assert recommendations[0]["title"] == "AI Engineer"
    assert recommendations[0]["match"] == 99


def test_skill_gap_analysis_prioritizes_missing_skills() -> None:
    gaps = analyze_skill_gap(["Python", "SQL"], "AI Engineer", resume_text=RESUME_TEXT)

    assert gaps
    assert gaps[0]["Priority"] == "High"
    assert gaps[0]["Estimated Learning Time"].endswith("weeks")
    assert "Recommended Learning Path" in gaps[0]
    assert all("Missing Skill" in row for row in gaps)


def test_skill_gap_analysis_validates_ai_output(monkeypatch) -> None:
    monkeypatch.setattr(
        "utils.knowledge.ai_json",
        lambda **kwargs: {
            "gaps": [
                {
                    "Missing Skill": "LLMs",
                    "Priority": "High",
                    "Difficulty": "Intermediate",
                    "Estimated Learning Time": "4-6 weeks",
                    "Recommended Learning Path": "Build a chatbot.",
                    "Progress Weight": 25,
                }
            ]
        },
    )

    assert analyze_skill_gap(["Python"], "AI Engineer")[0]["Missing Skill"] == "LLMs"
