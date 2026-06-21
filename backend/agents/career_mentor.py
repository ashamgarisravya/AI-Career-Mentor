from __future__ import annotations

import json
import re
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from backend.models.career import (
    CareerRecommendation,
    InterviewPreparation,
    InterviewQuestion,
    LearningResource,
    ResumeAnalysis,
    RoadmapMonth,
    SkillGap,
)
from backend.models.profile import MentorAdvice, ProfileAnalysis, UserProfile


@dataclass(frozen=True)
class CareerBlueprint:
    title: str
    description: str
    required_skills: tuple[str, ...]
    salary_range: str
    growth_rate: str
    roadmap: tuple[str, ...]


class CareerMentorAgent:
    def __init__(self) -> None:
        data_path = Path(__file__).resolve().parents[1] / "data" / "careers.json"
        raw_data = json.loads(data_path.read_text(encoding="utf-8"))
        self._careers = tuple(
            CareerBlueprint(
                title=item["title"],
                description=item["description"],
                required_skills=tuple(item["required_skills"]),
                salary_range=item["salary_range"],
                growth_rate=item["growth_rate"],
                roadmap=tuple(item["roadmap"]),
            )
            for item in raw_data
        )
        self._master_skills = self._build_master_skill_list()

    def extract_resume_text(self, pdf_bytes: bytes) -> str:
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(pdf_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

    def extract_skills(self, text: str) -> list[str]:
        lowered = text.lower()
        extracted = [skill for skill in self._master_skills if skill.lower() in lowered]
        return sorted(dict.fromkeys(extracted))

    def recommend_careers(self, profile: UserProfile) -> list[CareerRecommendation]:
        profile_skills = self._normalized(profile.current_skills)
        resume_skills = self._normalized(self.extract_skills(profile.resume_text))
        interests = self._normalized(profile.interests)
        preferred_roles = self._normalized(profile.preferred_roles)
        combined_skills = profile_skills | resume_skills

        recommendations: list[CareerRecommendation] = []
        for career in self._careers:
            required = self._normalized(list(career.required_skills))
            matched_skills = len(required & combined_skills)
            skill_score = int((matched_skills / max(len(required), 1)) * 65)
            interest_score = min(
                15,
                sum(token in interests for token in self._keywords_for_career(career))
                * 5,
            )
            role_bonus = 20 if career.title.lower() in preferred_roles else 0
            experience_bonus = 5 if profile.experience_level.strip() else 0
            score = max(
                18,
                min(98, skill_score + interest_score + role_bonus + experience_bonus),
            )
            missing = [
                skill
                for skill in career.required_skills
                if skill.lower() not in combined_skills
            ][:3]
            feedback = (
                "You already match several core skills. "
                f"Focus next on {', '.join(missing)}."
                if missing
                else (
                    "You already cover the main skill requirements. "
                    "Push for stronger project evidence."
                )
            )
            recommendations.append(
                CareerRecommendation(
                    id=self._slug(career.title),
                    title=career.title,
                    match_score=score,
                    salary_range=career.salary_range,
                    growth=career.growth_rate,
                    description=career.description,
                    skills=list(career.required_skills),
                    mentor_feedback=feedback,
                )
            )
        return sorted(recommendations, key=lambda item: item.match_score, reverse=True)

    def identify_skill_gaps(self, profile: UserProfile) -> list[SkillGap]:
        target = self._target_career(profile)
        current_skills = self._normalized(profile.current_skills)
        resume_skills = self._normalized(self.extract_skills(profile.resume_text))
        combined_skills = current_skills | resume_skills
        gaps: list[SkillGap] = []

        for skill in target.required_skills:
            current_level = self._skill_level(skill, combined_skills)
            if current_level >= 85:
                continue
            priority = (
                "High"
                if current_level < 45
                else "Medium"
                if current_level < 70
                else "Low"
            )
            gaps.append(
                SkillGap(
                    id=self._slug(skill),
                    skill=skill,
                    current_level=current_level,
                    target_level=90,
                    priority=priority,
                    resources=[
                        f"Learn {skill} through one focused study sprint.",
                        f"Use {skill} in a project tied to {target.title}.",
                        f"Add {skill} outcomes to your resume and portfolio.",
                    ],
                )
            )
        return sorted(gaps, key=lambda item: (item.current_level, item.skill))

    def calculate_ats(self, text: str, profile: UserProfile) -> int:
        lowered = text.lower()
        target = self._target_career(profile)
        keyword_hits = sum(skill.lower() in lowered for skill in target.required_skills)
        contact_score = 10 if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text) else 0
        education_score = 10 if "education" in lowered or profile.education else 0
        skills_score = min(25, keyword_hits * 4)
        project_score = (
            15
            if any(
                token in lowered
                for token in ("project", "built", "developed", "deployed")
            )
            else 0
        )
        metrics_score = 15 if re.search(r"\b\d+%|\b\d+\+|\b\d+x\b", lowered) else 0
        section_score = (
            15 if all(token in lowered for token in ("skills", "education")) else 8
        )
        return max(
            25,
            min(
                98,
                contact_score
                + education_score
                + skills_score
                + project_score
                + metrics_score
                + section_score,
            ),
        )

    def generate_resume_feedback(
        self, text: str, profile: UserProfile
    ) -> ResumeAnalysis:
        extracted_skills = self.extract_skills(text)
        strengths: list[str] = []
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text):
            strengths.append("Contact information is present.")
        if any(
            token in text.lower()
            for token in ("project", "built", "developed", "deployed")
        ):
            strengths.append("Project-oriented language is present.")
        if re.search(r"\b\d+%|\b\d+\+|\b\d+x\b", text.lower()):
            strengths.append("Metrics are included.")
        if extracted_skills:
            strengths.append(
                f"Relevant skills detected: {', '.join(extracted_skills[:5])}."
            )

        target = self._target_career(profile)
        missing_skills = [
            skill
            for skill in target.required_skills
            if skill not in extracted_skills and skill not in profile.current_skills
        ][:5]
        suggestions = []
        if not re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text):
            suggestions.append("Add contact details so the resume is ATS-complete.")
        if "education" not in text.lower():
            suggestions.append(
                "Add an Education section with degree, branch, and institution details."
            )
        if not any(
            token in text.lower()
            for token in ("project", "built", "developed", "deployed")
        ):
            suggestions.append(
                "Add at least one project section with tools used and "
                "outcomes achieved."
            )
        if not re.search(r"\b\d+%|\b\d+\+|\b\d+x\b", text.lower()):
            suggestions.append(
                "Add measurable impact like accuracy, latency, users, "
                "revenue, or time saved."
            )
        suggestions.extend(
            [
                f"Include evidence for {skill} if you have used it, "
                "or build a project that demonstrates it."
                for skill in missing_skills[:3]
            ]
        )

        ats_score = self.calculate_ats(text, profile)
        strongest_signals = (
            ", ".join(strengths[:2]).lower() if strengths else "basic resume structure"
        )
        missing_summary = ", ".join(missing_skills[:2]) or "core target-role skills"
        summary = (
            f"Your ATS score is {ats_score}%. "
            f"The strongest signals are {strongest_signals}. "
            f"To align better with {target.title}, "
            f"improve coverage of {missing_summary}."
        )
        return ResumeAnalysis(
            ats_score=ats_score,
            strengths=strengths or ["Baseline resume content is present."],
            missing_skills=missing_skills,
            suggestions=suggestions
            or [
                "Add clearer skills, projects, and measurable outcomes "
                "for stronger ATS performance."
            ],
            summary=summary,
        )

    def generate_roadmap(self, profile: UserProfile) -> list[RoadmapMonth]:
        target = self._target_career(profile)
        skill_gaps = self.identify_skill_gaps(profile)
        gap_skills = [gap.skill for gap in skill_gaps[:6]]
        roadmap_items = list(target.roadmap)
        month_one_focus = gap_skills[:2] or list(target.required_skills[:2])
        month_two_focus = gap_skills[2:4] or list(target.required_skills[2:4])
        month_three_focus = gap_skills[4:6] or list(target.required_skills[4:6])

        return [
            RoadmapMonth(
                month="Month 1",
                title="Fundamentals and foundation",
                goals=[
                    *(f"Learn {skill}." for skill in month_one_focus),
                    "Complete one mini project that proves your baseline "
                    "understanding.",
                ],
                resources=[
                    LearningResource(
                        title=roadmap_items[0], type="Course", duration="6 hrs"
                    ),
                    LearningResource(
                        title="Mini-project milestone",
                        type="Project",
                        duration="1 week",
                    ),
                ],
            ),
            RoadmapMonth(
                month="Month 2",
                title="Applied projects and implementation",
                goals=[
                    *(
                        f"Practice {skill} in a real implementation."
                        for skill in month_two_focus
                    ),
                    "Build a portfolio-ready project and document the "
                    "architecture and outcomes.",
                ],
                resources=[
                    LearningResource(
                        title=roadmap_items[1], type="Course", duration="8 hrs"
                    ),
                    LearningResource(
                        title=roadmap_items[2], type="Project", duration="1 week"
                    ),
                ],
            ),
            RoadmapMonth(
                month="Month 3",
                title="Deployment and interview readiness",
                goals=[
                    *(
                        f"Close your gap in {skill} with a targeted revision sprint."
                        for skill in month_three_focus
                    ),
                    f"Prepare tailored applications for {target.title} roles.",
                ],
                resources=[
                    LearningResource(
                        title=roadmap_items[-1], type="Practice", duration="5 hrs"
                    ),
                    LearningResource(
                        title="Interview preparation sprint",
                        type="Practice",
                        duration="4 hrs",
                    ),
                ],
            ),
        ]

    def generate_interview_prep(self, profile: UserProfile) -> InterviewPreparation:
        target = self._target_career(profile)
        gaps = self.identify_skill_gaps(profile)
        recommendations = self.recommend_careers(profile)
        target_recommendation = next(
            (item for item in recommendations if item.title == target.title), None
        )
        readiness_score = (
            target_recommendation.match_score if target_recommendation else 0
        )
        strongest_skills = profile.current_skills[:3] or list(
            target.required_skills[:3]
        )
        gap_skills = [gap.skill for gap in gaps[:3]]

        questions = [
            InterviewQuestion(
                question=(
                    f"Walk me through a project that shows you are ready for a "
                    f"{target.title} role."
                ),
                focus_area="Project storytelling",
                answer_tips=[
                    "Use situation, action, result, and metric.",
                    "Name the tools you used, especially "
                    f"{', '.join(strongest_skills)}.",
                    "Close with what you would improve next.",
                ],
            ),
            InterviewQuestion(
                question=(
                    f"How would you approach a new problem that requires "
                    f"{gap_skills[0] if gap_skills else target.required_skills[0]}?"
                ),
                focus_area="Skill gap handling",
                answer_tips=[
                    "State how you would learn the unknown part quickly.",
                    "Break the work into a small prototype and validation step.",
                    "Mention a resource or project you will use to close the gap.",
                ],
            ),
            InterviewQuestion(
                question=(
                    f"Why are you interested in {target.title}, and how does your "
                    "background support that path?"
                ),
                focus_area="Role motivation",
                answer_tips=[
                    "Connect your interests to the role's daily work.",
                    "Use one academic or project example as proof.",
                    "End with the impact you want to create.",
                ],
            ),
        ]

        return InterviewPreparation(
            target_role=target.title,
            readiness_score=readiness_score,
            practice_plan=[
                "Prepare two project stories with measurable outcomes.",
                *(
                    f"Revise {skill} fundamentals and prepare one example answer."
                    for skill in gap_skills[:2]
                ),
                "Run one mock interview and update your resume bullets afterward.",
            ],
            questions=questions,
            tips=[
                "Answer with concrete examples before listing tools.",
                "Keep each response under two minutes during practice.",
                "Tie every answer back to the target role and your next project.",
            ],
        )

    def mentor(self, profile: UserProfile) -> MentorAdvice:
        recommendations = self.recommend_careers(profile)
        target = self._target_career(profile)
        target_recommendation = next(
            (item for item in recommendations if item.title == target.title), None
        )
        gaps = self.identify_skill_gaps(profile)
        strongest_match = recommendations[0].title if recommendations else ""
        strengths = self._profile_strengths(profile, strongest_match)
        weaknesses = [
            f"You need stronger proof in {gap.skill}." for gap in gaps[:3]
        ] or ["Keep building project depth."]
        next_steps = self._next_steps(profile, gaps)
        role = target.title
        strongest = (
            ", ".join(profile.current_skills[:2])
            if profile.current_skills
            else "your existing foundation"
        )
        largest_gap = gaps[0].skill if gaps else "project depth"
        message = (
            f"You are already strong in {strongest}. "
            f"Your biggest gap for becoming a {role} is {largest_gap}. "
            f"{next_steps[0]} {next_steps[1] if len(next_steps) > 1 else ''}".strip()
        )
        return MentorAdvice(
            career_fit=target_recommendation.match_score
            if target_recommendation
            else 0,
            mentor_message=message,
            strengths=strengths,
            weaknesses=weaknesses,
            next_steps=next_steps,
        )

    def analyze_profile(self, profile: UserProfile) -> ProfileAnalysis:
        mentor = self.mentor(profile)
        return ProfileAnalysis(
            readiness_score=mentor.career_fit,
            strengths=mentor.strengths,
            weaknesses=mentor.weaknesses,
            mentor_summary=mentor.mentor_message,
        )

    def _target_career(self, profile: UserProfile) -> CareerBlueprint:
        preferred = self._normalized(profile.preferred_roles)
        for career in self._careers:
            if career.title.lower() in preferred:
                return career
        recommendations = self.recommend_careers(profile)
        top_title = (
            recommendations[0].title if recommendations else self._careers[0].title
        )
        return next(career for career in self._careers if career.title == top_title)

    def _keywords_for_career(self, career: CareerBlueprint) -> set[str]:
        return {
            token.lower()
            for token in re.findall(
                r"[a-zA-Z]+", f"{career.title} {career.description}"
            )
        }

    def _skill_level(self, skill: str, current_skills: set[str]) -> int:
        if skill.lower() in current_skills:
            return 88
        related = {
            "NumPy": {"python", "pandas"},
            "Pandas": {"python", "sql", "numpy"},
            "Scikit-learn": {"python", "machine learning", "statistics"},
            "Machine Learning": {"python", "statistics", "pandas"},
            "Deep Learning": {"machine learning", "python"},
            "FastAPI": {"python", "apis"},
            "Docker": {"deployment", "cloud", "devops"},
            "SQL": {"databases", "analytics"},
            "Statistics": {"math", "analytics"},
            "Visualization": {"dashboard", "analytics"},
            "ETL": {"sql", "python", "data warehousing"},
            "Spark": {"python", "etl"},
            "RAG": {"llms", "vector databases", "apis"},
            "Vector Databases": {"rag", "llms"},
            "Evaluation": {"llms", "machine learning"},
        }
        overlap = len(related.get(skill, set()) & current_skills)
        return 62 if overlap >= 2 else 45 if overlap == 1 else 20

    def _profile_strengths(self, profile: UserProfile, role: str) -> list[str]:
        strengths = []
        if profile.current_skills:
            strengths.append(
                f"You already have skills in {', '.join(profile.current_skills[:4])}."
            )
        if profile.education or profile.degree or profile.branch:
            strengths.append(
                "You have an academic foundation that supports technical career growth."
            )
        if profile.interests:
            strengths.append(
                "Your interests point clearly toward "
                f"{', '.join(profile.interests[:2])}."
            )
        if role:
            strengths.append(f"Your profile currently aligns best with {role}.")
        return strengths or ["You have a workable starting point for career planning."]

    def _next_steps(self, profile: UserProfile, gaps: list[SkillGap]) -> list[str]:
        preferred = (
            profile.preferred_roles[0]
            if profile.preferred_roles
            else self._target_career(profile).title
        )
        steps = [f"Build one targeted project for {preferred} in the next two weeks."]
        if gaps:
            steps.append(f"Learn {gaps[0].skill} and use it in that project.")
        if len(gaps) > 1:
            steps.append(
                f"Close the next gap in {gaps[1].skill} before your "
                "next resume revision."
            )
        steps.append(
            "Update your resume with metrics and apply consistently "
            "over the next 3 months."
        )
        return steps

    def _build_master_skill_list(self) -> list[str]:
        base_skills = {
            "Python",
            "SQL",
            "NumPy",
            "Pandas",
            "Scikit-learn",
            "Machine Learning",
            "Deep Learning",
            "FastAPI",
            "Docker",
            "Statistics",
            "Visualization",
            "Experimentation",
            "Product Strategy",
            "Roadmapping",
            "Analytics",
            "User Research",
            "Prompt Engineering",
            "Communication",
            "Data Structures",
            "Algorithms",
            "Git",
            "APIs",
            "Testing",
            "ETL",
            "Data Warehousing",
            "Spark",
            "Cloud",
            "LLMs",
            "RAG",
            "Vector Databases",
            "Evaluation",
        }
        for career in self._careers:
            base_skills.update(career.required_skills)
        return sorted(base_skills)

    def _normalized(self, values: list[str]) -> set[str]:
        return {value.strip().lower() for value in values if value.strip()}

    def _slug(self, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
