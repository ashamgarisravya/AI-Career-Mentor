<<<<<<< HEAD
# AGENTS.md

## Project Overview

AI Career Mentor is an AI-powered career guidance platform that provides personalized recommendations, skill gap analysis, and career roadmaps.

## Agent Responsibilities

### Career Guidance Agent

* Analyzes user interests and goals.
* Recommends suitable career paths.

### Skill Analysis Agent

* Identifies missing skills.
* Suggests learning resources.

### Recommendation Agent

* Generates personalized recommendations.
* Creates career development roadmaps.

## Development Notes

* Backend: Python, FastAPI
* Frontend: HTML, CSS, JavaScript
* AI Integration: Generative AI / LLM

## Repository Structure

* frontend/ : User interface files
* backend/ : API and business logic
* docs/ : Documentation files
=======
# AI Agent Instructions

This repository may be edited by AI coding agents. Agents must protect user work, keep changes focused, and preserve a clean compliance posture.

## Repository Context

- Python backend entry point: `app.py`
- Frontend application: `frontend/`
- Python tool configuration: `pyproject.toml`
- GitLab CI pipeline: `.gitlab-ci.yml`
- Product specifications: `specs/`

## Required Practices

- Read existing files before editing them.
- Do not delete user code unless explicitly requested.
- Keep generated files, dependency folders, secrets, logs, and caches out of Git.
- Update tests and documentation when behavior changes.
- Run or document the relevant quality checks before handing work back.

## Quality Gates

Agents should keep these commands healthy:

```bash
ruff check .
ruff format --check .
mypy .
pytest --cov=. --cov-fail-under=80
bandit -r .
pip-audit
```

## Security Rules

- Never invent or commit real credentials.
- Use `.env.example` for placeholder configuration only.
- Treat dependency and static-analysis findings as actionable until reviewed.

## Spec-Kit

For new features, add or update a specification under `specs/` before implementation when the behavior is non-trivial.
>>>>>>> 7a22386f (chore: add compliance tooling and documentation)
