<<<<<<< HEAD
# AI Career Mentor - User Manual

## Overview

AI Career Mentor is an AI-powered platform that helps users explore career paths, identify skill gaps, and receive personalized career recommendations.

## Features

* Career recommendations
* Skill gap analysis
* Personalized learning suggestions
* Career roadmap generation

## How to Use

1. Launch the application.
2. Enter your interests, skills, and career goals.
3. Submit your information.
4. Review the AI-generated recommendations.
5. Explore suggested skills and learning paths.

## Intended Users

* Students
* Graduates
* Job Seekers
* Career Changers

## Support

For issues or feedback, please create an issue in the repository.
=======
# User Manual

AI Career Mentor helps users explore career paths, review resumes, identify skill gaps, and plan learning roadmaps.

## Running the Backend

Install dependencies and start the FastAPI app:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://localhost:8000` to confirm the backend is running. The root endpoint returns a JSON health message.

## Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in a browser.

## Main Workflows

- Use the dashboard to view career guidance summaries.
- Use the resume page to upload or review resume-related information.
- Use the skill-gap page to compare existing skills with target roles.
- Use the roadmap page to view learning milestones.
- Use the profile page to manage user context.

## Configuration

Copy `.env.example` to `.env` and adjust values for your local environment. Do not commit `.env`.

## Troubleshooting

- If the backend does not start, confirm Python dependencies are installed.
- If the frontend cannot reach the backend, confirm `NEXT_PUBLIC_API_URL` points to the expected API URL.
- If quality checks fail, run the reported formatter or linter locally and commit the resulting changes.
>>>>>>> 7a22386f (chore: add compliance tooling and documentation)
