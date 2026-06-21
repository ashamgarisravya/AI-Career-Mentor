AI Career Mentor - Fix and Complete the Project

You are working on an existing project.

Stack:

- Frontend: Next.js + TypeScript

- Backend: FastAPI

- Existing folders:
  backend/
  agents/
  models/
  routers/
  services/
  
  frontend/
  src/app
  src/components
  src/hooks
  src/services

Current situation:

- Frontend pages load.
- Backend runs.
- User can open Dashboard, Careers, Resume, Roadmap, Profile.
- However, after entering profile data or uploading resume, the app does not provide meaningful output.
- ATS score remains 0.
- Career recommendations do not change.
- Roadmap does not update.
- Workflow feels disconnected.

Your task is NOT to redesign the UI.

Your task is to make the ENTIRE WORKFLOW FUNCTIONAL.

---

STEP 1: Understand existing code

First inspect:

- app.py
- backend/agents/*
- backend/models/*
- backend/services/*
- backend/routers/*
- frontend/src/services/api.ts
- frontend/src/hooks/*
- frontend/src/app/*

Find broken API calls, missing imports, mismatched response schemas, and incorrect routes.

Fix all of them.

---

STEP 2: Make Profile Dynamic

Profile page must collect:

- name
- education
- degree
- branch
- experience_level
- current_skills
- interests
- preferred_roles

POST this to:

POST /api/profile

Store profile in backend memory for now.

---

STEP 3: Build CareerMentorAgent

Create or improve:

backend/agents/career_mentor.py

Class:

CareerMentorAgent

Methods:

- extract_resume_text(pdf)
- extract_skills(text)
- recommend_careers(profile)
- identify_skill_gaps(profile)
- calculate_ats(text)
- generate_resume_feedback(text)
- generate_roadmap(profile)
- mentor(profile)

The agent must NOT return fixed mock data.

---

STEP 4: Create career knowledge base

Create:

backend/data/careers.json

Include careers:

- Machine Learning Engineer
- Data Scientist
- AI Product Manager
- Software Engineer
- Data Engineer
- Generative AI Engineer

Each career contains:

{
title,
description,
required_skills,
salary_range,
growth_rate,
roadmap
}

recommend_careers() should compare:

profile.skills
vs
required_skills

and return match percentage.

---

STEP 5: Resume Analysis

Resume upload must actually work.

Use:

pypdf

Flow:

Upload PDF

↓

Extract text

↓

Find skills from a master skill list

↓

Calculate ATS score

ATS score based on:

- Contact info
- Education
- Skills
- Projects
- Keywords
- Metrics

Return:

{
ats_score,

strengths:[...],

missing_skills:[...],

suggestions:[...]
}

Suggestions should explain exactly what the user should improve.

---

STEP 6: Skill Gap

Generate:

[
{
skill,
current_level,
target_level,
priority,
resources
}
]

Compare:

User skills

vs

Career required skills

---

STEP 7: Dynamic Roadmap

Generate personalized roadmap.

Example:

Month 1

- Learn NumPy
- Learn Pandas
- Complete mini project

Month 2

- Learn Scikit-learn
- Build ML API

Month 3

- Learn Docker
- Deploy model

Roadmap should depend on:

- profile
- target career
- skill gaps

---

STEP 8: Fix API routes

Verify frontend routes exactly match backend.

Required APIs:

POST /api/profile

POST /api/careers/recommend

POST /api/resume/analyze

GET /api/skills/gaps

GET /api/roadmap

If frontend expects different schemas,
fix frontend.

If backend returns wrong schemas,
fix backend.

---

STEP 9: Remove mock data

Remove:

mockCareer
mockResume
mockSkillGap
mockRoadmap

from:

frontend/src/services/api.ts

Frontend must use backend responses.

---

STEP 10: Dashboard

Dashboard must update automatically.

Show:

Career Fit %

ATS Score

Recommended Careers

Skill Gaps

Roadmap Progress

Resume Suggestions

These values should come from backend APIs.

---

STEP 11: Testing

After all modifications:

1. Run backend

uvicorn app:app --reload

2. Run frontend

cd frontend

npm run dev

3. Verify:

- Profile submission works
- Career recommendations change according to profile
- Resume upload works
- ATS score is not always zero
- Skill gaps change according to profile
- Roadmap changes dynamically
- Dashboard updates

Fix every error until the application is fully functional.

Do not stop after generating code.

Keep debugging until the complete workflow works end-to-end.