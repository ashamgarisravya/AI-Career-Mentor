You are a senior full-stack AI engineer.

Upgrade my existing project "AI Career Mentor" from a rule-based demo into a dynamic AI career coaching platform.

IMPORTANT RULES

1. DO NOT modify:
   - .gitlab-ci.yml
   - Dockerfile
   - README.md
   - CONTRIBUTING.md
   - .pre-commit-config.yaml
   - specs/
   - tests/ unless new tests are required

2. ONLY modify:
   - backend/
   - frontend/src/
   - app.py
   - requirements.txt

3. Preserve existing UI styling and pages.

4. Do NOT break the existing frontend routes.

--------------------------------------------------

CURRENT PROJECT STRUCTURE

Backend:
- FastAPI
- app.py
- backend/agents/career_mentor.py
- backend/services/career_service.py
- backend/models/
- backend/routers/

Frontend:
- Next.js App Router
- frontend/src/app/
- frontend/src/services/api.ts
- frontend/src/hooks/useCareerBuilder.ts

Currently:

career_service.py contains:

self._profile = UserProfile(
    name="Sravya",
    education="Computer Science Student",
    cgpa=8.2,
    current_role="Student Developer",
    target_role="Machine Learning Engineer",
    skills=["Python","SQL","React","APIs"],
    interests=["AI products","data","automation"],
    projects=["AI career mentor frontend"]
)

This MUST be removed.

--------------------------------------------------

GOAL

Transform this project into an AI Career Coach.

User should:

1. Create profile
2. Upload resume
3. Get personalized career recommendations
4. Get skill gap analysis
5. Get ATS score
6. Get 3 month roadmap
7. Get mentor advice
8. View everything on dashboard

--------------------------------------------------

BACKEND REQUIREMENTS

Create proper APIs.

1.

POST /profile

Input:

{
  "name":"",
  "education":"",
  "cgpa":0,
  "current_role":"",
  "target_role":"",
  "skills":[],
  "interests":[],
  "projects":[]
}

Save profile in memory for now.

Return:

{
  "readiness_score":0,
  "strengths":[],
  "weaknesses":[],
  "mentor_summary":""
}

--------------------------------------------------

2.

GET /profile

Return current profile.

--------------------------------------------------

3.

POST /careers/recommend

Accept profile.

Return:

[
 {
   "title":"",
   "match_score":0,
   "salary_range":"",
   "growth":"",
   "description":"",
   "skills":[],
   "mentor_feedback":""
 }
]

Recommendation MUST depend on:

- skills
- interests
- projects
- target_role

--------------------------------------------------

4.

POST /resume/analyze

Accept PDF or text.

Extract text using pypdf.

Return:

{
 "ats_score":0,
 "summary":"",
 "strengths":[],
 "missing_skills":[],
 "suggestions":[]
}

--------------------------------------------------

5.

GET /skills/gaps

Return dynamic skill gaps.

Skill gaps should depend on:

- target role
- current skills
- projects
- resume

--------------------------------------------------

6.

GET /roadmap

Return:

[
 {
   "month":"",
   "title":"",
   "goals":[],
   "resources":[]
 }
]

Generate roadmap dynamically.

--------------------------------------------------

7.

NEW API

GET /dashboard

Return:

{
  "career_fit":0,

  "mentor_summary":"",

  "ats_score":0,

  "top_careers":[],

  "skill_gaps":[],

  "roadmap":[],

  "strengths":[],

  "weaknesses":[],

  "next_steps":[]
}

--------------------------------------------------

AGENT REQUIREMENTS

Upgrade CareerMentorAgent.

Current methods:

- analyze_profile()
- recommend_careers()
- identify_skill_gaps()
- generate_learning_roadmap()
- analyze_resume()

ADD:

mentor_user(profile)

Return:

{
 "career_fit":0,

 "mentor_message":"",

 "strengths":[],

 "weaknesses":[],

 "next_steps":[]
}

Mentor message should sound like:

"You are already strong in Python and SQL.

Your biggest gap for becoming an ML Engineer is MLOps and deployment.

Build two projects.

Learn Docker.

Apply in 3 months."

--------------------------------------------------

CAREER RECOMMENDATION ENGINE

Expand ROLE_BLUEPRINTS.

Include:

1. Machine Learning Engineer

2. Data Scientist

3. AI Product Manager

4. Full Stack AI Developer

5. Frontend Engineer

6. Backend Engineer

7. Data Engineer

8. DevOps Engineer

9. Software Engineer

10. Product Manager

Each role should include:

- skills
- salary range
- growth
- description
- keywords

Match score should depend on:

- skill overlap
- interest overlap
- project keywords
- target role match
- cgpa bonus

--------------------------------------------------

FRONTEND REQUIREMENTS

Remove dependency on mock data.

frontend/src/services/api.ts

If backend exists:

ALWAYS call backend APIs.

Only use mocks if backend unavailable.

--------------------------------------------------

PROFILE PAGE

Allow user to enter:

- name
- education
- cgpa
- current role
- target role
- skills
- interests
- projects

On submit:

POST /profile

Store result.

--------------------------------------------------

CAREERS PAGE

Generate careers dynamically.

Display:

- match score
- salary
- growth
- mentor feedback

--------------------------------------------------

RESUME PAGE

Allow PDF upload.

Call:

POST /resume/analyze

Display:

- ATS score
- strengths
- missing skills
- suggestions

--------------------------------------------------

ROADMAP PAGE

Call:

GET /roadmap

Display:

Month 1

Month 2

Month 3

Goals

Resources

--------------------------------------------------

DASHBOARD PAGE

Create unified dashboard.

Show:

Career Fit %

ATS Score

Top Careers

Skill Gaps

Roadmap

Strengths

Weaknesses

AI Mentor Advice

Next Steps

--------------------------------------------------

ARCHITECTURE REQUIREMENT

Keep architecture ready for LLM integration.

Create clear separation:

backend/

agents/
    career_mentor.py

services/
    career_service.py

models/

routers/

Later I should be able to replace:

CareerMentorAgent

with

GPT / Gemini / Llama

without changing frontend.

--------------------------------------------------

OUTPUT FORMAT

1. Explain planned changes first.

2. Then modify files.

3. Show diff for every file.

4. After coding:

- show folder structure
- show APIs created
- show frontend pages updated
- show commands to run

5. Ensure project runs with:

Backend:

uvicorn app:app --reload

Frontend:

npm run dev

6. Verify all APIs return valid JSON.

Begin implementation now.