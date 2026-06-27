# AI Career Mentor

AI Career Mentor is a Python + Streamlit career guidance application. It stores user data locally in SQLite and provides profile management, dashboard analytics, resume analysis, career recommendations, skill gap analysis, learning roadmaps, interview preparation, resume PDF generation, and settings/export tools.

## Features

- Professional Streamlit dashboard
- SQLite-backed profile storage
- Rule-based resume ATS analysis with optional AI key detection
- Career recommendations and skill gap analysis
- 30/60/90 day learning roadmap
- Mock interview scoring
- Professional PDF resume builder
- JSON export and database reset

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Environment

Copy `.env.example` to `.env` and add optional API keys if you want to extend AI provider calls:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
DATABASE_PATH=database/app.db
```

The app works without API keys by using deterministic rule-based analysis.

## Structure

```text
app.py
pages/
utils/
database/
generated/
assets/
```
