# User Guide

AI Career Mentor helps learners analyze resumes, identify career paths, close skill gaps, create roadmaps, practice interviews, and generate a professional resume PDF.

## Dashboard

Use Dashboard as the main command center.

It shows:

- ATS Score
- Career Match
- Resume Status
- Learning Progress
- Interview Readiness
- Recent Activity
- Plotly analytics for ATS history, interview scores, recommendation runs, and database coverage

If the dashboard asks for setup, create a Profile first.

## Profile

Use Profile to save learner context.

Recommended fields:

- Name
- Email
- College
- Degree
- Branch
- Graduation year
- Skills
- Interests
- Target career
- Experience level

This information powers personalized recommendations, resume analysis, roadmap generation, and interview preparation.

## Resume Analyzer

Use Resume Analyzer to score a resume against a target career.

Steps:

1. Upload a PDF resume, or paste resume text.
2. Confirm or enter the target career.
3. Select Analyze Resume.
4. Review ATS score, strengths, weaknesses, missing skills, missing keywords, and suggestions.

Validation:

- PDF files must use `.pdf`.
- Empty PDFs are rejected.
- Files above `MAX_PDF_UPLOAD_MB` are rejected.
- If PDF text cannot be extracted, paste text manually.

## Career Recommendation

Use Career Recommendation to compare profile and resume signals against career paths.

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
- Missing skills
- Why the role fits
- Learning resources

Recommendation runs are saved to history for Dashboard analytics.

## Skill Gap Analysis

Use Skill Gap Analysis to compare current skills and resume evidence against a selected target career.

Outputs:

- Missing skills
- Priority
- Difficulty
- Estimated learning time
- Recommended learning path

Use these results to decide what to learn next.

## Learning Roadmap

Use Learning Roadmap to generate a 30/60/90 day plan.

Each roadmap includes:

- Weekly goals
- Suggested projects
- Milestones
- Resources
- Progress checkboxes

Select Refresh Roadmap to save a roadmap snapshot for analytics.

## Interview Preparation

Use Interview Preparation to practice:

- HR questions
- Technical questions
- Behavioral questions
- Coding questions

Mock interview flow:

1. Choose a question.
2. Write an answer.
3. Select Evaluate Answer.
4. Review score, feedback, and improvement suggestions.

Interview scores are saved to history.

## Resume Builder

Use Resume Builder to create a professional PDF resume.

Required inputs:

- Full name
- Email
- Education
- At least three skills

Optional inputs:

- Phone
- Location
- Portfolio, LinkedIn, or GitHub links
- Professional summary
- Experience
- Projects
- Certifications

The page provides:

- Completeness score
- Validation results
- Resume preview
- ReportLab PDF generation
- Download button

## Settings

Use Settings to:

- Save theme preference
- Store an API key label
- View AI mode status
- Export local app data as JSON
- Reset the local database

Reset permanently clears local app data.

## AI Behavior

AI integration is optional.

If OpenAI or Gemini is configured, the app attempts AI-enhanced output for:

- Resume analysis
- Career recommendations
- Skill gaps
- Roadmaps
- Interview questions
- Interview feedback

If no key is configured, if the provider times out, or if the provider returns invalid output, the app automatically uses deterministic rule-based fallback logic.
