"""Interview preparation helpers."""

from __future__ import annotations

from utils.knowledge import find_career, missing_skills_for_target


def generate_questions(skills: list[str], target_career: str) -> dict[str, list[str]]:
    """Generate interview questions for a target career."""
    career = find_career(target_career)
    gaps = missing_skills_for_target(skills, career.title)
    focus_skill = gaps[0] if gaps else career.required_skills[0]
    return {
        "HR Questions": [
            "Tell me about yourself and your career goals.",
            f"Why are you interested in becoming a {career.title}?",
            "Describe a time you handled a difficult deadline.",
        ],
        "Technical Questions": [
            f"Explain a project where you used {career.required_skills[0]}.",
            f"How would you learn or apply {focus_skill} quickly?",
            f"What are the key responsibilities of a {career.title}?",
        ],
        "Behavioral Questions": [
            "Tell me about a time you received feedback and improved your work.",
            "How do you prioritize tasks when multiple things are urgent?",
            "Describe a project failure and what you learned.",
        ],
        "Coding Questions": [
            "Write logic to clean and summarize a list of records.",
            "Explain time complexity for searching and sorting.",
            "Design a small API or data flow for a career mentor feature.",
        ],
    }


def evaluate_answer(answer: str) -> dict[str, object]:
    """Score a mock interview answer with simple explainable rules."""
    clean = answer.strip()
    word_count = len(clean.split())
    score = 25
    score += 25 if word_count >= 40 else 10 if word_count >= 20 else 0
    score += 20 if any(token in clean.lower() for token in ("project", "example", "built", "created")) else 0
    score += 15 if any(char.isdigit() for char in clean) else 0
    score += 15 if any(token in clean.lower() for token in ("learned", "improved", "result", "impact")) else 0
    score = min(100, score)
    suggestions = []
    if word_count < 40:
        suggestions.append("Add more detail using situation, action, and result.")
    if not any(char.isdigit() for char in clean):
        suggestions.append("Include a measurable result or number.")
    if "project" not in clean.lower():
        suggestions.append("Anchor the answer in a concrete project or example.")
    return {
        "score": score,
        "feedback": "Strong answer structure." if score >= 75 else "Good start; make it more specific.",
        "suggestions": suggestions or ["Keep responses concise and evidence-driven."],
    }
