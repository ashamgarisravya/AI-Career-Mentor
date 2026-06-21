from io import BytesIO

from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from app import app
from backend.agents.career_mentor import CareerMentorAgent
from backend.models.profile import UserProfile
from backend.services.career_service import CareerService

client = TestClient(app)


def sample_profile() -> dict[str, object]:
    return {
        "name": "Sravya",
        "education": "BTech",
        "degree": "BTech",
        "branch": "Computer Science",
        "experience_level": "Beginner",
        "current_skills": ["Python", "SQL", "APIs"],
        "interests": ["AI", "data", "products"],
        "preferred_roles": ["Generative AI Engineer"],
        "resume_text": (
            "Education Skills Python SQL APIs LLMs RAG project built chatbot "
            "with 25% faster responses. email test@example.com"
        ),
    }


def test_health_and_profile_workflow() -> None:
    assert client.get("/").json() == {"message": "AI Career Mentor Backend Running"}

    save_response = client.post("/api/profile", json=sample_profile())
    assert save_response.status_code == 200
    analysis = save_response.json()
    assert analysis["readiness_score"] > 0
    assert analysis["mentor_summary"]

    profile_response = client.get("/api/profile")
    assert profile_response.status_code == 200
    assert profile_response.json()["preferred_roles"] == ["Generative AI Engineer"]


def test_dashboard_recommendations_skill_gaps_and_roadmap() -> None:
    profile = sample_profile()
    career_response = client.post("/api/careers/recommend", json=profile)
    assert career_response.status_code == 200
    careers = career_response.json()
    assert careers[0]["title"] == "Generative AI Engineer"
    assert "matchScore" in careers[0]
    assert "salaryRange" in careers[0]

    gaps_response = client.get("/api/skills/gaps")
    assert gaps_response.status_code == 200
    assert all("targetLevel" in gap for gap in gaps_response.json())

    roadmap_response = client.get("/api/roadmap")
    assert roadmap_response.status_code == 200
    assert len(roadmap_response.json()) == 3

    dashboard_response = client.get("/api/dashboard")
    assert dashboard_response.status_code == 200
    dashboard = dashboard_response.json()
    assert dashboard["topCareers"]
    assert dashboard["skillGaps"] == gaps_response.json()
    assert dashboard["roadmap"] == roadmap_response.json()

    interview_response = client.get("/api/interview/prep")
    assert interview_response.status_code == 200
    interview = interview_response.json()
    assert interview["targetRole"] == "Generative AI Engineer"
    assert interview["readinessScore"] > 0
    assert len(interview["questions"]) == 3
    assert "answerTips" in interview["questions"][0]


def test_resume_text_and_file_upload_analysis() -> None:
    resume_text = (
        "Education Skills Python SQL FastAPI Docker project deployed API "
        "serving 100+ users. test@example.com"
    )
    text_response = client.post(
        "/api/resume/analyze",
        data={"resume_text": resume_text},
    )
    assert text_response.status_code == 200
    text_analysis = text_response.json()
    assert text_analysis["atsScore"] >= 25
    assert "Python" in text_analysis["strengths"][-1]

    file_response = client.post(
        "/api/resume/analyze",
        files={"resume": ("resume.txt", resume_text, "text/plain")},
    )
    assert file_response.status_code == 200
    assert file_response.json()["summary"]

    invalid_pdf_response = client.post(
        "/api/resume/analyze",
        files={"resume": ("resume.pdf", b"not a real pdf", "application/pdf")},
    )
    assert invalid_pdf_response.status_code == 200
    assert invalid_pdf_response.json()["suggestions"]


def test_agent_helpers_cover_default_and_related_skill_paths() -> None:
    agent = CareerMentorAgent()
    blank_profile = UserProfile()
    assert agent.extract_skills("Python, pandas, SQL, and RAG") == [
        "Pandas",
        "Python",
        "RAG",
        "SQL",
    ]

    blank_recommendations = agent.recommend_careers(blank_profile)
    assert blank_recommendations
    assert blank_recommendations[0].match_score >= 18

    related_profile = UserProfile(
        current_skills=["python", "pandas"],
        preferred_roles=["Machine Learning Engineer"],
    )
    gaps = agent.identify_skill_gaps(related_profile)
    numpy_gap = next(gap for gap in gaps if gap.skill == "NumPy")
    assert numpy_gap.current_level == 62
    assert numpy_gap.priority == "Medium"

    resume_feedback = agent.generate_resume_feedback("", blank_profile)
    assert resume_feedback.ats_score == 25
    assert resume_feedback.strengths == ["Baseline resume content is present."]


def test_service_cleans_profile_and_handles_empty_resume() -> None:
    service = CareerService()
    profile = TypeAdapter(UserProfile).validate_python(
        {
            "name": "  Ada  ",
            "education": "  College  ",
            "degree": "  BS  ",
            "branch": "  CS  ",
            "experience_level": "  Entry  ",
            "current_skills": [" Python ", ""],
            "interests": [" AI "],
            "preferred_roles": [" Data Scientist "],
            "resume_text": "  Skills Python project 10%  ",
        }
    )
    service.save_profile(profile)
    cleaned = service.get_profile()
    assert cleaned.name == "Ada"
    assert cleaned.current_skills == ["Python"]
    assert cleaned.preferred_roles == ["Data Scientist"]

    analysis = client.post(
        "/api/resume/analyze",
        files={"resume": ("empty.txt", BytesIO(b""), "text/plain")},
    )
    assert analysis.status_code == 200
