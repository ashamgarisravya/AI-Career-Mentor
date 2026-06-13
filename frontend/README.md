# AI Career Builder Frontend

Responsive Next.js 15 frontend for a hackathon AI career coach that helps users discover careers, analyze resumes, identify skill gaps, and generate learning roadmaps.

## Tech Stack

- Next.js 15 App Router
- TypeScript
- Tailwind CSS
- Shadcn UI-style components
- Axios
- React Hook Form
- Zod
- Dark mode with `next-themes`

## Getting Started

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## API

The UI uses mock data by default. Configure a backend with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

The service layer is in `src/services/api.ts`, and app state helpers are in `src/hooks/useCareerBuilder.ts`.

## Pages

- `/` - Home hero, features, CTA
- `/dashboard` - Analytics, career matches, skill gaps
- `/careers` - Career discovery profile form and recommendations
- `/resume` - PDF upload, ATS score, missing skills
- `/skill-gap` - Current skills, missing skills, priority indicators
- `/roadmap` - Monthly roadmap timeline and resources
- `/profile` - User profile management
