"""Learning roadmap generation utilities."""

from __future__ import annotations

from utils.knowledge import find_career, missing_skills_for_target


def generate_roadmaps(skills: list[str], target_career: str) -> dict[str, list[dict[str, object]]]:
    """Generate 30, 60, and 90 day roadmaps."""
    career = find_career(target_career)
    gaps = missing_skills_for_target(skills, career.title) or list(career.required_skills[:3])
    return {
        "30 Days": [
            {
                "week": "Week 1",
                "goal": f"Refresh fundamentals for {career.title}.",
                "project": f"Mini project using {gaps[0]}.",
                "milestone": "Publish notes and one small demo.",
                "resources": career.resources[:2],
            },
            {
                "week": "Week 2-4",
                "goal": f"Build practical confidence in {', '.join(gaps[:2])}.",
                "project": "Portfolio-ready feature or notebook.",
                "milestone": "Document outcomes with screenshots and metrics.",
                "resources": career.resources,
            },
        ],
        "60 Days": [
            {
                "week": "Weeks 5-6",
                "goal": "Deepen implementation skills and add testing.",
                "project": f"End-to-end {career.title} project.",
                "milestone": "Complete first deployable version.",
                "resources": career.resources,
            },
            {
                "week": "Weeks 7-8",
                "goal": "Improve portfolio storytelling and resume evidence.",
                "project": "Case study write-up.",
                "milestone": "Resume updated with measurable project bullets.",
                "resources": ("Portfolio review checklist", "Resume bullet rewrite practice"),
            },
        ],
        "90 Days": [
            {
                "week": "Weeks 9-10",
                "goal": "Interview preparation and applied revision.",
                "project": "Mock interview and coding practice set.",
                "milestone": "Complete 3 mock interviews.",
                "resources": ("STAR method practice", "Technical interview drills"),
            },
            {
                "week": "Weeks 11-12",
                "goal": "Apply consistently and refine based on feedback.",
                "project": "Application tracker and targeted outreach.",
                "milestone": "Apply to 20 aligned roles.",
                "resources": ("LinkedIn profile review", "Target company research"),
            },
        ],
    }
