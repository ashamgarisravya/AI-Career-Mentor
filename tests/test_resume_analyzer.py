from utils.ats import analyze_resume_text

STRONG_DATA_RESUME = """
Jane Doe
jane@example.com

Summary
Data scientist focused on machine learning, statistics, SQL, Python, and visualization.

Skills
Python, SQL, Statistics, Machine Learning, Visualization, Experimentation, pandas, plotly

Experience
Built churn models and improved retention dashboards for 25000 users.
Automated reporting workflows and reduced analysis time by 35%.

Projects
Created an experimentation dashboard with metrics, regression analysis, and model monitoring.

Education
B.Tech Computer Science
"""


def test_resume_analyzer_scores_strong_targeted_resume() -> None:
    analysis = analyze_resume_text(STRONG_DATA_RESUME, "Data Scientist")

    assert 0 <= analysis["ats_score"] <= 100
    assert analysis["ats_score"] >= 70
    assert "summary" in analysis and "Data Scientist" in analysis["summary"]
    assert "Python" not in analysis["missing_skills"]
    assert any("measurable impact" in item.lower() for item in analysis["strengths"])
    assert analysis["suggestions"]


def test_resume_analyzer_returns_explainable_fallback_for_short_resume() -> None:
    analysis = analyze_resume_text("Alex built websites.", "AI Engineer")

    assert analysis["ats_score"] >= 10
    assert "summary" in analysis
    assert "Python" in analysis["missing_skills"]
    assert any("too short" in item.lower() for item in analysis["weaknesses"])
    assert any("standard headings" in item.lower() for item in analysis["suggestions"])


def test_resume_analyzer_uses_ai_result_when_valid(monkeypatch) -> None:
    expected = {
        "ats_score": 88,
        "strengths": ["Strong Python projects"],
        "weaknesses": ["Needs more deployment detail"],
        "missing_skills": ["LLMs"],
        "missing_keywords": ["Vector Databases"],
        "suggestions": ["Add a retrieval augmented generation project."],
        "summary": "Strong AI Engineer candidate.",
    }
    monkeypatch.setattr("utils.ats.ai_json", lambda **kwargs: expected)

    result = analyze_resume_text(STRONG_DATA_RESUME, "AI Engineer")

    assert result == expected


def test_resume_analyzer_clamps_invalid_ai_score(monkeypatch) -> None:
    monkeypatch.setattr(
        "utils.ats.ai_json",
        lambda **kwargs: {
            "ats_score": 200,
            "strengths": "bad",
            "weaknesses": [],
            "missing_skills": [],
            "missing_keywords": [],
            "suggestions": [],
            "summary": "",
        },
    )

    result = analyze_resume_text(STRONG_DATA_RESUME, "Data Scientist")

    assert result["ats_score"] == 100
    assert isinstance(result["strengths"], list)
    assert result["summary"]
