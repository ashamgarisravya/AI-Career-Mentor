from fastapi.testclient import TestClient

from app import app


def test_home_returns_backend_status() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "AI Career Mentor Backend Running"}
