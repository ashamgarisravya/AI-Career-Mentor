"""SQLite persistence helpers for AI Career Mentor."""

from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


load_dotenv()

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "database/app.db"))


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
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def fetch_one(query: str, parameters: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    """Fetch a single row as a dictionary."""
    initialize_database()
    with get_connection() as connection:
        row = connection.execute(query, parameters).fetchone()
    return None if row is None else dict(row)


def fetch_all(query: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Fetch all rows as dictionaries."""
    initialize_database()
    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [dict(row) for row in rows]


def execute_write(query: str, parameters: tuple[Any, ...] = ()) -> int:
    """Execute a write statement and return the last inserted row id."""
    initialize_database()
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return int(cursor.lastrowid or 0)


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
                resume_id INTEGER,
                filename TEXT NOT NULL DEFAULT '',
                resume_text TEXT NOT NULL DEFAULT '',
                target_career TEXT NOT NULL DEFAULT '',
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
        _ensure_columns(
            connection,
            "resume_analyses",
            {
                "resume_id": "INTEGER",
                "target_career": "TEXT NOT NULL DEFAULT ''",
            },
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS uploaded_resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL DEFAULT '',
                text_length INTEGER NOT NULL DEFAULT 0,
                content_hash TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS ats_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_analysis_id INTEGER,
                ats_score INTEGER NOT NULL DEFAULT 0,
                target_career TEXT NOT NULL DEFAULT '',
                missing_skill_count INTEGER NOT NULL DEFAULT 0,
                missing_keyword_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS career_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                education TEXT NOT NULL DEFAULT '',
                target_industry TEXT NOT NULL DEFAULT '',
                skills TEXT NOT NULL DEFAULT '[]',
                interests TEXT NOT NULL DEFAULT '[]',
                recommendations TEXT NOT NULL DEFAULT '[]',
                top_career TEXT NOT NULL DEFAULT '',
                top_match INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS roadmaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_career TEXT NOT NULL DEFAULT '',
                skills TEXT NOT NULL DEFAULT '[]',
                roadmap TEXT NOT NULL DEFAULT '{}',
                progress INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS interview_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_career TEXT NOT NULL DEFAULT '',
                question TEXT NOT NULL DEFAULT '',
                answer TEXT NOT NULL DEFAULT '',
                score INTEGER NOT NULL DEFAULT 0,
                feedback TEXT NOT NULL DEFAULT '',
                suggestions TEXT NOT NULL DEFAULT '[]',
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
        _create_indexes(connection)
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


def _create_indexes(connection: sqlite3.Connection) -> None:
    """Create indexes used by dashboard/history queries."""
    indexes = (
        "CREATE INDEX IF NOT EXISTS idx_resume_analyses_created ON resume_analyses(created_at DESC, id DESC)",
        "CREATE INDEX IF NOT EXISTS idx_ats_history_created ON ats_history(created_at DESC, id DESC)",
        "CREATE INDEX IF NOT EXISTS idx_recommendations_created ON career_recommendations(created_at DESC, id DESC)",
        "CREATE INDEX IF NOT EXISTS idx_roadmaps_created ON roadmaps(created_at DESC, id DESC)",
        "CREATE INDEX IF NOT EXISTS idx_interview_scores_created ON interview_scores(created_at DESC, id DESC)",
        "CREATE INDEX IF NOT EXISTS idx_activities_created ON activities(created_at DESC, id DESC)",
    )
    for statement in indexes:
        connection.execute(statement)


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True)


def _json_loads(value: str, default: Any) -> Any:
    try:
        return json.loads(value or "")
    except (TypeError, json.JSONDecodeError):
        return default


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
    target_career: str = "",
) -> None:
    """Persist a resume analysis result."""
    initialize_database()
    content_hash = str(abs(hash(resume_text)))
    with get_connection() as connection:
        resume_cursor = connection.execute(
            """
            INSERT INTO uploaded_resumes (filename, text_length, content_hash)
            VALUES (?, ?, ?)
            """,
            (filename, len(resume_text), content_hash),
        )
        resume_id = int(resume_cursor.lastrowid or 0)
        analysis_cursor = connection.execute(
            """
            INSERT INTO resume_analyses (
                resume_id, filename, resume_text, target_career, ats_score, strengths, weaknesses,
                missing_skills, missing_keywords, suggestions, summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resume_id,
                filename,
                resume_text,
                target_career,
                ats_score,
                _json_dumps(strengths),
                _json_dumps(weaknesses),
                _json_dumps(missing_skills),
                _json_dumps(missing_keywords),
                _json_dumps(suggestions),
                summary,
            ),
        )
        analysis_id = int(analysis_cursor.lastrowid or 0)
        connection.execute(
            """
            INSERT INTO ats_history (
                resume_analysis_id, ats_score, target_career,
                missing_skill_count, missing_keyword_count
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (analysis_id, ats_score, target_career, len(missing_skills), len(missing_keywords)),
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
        result[key] = _json_loads(result[key], [])
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


def list_uploaded_resumes(limit: int = 20) -> list[dict[str, Any]]:
    """Return recent uploaded resume metadata."""
    return fetch_all(
        """
        SELECT id, filename, text_length, content_hash, created_at
        FROM uploaded_resumes
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )


def list_ats_history(limit: int = 20) -> list[dict[str, Any]]:
    """Return recent ATS score history."""
    return fetch_all(
        """
        SELECT id, resume_analysis_id, ats_score, target_career,
               missing_skill_count, missing_keyword_count, created_at
        FROM ats_history
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )


def save_career_recommendations(
    *,
    skills: list[str],
    interests: list[str],
    education: str,
    target_industry: str,
    recommendations: list[dict[str, Any]],
) -> None:
    """Persist a career recommendation run."""
    top = recommendations[0] if recommendations else {}
    execute_write(
        """
        INSERT INTO career_recommendations (
            education, target_industry, skills, interests,
            recommendations, top_career, top_match
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            education,
            target_industry,
            _json_dumps(skills),
            _json_dumps(interests),
            _json_dumps(recommendations),
            str(top.get("title", "")),
            int(top.get("match", 0) or 0),
        ),
    )


def list_career_recommendations(limit: int = 10) -> list[dict[str, Any]]:
    """Return recent career recommendation runs."""
    rows = fetch_all(
        """
        SELECT id, education, target_industry, skills, interests,
               recommendations, top_career, top_match, created_at
        FROM career_recommendations
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    for row in rows:
        row["skills"] = _json_loads(row["skills"], [])
        row["interests"] = _json_loads(row["interests"], [])
        row["recommendations"] = _json_loads(row["recommendations"], [])
    return rows


def save_roadmap(
    *,
    target_career: str,
    skills: list[str],
    roadmap: dict[str, list[dict[str, Any]]],
    progress: int = 0,
) -> None:
    """Persist a generated roadmap."""
    execute_write(
        """
        INSERT INTO roadmaps (target_career, skills, roadmap, progress)
        VALUES (?, ?, ?, ?)
        """,
        (target_career, _json_dumps(skills), _json_dumps(roadmap), int(progress)),
    )


def list_roadmaps(limit: int = 10) -> list[dict[str, Any]]:
    """Return recent roadmap runs."""
    rows = fetch_all(
        """
        SELECT id, target_career, skills, roadmap, progress, created_at
        FROM roadmaps
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    for row in rows:
        row["skills"] = _json_loads(row["skills"], [])
        row["roadmap"] = _json_loads(row["roadmap"], {})
    return rows


def save_interview_score(
    *,
    target_career: str,
    question: str,
    answer: str,
    score: int,
    feedback: str,
    suggestions: list[str],
) -> None:
    """Persist an evaluated interview answer."""
    execute_write(
        """
        INSERT INTO interview_scores (
            target_career, question, answer, score, feedback, suggestions
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (target_career, question, answer, int(score), feedback, _json_dumps(suggestions)),
    )


def list_interview_scores(limit: int = 20) -> list[dict[str, Any]]:
    """Return recent interview score history."""
    rows = fetch_all(
        """
        SELECT id, target_career, question, score, feedback, suggestions, created_at
        FROM interview_scores
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    for row in rows:
        row["suggestions"] = _json_loads(row["suggestions"], [])
    return rows


def dashboard_analytics() -> dict[str, Any]:
    """Load optimized dashboard analytics in a small number of aggregate queries."""
    initialize_database()
    with get_connection() as connection:
        counts = {
            "profiles": connection.execute("SELECT COUNT(*) AS count FROM profiles").fetchone()["count"],
            "uploaded_resumes": connection.execute("SELECT COUNT(*) AS count FROM uploaded_resumes").fetchone()["count"],
            "ats_history": connection.execute("SELECT COUNT(*) AS count FROM ats_history").fetchone()["count"],
            "career_recommendations": connection.execute("SELECT COUNT(*) AS count FROM career_recommendations").fetchone()["count"],
            "roadmaps": connection.execute("SELECT COUNT(*) AS count FROM roadmaps").fetchone()["count"],
            "interview_scores": connection.execute("SELECT COUNT(*) AS count FROM interview_scores").fetchone()["count"],
        }
        averages = connection.execute(
            """
            SELECT
                COALESCE(ROUND(AVG(ats_score)), 0) AS avg_ats,
                COALESCE(ROUND((SELECT AVG(top_match) FROM career_recommendations)), 0) AS avg_career_match,
                COALESCE(ROUND((SELECT AVG(progress) FROM roadmaps)), 0) AS avg_learning_progress,
                COALESCE(ROUND((SELECT AVG(score) FROM interview_scores)), 0) AS avg_interview_score
            FROM ats_history
            """
        ).fetchone()
        ats_rows = connection.execute(
            """
            SELECT ats_score, target_career, created_at
            FROM ats_history
            ORDER BY created_at ASC, id ASC
            LIMIT 30
            """
        ).fetchall()
        interview_rows = connection.execute(
            """
            SELECT score, target_career, created_at
            FROM interview_scores
            ORDER BY created_at ASC, id ASC
            LIMIT 30
            """
        ).fetchall()
        recommendation_rows = connection.execute(
            """
            SELECT top_career, top_match, created_at
            FROM career_recommendations
            ORDER BY created_at DESC, id DESC
            LIMIT 10
            """
        ).fetchall()
    return {
        "counts": counts,
        "averages": dict(averages),
        "ats_history": [dict(row) for row in ats_rows],
        "interview_scores": [dict(row) for row in interview_rows],
        "career_recommendations": [dict(row) for row in recommendation_rows],
    }


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
        uploaded_rows = connection.execute("SELECT * FROM uploaded_resumes").fetchall()
        resume_rows = connection.execute("SELECT * FROM resume_analyses").fetchall()
        ats_rows = connection.execute("SELECT * FROM ats_history").fetchall()
        recommendation_rows = connection.execute("SELECT * FROM career_recommendations").fetchall()
        roadmap_rows = connection.execute("SELECT * FROM roadmaps").fetchall()
        interview_rows = connection.execute("SELECT * FROM interview_scores").fetchall()
        activity_rows = connection.execute("SELECT * FROM activities").fetchall()
        setting_rows = connection.execute("SELECT * FROM settings").fetchall()
    return {
        "profiles": [dict(row) for row in profile_rows],
        "uploaded_resumes": [dict(row) for row in uploaded_rows],
        "resume_analyses": [dict(row) for row in resume_rows],
        "ats_history": [dict(row) for row in ats_rows],
        "career_recommendations": [dict(row) for row in recommendation_rows],
        "roadmaps": [dict(row) for row in roadmap_rows],
        "interview_scores": [dict(row) for row in interview_rows],
        "activities": [dict(row) for row in activity_rows],
        "settings": [dict(row) for row in setting_rows],
    }


def reset_database() -> None:
    """Remove all user-created app data while keeping tables available."""
    initialize_database()
    with get_connection() as connection:
        connection.execute("DELETE FROM profiles")
        connection.execute("DELETE FROM uploaded_resumes")
        connection.execute("DELETE FROM resume_analyses")
        connection.execute("DELETE FROM ats_history")
        connection.execute("DELETE FROM career_recommendations")
        connection.execute("DELETE FROM roadmaps")
        connection.execute("DELETE FROM interview_scores")
        connection.execute("DELETE FROM activities")
        connection.execute("DELETE FROM settings")


def profile_as_dict(profile: UserProfile | None) -> dict[str, Any]:
    """Convert a profile object into a plain dictionary."""
    return {} if profile is None else asdict(profile)


def split_list(value: str) -> list[str]:
    """Split comma/newline-separated text into cleaned values."""
    normalized = value.replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]
