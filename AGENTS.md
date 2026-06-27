# AI Career Mentor Agents and Modules

This project uses modular career-advisory components under `utils/`. These modules act as deterministic agents and can optionally use OpenAI or Gemini through `utils/ai.py` when API keys are configured. Every AI-enabled path has a rule-based fallback.

## Resume Analyzer

Primary files:

- `pages/Resume_Analyzer.py`
- `utils/ats.py`
- `utils/pdf_parser.py`
- `utils/database.py`

Responsibilities:

- Validate uploaded PDF resumes.
- Extract PDF text.
- Analyze resume text for ATS readiness.
- Calculate ATS score.
- Identify strengths, weaknesses, missing keywords, and missing skills.
- Save resume metadata and ATS history to SQLite.

Optional AI:

- Uses `utils.ai.ai_json()` for AI-enhanced resume analysis when a provider key is available.
- Falls back to deterministic scoring when AI is unavailable or returns invalid output.

## Career Recommendation

Primary files:

- `pages/Career_Recommendation.py`
- `utils/knowledge.py`
- `utils/database.py`

Responsibilities:

- Combine profile skills, interests, education, industry preference, and resume signals.
- Rank career paths.
- Explain why each role fits.
- Provide salary range, growth outlook, required skills, missing skills, and resources.
- Save recommendation runs to SQLite.

Optional AI:

- Uses provider JSON output to refine recommendation explanations and ranking.
- Falls back to local matching rules.

## Skill Gap Analyzer

Primary files:

- `pages/Skill_Gap.py`
- `utils/knowledge.py`

Responsibilities:

- Compare current skills and resume evidence against a target career.
- Identify missing skills.
- Assign priority, difficulty, estimated learning time, and learning path.

Optional AI:

- Uses optional provider output for richer gap analysis.
- Falls back to local career-skill matching.

## Learning Roadmap Generator

Primary files:

- `pages/Learning_Roadmap.py`
- `utils/roadmap.py`
- `utils/database.py`

Responsibilities:

- Generate 30/60/90 day plans.
- Provide weekly goals, projects, milestones, resources, and skill focus.
- Track milestone progress in Streamlit session state.
- Save roadmap snapshots to SQLite.

Optional AI:

- Uses optional provider output to improve roadmap wording and sequencing.
- Falls back to deterministic roadmap generation.

## Interview Preparation

Primary files:

- `pages/Interview_Prep.py`
- `utils/interview.py`
- `utils/database.py`

Responsibilities:

- Generate HR, technical, behavioral, and coding interview questions.
- Score mock interview answers.
- Provide feedback and improvement suggestions.
- Save interview scores to SQLite.

Optional AI:

- Uses optional provider output for question generation and answer feedback.
- Falls back to rule-based scoring and question templates.

## Resume Builder

Primary files:

- `pages/Resume_Builder.py`
- `utils/resume_builder.py`

Responsibilities:

- Validate personal details, education, skills, experience, projects, and certifications.
- Provide a structured resume preview.
- Generate a professional PDF resume using ReportLab.
- Provide a PDF download.

AI usage:

- Resume Builder is deterministic and does not require external AI.

## Shared Infrastructure

Primary files:

- `utils/ai.py`
- `utils/database.py`
- `utils/production.py`
- `utils/ui.py`
- `utils/charts.py`

Responsibilities:

- Optional OpenAI/Gemini integration.
- SQLite table creation, migrations, query helpers, and analytics.
- Logging, validation, and file checks.
- Reusable Streamlit UI components.
- Plotly chart helpers.
