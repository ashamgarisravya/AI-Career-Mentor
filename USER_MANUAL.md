# AI Career Mentor User Manual

AI Career Mentor is a Streamlit application for resume analysis, career recommendations, skill gap analysis, learning roadmaps, interview preparation, and professional resume PDF generation.

## Installation

1. Install Python 3.11 or newer.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment.

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

4. Install dependencies.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Create a local environment file.

Windows:

```bash
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

AI keys are optional. Without keys, the app uses rule-based fallback logic.

## Running Locally

Start the app:

```bash
streamlit run app.py
```

Open the URL printed by Streamlit, usually:

```text
http://localhost:8501
```

If the port is busy:

```bash
streamlit run app.py --server.port 8502
```

## Using the Application

Use the sidebar to navigate between pages:

- Dashboard
- Profile
- Resume Analyzer
- Career Recommendation
- Skill Gap Analysis
- Learning Roadmap
- Interview Preparation
- Resume Builder
- Settings

Start by completing the Profile page. Profile information personalizes resume scoring, recommendations, roadmaps, and interview prompts.

## Uploading Resumes

1. Open Resume Analyzer.
2. Upload a PDF resume or paste resume text.
3. Confirm the target career.
4. Select Analyze Resume.

The app validates PDF type and size, extracts readable text, and generates:

- ATS score
- Resume summary
- Strengths
- Weaknesses
- Missing skills
- Missing keywords
- Actionable suggestions

If a PDF has no extractable text, paste the resume text manually.

## Career Recommendation

Open Career Recommendation to compare profile and resume signals against career paths.

Inputs:

- Skills
- Interests
- Education
- Target industry

Outputs:

- Top career matches
- Match score
- Salary range
- Growth outlook
- Required skills
- Skills to build
- Learning resources

## Skill Gap Analysis

Open Skill Gap Analysis to compare your profile and resume evidence against a target career.

The page shows:

- Missing skills
- Priority
- Difficulty
- Estimated learning time
- Recommended learning path

Use the results to plan the next learning sprint.

## Learning Roadmap

Open Learning Roadmap to generate a 30/60/90 day career plan.

The roadmap includes:

- Weekly milestones
- Suggested projects
- Resources
- Progress checkboxes

Select Refresh Roadmap to save the current roadmap snapshot.

## Interview Preparation

Open Interview Preparation to practice:

- HR questions
- Technical questions
- Behavioral questions
- Coding questions

For mock interview feedback:

1. Select a question.
2. Enter an answer.
3. Select Evaluate Answer.

The app returns a score, feedback, and improvement suggestions.

## Resume Builder

Open Resume Builder to create a professional PDF resume.

Required fields:

- Full name
- Email
- Education
- At least three skills

Optional fields:

- Phone
- Location
- Portfolio, LinkedIn, or GitHub links
- Professional summary
- Experience
- Projects
- Certifications

Use the Preview tab to inspect content and the Validation tab to fix issues before generating the PDF.

## Troubleshooting

`streamlit` command not found:

```bash
python -m streamlit run app.py
```

Dependency installation fails:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

PDF upload fails:

- Confirm the file ends in `.pdf`.
- Confirm the file is not empty.
- Confirm the file is below `MAX_PDF_UPLOAD_MB`.
- Paste resume text manually if extraction fails.

AI output is unavailable:

- Check `.env` for `OPENAI_API_KEY` or `GEMINI_API_KEY`.
- Confirm `AI_PROVIDER` is blank, `openai`, or `gemini`.
- The app automatically uses rule-based fallback when AI is unavailable.

Database issues:

- Confirm the `database/` directory is writable.
- Confirm `DATABASE_PATH` in `.env` points to a writable SQLite path.

Logs:

- Runtime logs are written to `LOG_PATH`, defaulting to `logs/app.log`.
