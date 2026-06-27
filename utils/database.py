"""SQLite persistence helpers for AI Career Mentor."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DATABASE_PATH = Path("database") / "app.db"


@dataclass(frozen=True)
class UserProfile:
    """Stored user profile data."""

    id: int
    name: str
    email: str
    college: str
    degree: str
    branch: str
    graduation_year: str
    skills: str
    interests: str
    target_career: str
    experience_level: str
    created_at: str
    updated_at: str


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection and ensure the database directory exists."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create application tables and add missing columns for older local DBs."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                college TEXT NOT NULL DEFAULT '',
                degree TEXT NOT NULL DEFAULT '',
                branch TEXT NOT NULL DEFAULT '',
                graduation_year TEXT NOT NULL DEFAULT '',
                skills TEXT NOT NULL DEFAULT '',
                interests TEXT NOT NULL DEFAULT '',
                target_career TEXT NOT NULL DEFAULT '',
                experience_level TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        _ensure_columns(
            connection,
            "profiles",
            {
                "branch": "TEXT NOT NULL DEFAULT ''",
                "experience_level": "TEXT NOT NULL DEFAULT ''",
            },
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL DEFAULT '',
                resume_text TEXT NOT NULL DEFAULT '',
                ats_score INTEGER NOT NULL DEFAULT 0,
                strengths TEXT NOT NULL DEFAULT '[]',
                weaknesses TEXT NOT NULL DEFAULT '[]',
                missing_skills TEXT NOT NULL DEFAULT '[]',
                missing_keywords TEXT NOT NULL DEFAULT '[]',
                suggestions TEXT NOT NULL DEFAULT '[]',
                summary TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                detail TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _ensure_columns(
    connection: sqlite3.Connection, table_name: str, columns: dict[str, str]
) -> None:
    existing = {
        row["name"]
        for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    for name, definition in columns.items():
        if name not in existing:
            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")


def save_profile(
    *,
    name: str,
    email: str,
    college: str,
    degree: str,
    branch: str,
    graduation_year: str,
    skills: str,
    interests: str,
    target_career: str,
    experience_level: str,
) -> None:
    """Create or update the single active user profile."""
    initialize_database()
    values = {
        "id": 1,
        "name": name.strip(),
        "email": email.strip(),
        "college": college.strip(),
        "degree": degree.strip(),
        "branch": branch.strip(),
        "graduation_year": graduation_year.strip(),
        "skills": skills.strip(),
        "interests": interests.strip(),
        "target_career": target_career.strip(),
        "experience_level": experience_level.strip(),
    }
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO profiles (
                id, name, email, college, degree, branch, graduation_year,
                skills, interests, target_career, experience_level
            )
            VALUES (
                :id, :name, :email, :college, :degree, :branch, :graduation_year,
                :skills, :interests, :target_career, :experience_level
            )
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                email = excluded.email,
                college = excluded.college,
                degree = excluded.degree,
                branch = excluded.branch,
                graduation_year = excluded.graduation_year,
                skills = excluded.skills,
                interests = excluded.interests,
                target_career = excluded.target_career,
                experience_level = excluded.experience_level,
                updated_at = CURRENT_TIMESTAMP
            """,
            values,
        )
    add_activity("Profile saved", f"{values['name']} updated profile details.")


def load_profile() -> UserProfile | None:
    """Load the active user profile, if one has been saved."""
    initialize_database()
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM profiles WHERE id = 1").fetchone()
    if row is None:
        return None
    return UserProfile(**dict(row))


def save_resume_analysis(
    *,
    filename: str,
    resume_text: str,
    ats_score: int,
    strengths: list[str],
    weaknesses: list[str],
    missing_skills: list[str],
    missing_keywords: list[str],
    suggestions: list[str],
    summary: str,
) -> None:
    """Persist a resume analysis result."""
    initialize_database()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO resume_analyses (
                filename, resume_text, ats_score, strengths, weaknesses,
                missing_skills, missing_keywords, suggestions, summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                resume_text,
                ats_score,
                json.dumps(strengths),
                json.dumps(weaknesses),
                json.dumps(missing_skills),
                json.dumps(missing_keywords),
                json.dumps(suggestions),
                summary,
            ),
        )
    add_activity("Resume analyzed", f"{filename or 'Pasted resume'} scored {ats_score}%.")


def load_latest_resume_analysis() -> dict[str, Any] | None:
    """Load the most recent resume analysis."""
    initialize_database()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM resume_analyses ORDER BY created_at DESC, id DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    result = dict(row)
    for key in ("strengths", "weaknesses", "missing_skills", "missing_keywords", "suggestions"):
        result[key] = json.loads(result[key] or "[]")
    return result


def list_resume_analyses(limit: int = 20) -> list[dict[str, Any]]:
    """Return recent resume analyses."""
    initialize_database()
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, filename, ats_score, summary, created_at
            FROM resume_analyses
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def add_activity(label: str, detail: str = "") -> None:
    """Record a recent activity event."""
    initialize_database()
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO activities (label, detail) VALUES (?, ?)",
            (label.strip(), detail.strip()),
        )


def recent_activities(limit: int = 8) -> list[dict[str, str]]:
    """Load recent activity events."""
    initialize_database()
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT label, detail, created_at
            FROM activities
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_setting(key: str, value: str) -> None:
    """Persist a settings value."""
    initialize_database()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
            """,
            (key, value),
        )


def load_setting(key: str, default: str = "") -> str:
    """Load a settings value."""
    initialize_database()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
    return default if row is None else str(row["value"])


def export_data() -> dict[str, Any]:
    """Export application data as serializable dictionaries."""
    initialize_database()
    with get_connection() as connection:
        profile_rows = connection.execute("SELECT * FROM profiles").fetchall()
        resume_rows = connection.execute("SELECT * FROM resume_analyses").fetchall()
        activity_rows = connection.execute("SELECT * FROM activities").fetchall()
        setting_rows = connection.execute("SELECT * FROM settings").fetchall()
    return {
        "profiles": [dict(row) for row in profile_rows],
        "resume_analyses": [dict(row) for row in resume_rows],
        "activities": [dict(row) for row in activity_rows],
        "settings": [dict(row) for row in setting_rows],
    }


def reset_database() -> None:
    """Remove all user-created app data while keeping tables available."""
    initialize_database()
    with get_connection() as connection:
        connection.execute("DELETE FROM profiles")
        connection.execute("DELETE FROM resume_analyses")
        connection.execute("DELETE FROM activities")
        connection.execute("DELETE FROM settings")


def profile_as_dict(profile: UserProfile | None) -> dict[str, Any]:
    """Convert a profile object into a plain dictionary."""
    return {} if profile is None else asdict(profile)


def split_list(value: str) -> list[str]:
    """Split comma/newline-separated text into cleaned values."""
    normalized = value.replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]
