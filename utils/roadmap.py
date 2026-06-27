"""Learning roadmap generation utilities."""

from __future__ import annotations

import json
from typing import Any

from utils.ai import ai_json
from utils.knowledge import analyze_skill_gap, find_career, missing_skills_for_target


def _focus_skills(skills: list[str], target_career: str) -> list[str]:
    career = find_career(target_career)
    gaps = missing_skills_for_target(skills, career.title)
    return gaps or list(career.required_skills[:4])


def generate_roadmaps(skills: list[str], target_career: str) -> dict[str, list[dict[str, object]]]:
    """Generate 30, 60, and 90 day plans with weekly milestones."""
    career = find_career(target_career)
    focus = _focus_skills(skills, career.title)
    skill_gap_rows = analyze_skill_gap(skills, career.title)
    first = focus[0]
    second = focus[1] if len(focus) > 1 else career.required_skills[1]
    third = focus[2] if len(focus) > 2 else career.required_skills[2]
    fourth = focus[3] if len(focus) > 3 else career.required_skills[3]

    fallback = {
        "30 Days": [
            {
                "week": "Week 1",
                "goal": f"Set up the {career.title} learning workspace and refresh {first}.",
                "project": f"Complete a guided {first} mini lab.",
                "milestone": "Publish notes, setup proof, and one short demo.",
                "resources": career.resources[:2],
                "skills": [first],
            },
            {
                "week": "Week 2",
                "goal": f"Practice {second} through small exercises.",
                "project": f"Build a focused {second} component for the portfolio.",
                "milestone": "Create three evidence bullets for resume use.",
                "resources": career.resources[1:3],
                "skills": [second],
            },
            {
                "week": "Week 3",
                "goal": f"Combine {first} and {second} in a realistic workflow.",
                "project": f"Ship a small {career.title} workflow with README documentation.",
                "milestone": "Document inputs, outputs, tools, and one metric.",
                "resources": career.resources[:3],
                "skills": [first, second],
            },
            {
                "week": "Week 4",
                "goal": "Review gaps, polish the strongest artifact, and update resume bullets.",
                "project": "Portfolio cleanup and resume rewrite sprint.",
                "milestone": "One polished project link and five targeted resume bullets.",
                "resources": ("Resume bullet rewrite practice", "Portfolio review checklist"),
                "skills": focus[:2],
            },
        ],
        "60 Days": [
            {
                "week": "Weeks 5-6",
                "goal": f"Deepen {third} and add testing or validation.",
                "project": f"Build an end-to-end {career.title} project using {third}.",
                "milestone": "First deployable version with clear success criteria.",
                "resources": career.resources,
                "skills": [third],
            },
            {
                "week": "Weeks 7-8",
                "goal": "Turn project work into interview-ready stories.",
                "project": "Case study write-up with problem, approach, tradeoffs, and result.",
                "milestone": "Two STAR stories and one architecture/process diagram.",
                "resources": ("STAR method practice", "Case study examples", "Peer review checklist"),
                "skills": [first, second, third],
            },
        ],
        "90 Days": [
            {
                "week": "Weeks 9-10",
                "goal": f"Add {fourth} and prepare role-specific interview answers.",
                "project": f"Extend the portfolio project with a {fourth} feature.",
                "milestone": "Complete three mock interviews and close the highest priority gap.",
                "resources": ("Technical interview drills", "Mock interview notes", *career.resources[:1]),
                "skills": [fourth],
            },
            {
                "week": "Weeks 11-12",
                "goal": "Apply consistently and refine based on feedback.",
                "project": "Application tracker, targeted outreach, and weekly retrospective.",
                "milestone": "Apply to 20 aligned roles and revise resume from response patterns.",
                "resources": ("LinkedIn profile review", "Target company research", "Application tracker"),
                "skills": [row["Missing Skill"] for row in skill_gap_rows[:3]],
            },
        ],
    }
    prompt = json.dumps(
        {
            "skills": skills,
            "target_career": career.title,
            "skill_gaps": skill_gap_rows,
            "rule_based_roadmap": fallback,
            "required_output": {
                "roadmap": {
                    "30 Days": "list of weekly milestone objects",
                    "60 Days": "list of weekly milestone objects",
                    "90 Days": "list of weekly milestone objects",
                },
                "milestone_object": "week, goal, project, milestone, resources, skills",
            },
        },
        ensure_ascii=True,
    )
    result = ai_json(task="learning roadmap", prompt=prompt, fallback={"roadmap": fallback}, expected_type=dict)
    return _valid_roadmap(result.get("roadmap"), fallback)


def calculate_progress(completed: dict[str, bool], roadmaps: dict[str, list[dict[str, object]]]) -> int:
    """Calculate roadmap completion percentage from checkbox state."""
    total = sum(len(items) for items in roadmaps.values())
    if total == 0:
        return 0
    done = sum(1 for items in roadmaps.values() for item in items if completed.get(str(item["week"])))
    return round((done / total) * 100)


def _valid_roadmap(value: Any, fallback: dict[str, list[dict[str, object]]]) -> dict[str, list[dict[str, object]]]:
    if not isinstance(value, dict):
        return fallback
    valid: dict[str, list[dict[str, object]]] = {}
    for period in ("30 Days", "60 Days", "90 Days"):
        items = value.get(period)
        if not isinstance(items, list):
            valid[period] = fallback[period]
            continue
        valid_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            resources = item.get("resources", [])
            skills = item.get("skills", [])
            valid_items.append(
                {
                    "week": str(item.get("week", "Week")),
                    "goal": str(item.get("goal", "Build role readiness.")),
                    "project": str(item.get("project", "Portfolio project.")),
                    "milestone": str(item.get("milestone", "Complete and document the work.")),
                    "resources": [str(resource) for resource in resources] if isinstance(resources, list) else [str(resources)],
                    "skills": [str(skill) for skill in skills] if isinstance(skills, list) else [str(skills)],
                }
            )
        valid[period] = valid_items or fallback[period]
    return valid
