import json

from utils import database


def test_profile_round_trip_and_split_list(temp_database) -> None:
    database.save_profile(
        name="Jane Doe",
        email="jane@example.com",
        college="Example University",
        degree="B.Tech",
        branch="CSE",
        graduation_year="2027",
        skills="Python, SQL",
        interests="AI, Data",
        target_career="Data Scientist",
        experience_level="Student",
    )

    profile = database.load_profile()

    assert temp_database.exists()
    assert profile is not None
    assert profile.name == "Jane Doe"
    assert database.profile_as_dict(profile)["target_career"] == "Data Scientist"
    assert database.split_list("Python, SQL\nML") == ["Python", "SQL", "ML"]


def test_resume_analysis_persistence_and_history(temp_database) -> None:
    assert temp_database.exists()
    database.save_resume_analysis(
        filename="resume.pdf",
        resume_text="Python SQL machine learning resume",
        ats_score=82,
        strengths=["Strong skills"],
        weaknesses=["Needs metrics"],
        missing_skills=["Statistics"],
        missing_keywords=["impact"],
        suggestions=["Add measurable outcomes"],
        summary="Solid resume.",
        target_career="Data Scientist",
    )

    latest = database.load_latest_resume_analysis()
    analyses = database.list_resume_analyses()
    uploaded = database.list_uploaded_resumes()
    history = database.list_ats_history()

    assert latest is not None
    assert latest["ats_score"] == 82
    assert latest["strengths"] == ["Strong skills"]
    assert analyses[0]["filename"] == "resume.pdf"
    assert uploaded[0]["text_length"] > 0
    assert history[0]["missing_skill_count"] == 1


def test_recommendations_roadmaps_interviews_settings_and_export(temp_database) -> None:
    assert temp_database.exists()
    recommendations = [
        {
            "title": "AI Engineer",
            "match": 91,
            "required_skills": ["Python"],
            "missing_skills": ["LLMs"],
            "resources": ["DeepLearning.AI"],
        }
    ]
    database.save_career_recommendations(
        skills=["Python"],
        interests=["AI"],
        education="B.Tech",
        target_industry="Artificial Intelligence",
        recommendations=recommendations,
    )
    database.save_roadmap(
        target_career="AI Engineer",
        skills=["Python"],
        roadmap={"30_days": [{"week": "Week 1"}]},
        progress=40,
    )
    database.save_interview_score(
        target_career="AI Engineer",
        question="Explain APIs.",
        answer="APIs connect systems.",
        score=78,
        feedback="Clear answer.",
        suggestions=["Add an example"],
    )
    database.save_setting("theme", "light")
    database.add_activity("Custom activity", "Verified")

    analytics = database.dashboard_analytics()
    exported = database.export_data()

    assert database.list_career_recommendations()[0]["recommendations"] == recommendations
    assert database.list_roadmaps()[0]["roadmap"]["30_days"][0]["week"] == "Week 1"
    assert database.list_interview_scores()[0]["suggestions"] == ["Add an example"]
    assert database.load_setting("theme") == "light"
    assert database.recent_activities()[0]["label"] == "Custom activity"
    assert analytics["counts"]["career_recommendations"] == 1
    assert exported["settings"][0]["key"] == "theme"


def test_fetch_helpers_reset_and_json_fallbacks(temp_database) -> None:
    assert temp_database.exists()
    row_id = database.execute_write(
        "INSERT INTO settings (key, value) VALUES (?, ?)", ("raw", "value")
    )
    assert row_id >= 1
    assert database.fetch_one("SELECT value FROM settings WHERE key = ?", ("raw",)) == {
        "value": "value"
    }
    assert database.fetch_all("SELECT key FROM settings") == [{"key": "raw"}]
    assert database.load_setting("missing", "default") == "default"

    database.execute_write(
        """
        INSERT INTO career_recommendations (
            education, target_industry, skills, interests, recommendations, top_career, top_match
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ("", "", "not json", json.dumps(["AI"]), "not json", "AI Engineer", 50),
    )

    broken = database.list_career_recommendations()[0]

    assert broken["skills"] == []
    assert broken["recommendations"] == []

    database.reset_database()

    assert database.load_profile() is None
    assert database.fetch_one("SELECT COUNT(*) AS count FROM settings") == {"count": 0}
