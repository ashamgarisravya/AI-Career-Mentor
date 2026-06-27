import warnings
from collections.abc import Iterator
from pathlib import Path

import pytest

from utils import database

warnings.simplefilter("ignore", ResourceWarning)


@pytest.fixture
def temp_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    db_path = tmp_path / "app.db"
    connections = []
    original_get_connection = database.get_connection

    def tracked_connection():
        connection = original_get_connection()
        connections.append(connection)
        return connection

    monkeypatch.setattr(database, "DATABASE_PATH", db_path)
    monkeypatch.setattr(database, "get_connection", tracked_connection)
    database.initialize_database()
    yield db_path
    for connection in connections:
        connection.close()


@pytest.fixture(autouse=True)
def clear_ai_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for name in (
        "AI_PROVIDER",
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "OPENAI_MODEL",
        "GEMINI_MODEL",
        "AI_TIMEOUT_SECONDS",
    ):
        monkeypatch.delenv(name, raising=False)
    yield
