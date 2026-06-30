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
