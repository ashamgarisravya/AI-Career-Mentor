# AI Career Mentor

AI Career Mentor is a full-stack career guidance project with a Python FastAPI backend and a Next.js frontend. The backend exposes an API foundation for career coaching workflows, while the frontend provides pages for career discovery, resume review, skill-gap analysis, roadmap planning, and interview preparation.

## Features

- FastAPI backend entry point in `app.py`.
- Next.js frontend in `frontend/`.
- Functional API routes for profile, dashboard, career recommendations, resume analysis, skill gaps, roadmaps, and interview preparation.
- Python quality tooling for linting, formatting, typing, testing, coverage, and security checks.
- GitLab CI pipeline with visible lint, format, type-check, test, coverage, and security jobs.
- Spec-Kit structure for documenting product requirements before implementation.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer for the frontend
- Git

## Backend Setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app:app --reload
```

The backend runs at `http://localhost:8000`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:3000`.

## Quality Checks

```bash
pytest --cov=. --cov-fail-under=80
ruff check .
ruff format --check .
mypy .
bandit -r .
pip-audit
```

Install pre-commit hooks with:

```bash
pre-commit install
```

## Documentation

- `USER_MANUAL.md` explains how to run and use the project.
- `CONTRIBUTING.md` explains the development workflow.
- `AGENTS.md` documents guidance for AI coding agents.
- `SECURITY.md` explains vulnerability reporting.
- `specs/example-feature/spec.md` provides an example product specification.

## License

This project is licensed under the GNU Affero General Public License v3.0 only. See `LICENSE` for the full AGPLv3 license text.
