# AI Career Mentor

AI Career Mentor is a professional Streamlit SaaS-style application for career planning, resume intelligence, learning roadmaps, and interview preparation. It stores user data locally in SQLite, supports optional OpenAI or Gemini enrichment, and automatically falls back to deterministic rule-based logic when no API key is configured.

## Features

- Dashboard with ATS score, career match, resume status, learning progress, interview readiness, recent activity, and Plotly analytics.
- Profile management for learner details, education, skills, interests, and target career.
- Resume Analyzer with PDF upload, text extraction, ATS scoring, strengths, weaknesses, missing keywords, missing skills, and actionable suggestions.
- Career Recommendation using profile and resume signals, salary range, growth outlook, required skills, and learning resources.
- Skill Gap Analysis comparing current evidence against a selected target career.
- Learning Roadmap with 30/60/90 day plans, weekly milestones, project work, resources, and progress tracking.
- Interview Preparation with HR, technical, behavioral, and coding prompts plus answer scoring and feedback.
- Professional Resume Builder with validation, preview, ReportLab PDF generation, and download.
- SQLite-backed history for resumes, ATS runs, recommendations, roadmaps, interview scores, activities, and settings.
- Optional Gemini or OpenAI integration via environment variables.
- Production hardening with validation, loading spinners, empty states, graceful errors, and file-backed logging.

## Architecture

AI Career Mentor is a single-process Python Streamlit application.

```text
Browser
  |
  v
Streamlit app.py
  |
  +-- pages/                  # Product pages
  +-- utils/                  # Business logic, AI, database, UI helpers
  +-- database/app.db         # Local SQLite database
  +-- logs/app.log            # Runtime application log
```

Key design points:

- `app.py` configures the main Streamlit app and shared sidebar navigation.
- `pages/` contains Streamlit page modules.
- `utils/database.py` owns SQLite schema creation, query helpers, persistence, and dashboard analytics.
- `utils/ai.py` provides optional OpenAI/Gemini JSON calls with automatic fallback.
- `utils/ats.py`, `utils/knowledge.py`, `utils/roadmap.py`, and `utils/interview.py` contain career-domain logic.
- `utils/resume_builder.py` generates professional PDF resumes with ReportLab.
- `utils/ui.py` provides reusable UI styling and components.
- `utils/production.py` centralizes logging and validation helpers.

## Folder Structure

```text
AI Career Mentor/
|-- app.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- USER_MANUAL.md
|-- AGENTS.md
|-- SECURITY.md
|-- Dockerfile
|-- docs/
|   |-- INSTALLATION.md
|   |-- USER_GUIDE.md
|   `-- DEPLOYMENT.md
|-- pages/
|   |-- Dashboard.py
|   |-- Profile.py
|   |-- Resume_Analyzer.py
|   |-- Career_Recommendation.py
|   |-- Skill_Gap.py
|   |-- Learning_Roadmap.py
|   |-- Interview_Prep.py
|   |-- Resume_Builder.py
|   `-- Settings.py
|-- utils/
|   |-- ai.py
|   |-- ats.py
|   |-- charts.py
|   |-- database.py
|   |-- interview.py
|   |-- knowledge.py
|   |-- pdf_parser.py
|   |-- production.py
|   |-- resume_builder.py
|   |-- roadmap.py
|   `-- ui.py
|-- database/
|-- generated/
|-- logs/
`-- assets/
```

## Installation

See the detailed [Installation Guide](docs/INSTALLATION.md).

Quick setup:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

On macOS/Linux, activate with:

```bash
source .venv/bin/activate
```

## Environment Variables

Copy `.env.example` to `.env` and edit values as needed.

```env
AI_PROVIDER=
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
GEMINI_MODEL=gemini-1.5-flash
AI_TIMEOUT_SECONDS=12
DATABASE_PATH=database/app.db
LOG_PATH=logs/app.log
MAX_PDF_UPLOAD_MB=8
```

Notes:

- API keys are optional. Without keys, the app uses rule-based local logic.
- `AI_PROVIDER` can be `openai`, `gemini`, or blank for automatic detection.
- Never commit a real `.env` file or real API keys.

## Running the Project

```bash
streamlit run app.py
```

Then open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

If port `8501` is busy:

```bash
streamlit run app.py --server.port 8502
```

## Development Tooling

Install development tools:

```bash
python -m pip install -r requirements-dev.txt
```

Install Git hooks:

```bash
python -m pre_commit install
```

Run code quality checks:

```bash
python -m ruff check app.py pages utils
python -m mypy app.py pages utils
python -m flake8 app.py pages utils
python -m pylint app.py pages utils
python -m bandit -c pyproject.toml -r app.py pages utils
python -m vulture app.py pages utils vulture_whitelist.py --min-confidence 100
$files = @("app.py") + (Get-ChildItem pages,utils -Filter *.py | ForEach-Object { $_.FullName })
python -m pyupgrade --py311-plus @files
```

Run formatting and repository automation checks:

```bash
python -m black --check app.py pages utils tests
python -m pytest
python -m pip_audit --disable-pip --no-deps --cache-dir .pip-audit-cache --ignore-vuln PYSEC-2026-212 --ignore-vuln CVE-2026-33682 -r requirements.txt -r requirements-dev.txt
python -m pre_commit run --all-files
```

Pytest is configured in `pytest.ini`, and coverage.py is configured in `.coveragerc` with an 80% fail-under threshold for the tested business modules. The default `python -m pytest` command prints missing coverage lines and writes `coverage.xml`.

Run the optional Streamlit page smoke test when you want runtime page coverage:

```bash
python -m pytest -m "integration" --no-cov
```

The repository also includes GitHub Actions workflows for Ruff, Mypy, Bandit, pip-audit, Gitleaks secret scanning, test coverage artifact upload, and changelog generation from tags using git-cliff.

The pip-audit command ignores two Streamlit advisories while the application is intentionally pinned to Streamlit `1.41.1` for compatibility. Remove the `--ignore-vuln` flags when the project is approved to upgrade Streamlit.

## Screenshots

Add screenshots to `assets/screenshots/` and update these placeholders.

```text
assets/screenshots/dashboard.png
assets/screenshots/resume-analyzer.png
assets/screenshots/career-recommendation.png
assets/screenshots/learning-roadmap.png
assets/screenshots/resume-builder.png
```

Suggested README embeds:

```md
![Dashboard](assets/screenshots/dashboard.png)
![Resume Analyzer](assets/screenshots/resume-analyzer.png)
![Career Recommendation](assets/screenshots/career-recommendation.png)
![Learning Roadmap](assets/screenshots/learning-roadmap.png)
![Resume Builder](assets/screenshots/resume-builder.png)
```

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [User Manual](USER_MANUAL.md)
- [Agents and Modules](AGENTS.md)
- [Security Policy](SECURITY.md)

## Future Scope

- Multi-user authentication and role-based access.
- Cloud database support for Postgres or managed SQLite.
- Resume template selection and DOCX export.
- More AI providers and configurable prompt templates.
- Admin analytics dashboard.
- Cloud object storage for uploaded resumes and generated PDFs.
- Test suite with CI checks for Streamlit pages and utility modules.

## License

See [LICENSE](LICENSE).
