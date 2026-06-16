# AI Agent Instructions

This repository may be edited by AI coding agents. Agents must protect user work, keep changes focused, and preserve a clean compliance posture.

## Project Overview

AI Career Mentor is an AI-powered career guidance platform that provides personalized recommendations, skill-gap analysis, and career roadmaps.

## Repository Context

- Python backend entry point: `app.py`
- Frontend application: `frontend/`
- Python tool configuration: `pyproject.toml`
- GitLab CI pipeline: `.gitlab-ci.yml`
- Product specifications: `specs/`

## Agent Responsibilities

### Career Guidance Agent

- Analyzes user interests and goals.
- Recommends suitable career paths.

### Skill Analysis Agent

- Identifies missing skills.
- Suggests learning resources.

### Recommendation Agent

- Generates personalized recommendations.
- Creates career development roadmaps.

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
bandit -c pyproject.toml -r .
pip-audit
```

## Security Rules

- Never invent or commit real credentials.
- Use `.env.example` for placeholder configuration only.
- Treat dependency and static-analysis findings as actionable until reviewed.

## Spec-Kit

For new features, add or update a specification under `specs/` before implementation when the behavior is non-trivial.
