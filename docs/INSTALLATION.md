# Installation Guide

This guide installs AI Career Mentor locally for development or personal use.

## Prerequisites

- Python 3.11 or newer.
- PowerShell, Command Prompt, Terminal, or another shell.
- Git, if cloning from a repository.
- Optional OpenAI or Gemini API key for AI-enhanced output.

## 1. Open the Project

```bash
cd "C:\Users\Sravya\Downloads\Ai career mentor"
```

Use your own checkout path if the project is elsewhere.

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Pinned dependencies include Streamlit, pandas, Plotly, PyPDF2, ReportLab, python-dotenv, and streamlit-option-menu.

## 4. Configure Environment

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Edit `.env`:

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

API keys are optional. The app works without them by using rule-based fallbacks.

## 5. Run the App

```bash
streamlit run app.py
```

Open the displayed local URL.

If the default port is busy:

```bash
streamlit run app.py --server.port 8502
```

## 6. Verify Installation

Check these pages from the sidebar:

- Dashboard
- Profile
- Resume Analyzer
- Career Recommendation
- Skill Gap Analysis
- Learning Roadmap
- Interview Preparation
- Resume Builder
- Settings

The SQLite database is created automatically at `database/app.db`.

## Troubleshooting

`streamlit` command not found:

```bash
python -m streamlit run app.py
```

Dependency install fails:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

PDF extraction returns empty text:

- Confirm the PDF contains selectable text.
- Paste resume text manually into Resume Analyzer.

AI output does not appear:

- Confirm `.env` contains a valid `OPENAI_API_KEY` or `GEMINI_API_KEY`.
- Confirm `AI_PROVIDER` is blank, `openai`, or `gemini`.
- The app automatically falls back to rule-based output on API errors.
