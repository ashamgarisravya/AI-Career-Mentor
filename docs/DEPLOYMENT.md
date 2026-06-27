# Deployment Guide

This guide covers deploying AI Career Mentor as a Streamlit application.

## Production Checklist

Before deploying:

- Install dependencies from `requirements.txt`.
- Create a production `.env` from `.env.example`.
- Confirm API keys are stored as secrets, not committed.
- Confirm `DATABASE_PATH` points to a persistent writable path.
- Confirm `LOG_PATH` points to a writable path.
- Confirm `MAX_PDF_UPLOAD_MB` matches your hosting limits.
- Test all Streamlit pages locally.

## Local Production Run

```bash
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

For a private local run, use:

```bash
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

## Environment Variables

Configure these in the hosting platform:

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

Security notes:

- Never commit `.env`.
- Use platform secrets for API keys.
- Leave API keys blank if rule-based-only mode is desired.

## Streamlit Community Cloud

1. Push the project to a Git repository.
2. Ensure `requirements.txt`, `app.py`, `pages/`, `utils/`, and docs are included.
3. Create the app in Streamlit Community Cloud.
4. Set the main file to `app.py`.
5. Add secrets for optional AI provider keys.
6. Deploy.

SQLite note:

- Streamlit Community Cloud storage can be ephemeral.
- For long-term multi-session persistence, use an external database or persistent volume.

## VM or Server Deployment

1. Install Python.
2. Clone or copy the project.
3. Create a virtual environment.
4. Install requirements.
5. Create `.env`.
6. Run Streamlit with a process manager.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Use a reverse proxy such as Nginx or Caddy for HTTPS and domain routing.

## Database Persistence

The app uses SQLite by default.

Recommended production settings:

```env
DATABASE_PATH=/app/data/app.db
LOG_PATH=/app/logs/app.log
```

Make sure both directories are writable by the app process.

## Backups

Back up:

- SQLite database file from `DATABASE_PATH`
- Any uploaded/generated files if you add persistent file storage later
- Environment configuration, excluding secret values

Simple backup example:

```bash
copy database\app.db backups\app.db
```

## Logging

Application logs are written to `LOG_PATH`, defaulting to:

```text
logs/app.log
```

Use these logs to inspect:

- PDF parsing failures
- Database write failures
- Dashboard analytics failures
- Optional dependency fallback behavior

## Health Checks

After deployment, open these routes:

- `/`
- `/Dashboard`
- `/Profile`
- `/Resume_Analyzer`
- `/Career_Recommendation`
- `/Skill_Gap`
- `/Learning_Roadmap`
- `/Interview_Prep`
- `/Resume_Builder`
- `/Settings`

All pages should load without runtime errors.

## Scaling Notes

The current architecture is best for single-user or small-team deployments.

For larger production use, consider:

- Replacing SQLite with Postgres.
- Adding authentication.
- Moving uploads and generated PDFs to object storage.
- Adding automated tests and CI.
- Adding rate limits for AI provider calls.
