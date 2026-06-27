"""Interview preparation helpers."""

from __future__ import annotations

import json
import re
from typing import Any

from utils.ai import ai_json
from utils.knowledge import find_career, missing_skills_for_target


def generate_questions(skills: list[str], target_career: str) -> dict[str, list[str]]:
    """Generate HR, technical, behavioral, and coding questions."""
    career = find_career(target_career)
    gaps = missing_skills_for_target(skills, career.title)
    focus_skill = gaps[0] if gaps else career.required_skills[0]
    second_skill = gaps[1] if len(gaps) > 1 else career.required_skills[1]
    fallback = {
        "HR Questions": [
            "Tell me about yourself and the direction you want your career to take.",
            f"Why are you interested in becoming a {career.title}?",
            "What achievement are you most proud of, and what did you learn from it?",
            "How do you choose what to learn next when preparing for a role?",
        ],
        "Technical Questions": [
            f"Explain a project where you used {career.required_skills[0]} and the tradeoffs you made.",
            f"How would you learn and apply {focus_skill} in a four-week sprint?",
            f"What are the key responsibilities of a {career.title} in a production team?",
            f"How would you debug a problem involving {second_skill}?",
        ],
        "Behavioral Questions": [
            "Tell me about a time you received critical feedback and changed your approach.",
            "Describe a deadline conflict and how you prioritized the work.",
            "Tell me about a project failure, the root cause, and what you changed afterward.",
            "Describe a time you explained a technical idea to a non-technical person.",
        ],
        "Coding Questions": [
            "Write logic to clean, validate, and summarize a list of records.",
            "Explain the time complexity of searching, sorting, and grouping data.",
            "Design a small API or data flow for a career mentor feature.",
            f"Sketch pseudocode for a {career.title} project that uses {focus_skill}.",
        ],
    }
    prompt = json.dumps(
        {
            "skills": skills,
            "target_career": career.title,
            "missing_skills": gaps,
            "rule_based_questions": fallback,
            "required_output": {
                "questions": {
                    "HR Questions": "list of strings",
                    "Technical Questions": "list of strings",
                    "Behavioral Questions": "list of strings",
                    "Coding Questions": "list of strings",
                }
            },
        },
        ensure_ascii=True,
    )
    result = ai_json(
        task="interview questions",
        prompt=prompt,
        fallback={"questions": fallback},
        expected_type=dict,
    )
    return _valid_questions(result.get("questions"), fallback)


def evaluate_answer(answer: str, question: str = "", target_career: str = "") -> dict[str, Any]:
    """Score a mock interview answer with explainable feedback."""
    clean = answer.strip()
    lowered = clean.lower()
    words = re.findall(r"[a-zA-Z][a-zA-Z'-]+", clean)
    word_count = len(words)
    has_example = any(
        token in lowered
        for token in ("for example", "project", "built", "created", "worked on", "implemented")
    )
    has_result = any(
        token in lowered
        for token in ("result", "impact", "improved", "reduced", "increased", "learned")
    )
    has_metric = bool(
        re.search(r"\b\d+(?:\.\d+)?\s*(?:%|x|users|hours|days|projects|models)?\b", clean)
    )
    has_structure = any(
        token in lowered
        for token in ("situation", "task", "action", "result", "first", "then", "finally")
    )
    role_terms = (
        [term.lower() for term in find_career(target_career).required_skills]
        if target_career
        else []
    )
    role_hits = sum(1 for term in role_terms if term in lowered)

    score = 20
    score += 20 if word_count >= 70 else 14 if word_count >= 40 else 7 if word_count >= 20 else 0
    score += 18 if has_example else 0
    score += 18 if has_result else 0
    score += 14 if has_metric else 0
    score += 12 if has_structure else 0
    score += min(12, role_hits * 4)
    score = min(100, score)

    suggestions = []
    if word_count < 40:
        suggestions.append("Add enough detail to cover situation, action, and result.")
    if not has_example:
        suggestions.append(
            "Anchor the answer in a specific project, internship, coursework, or team example."
        )
    if not has_result:
        suggestions.append("Explain the outcome and what changed because of your work.")
    if not has_metric:
        suggestions.append(
            "Include a number such as accuracy, time saved, users, defects reduced, or scope delivered."
        )
    if target_career and role_hits == 0:
        suggestions.append(f"Connect the answer to {target_career} skills or responsibilities.")

    if score >= 80:
        feedback = "Strong answer with clear evidence, outcome, and role relevance."
    elif score >= 60:
        feedback = "Good answer; make the evidence and measurable result sharper."
    else:
        feedback = "Promising start; add structure, a concrete example, and a measurable outcome."

    fallback = {
        "score": score,
        "feedback": feedback,
        "suggestions": suggestions
        or ["Keep it concise, evidence-driven, and tailored to the question."],
        "question": question,
    }
    if word_count < 5:
        return fallback
    prompt = json.dumps(
        {
            "target_career": target_career,
            "question": question,
            "answer": clean[:5000],
            "rule_based_feedback": fallback,
            "required_output": {
                "score": "integer 0-100",
                "feedback": "one concise paragraph",
                "suggestions": "list of strings",
                "question": "same question string",
            },
        },
        ensure_ascii=True,
    )
    result = ai_json(
        task="interview feedback", prompt=prompt, fallback=fallback, expected_type=dict
    )
    return _valid_feedback(result, fallback)


def _valid_questions(value: Any, fallback: dict[str, list[str]]) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return fallback
    valid = {}
    for category, defaults in fallback.items():
        items = value.get(category, defaults)
        if not isinstance(items, list):
            valid[category] = defaults
        else:
            cleaned = [str(item).strip() for item in items if str(item).strip()]
            valid[category] = cleaned or defaults
    return valid


def _valid_feedback(result: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    try:
        score = int(result.get("score", fallback["score"]))
    except (TypeError, ValueError):
        score = int(fallback["score"])
    suggestions = result.get("suggestions", fallback["suggestions"])
    if not isinstance(suggestions, list):
        suggestions = fallback["suggestions"]
    return {
        "score": max(0, min(100, score)),
        "feedback": str(result.get("feedback") or fallback["feedback"]),
        "suggestions": [str(item).strip() for item in suggestions if str(item).strip()]
        or fallback["suggestions"],
        "question": str(result.get("question") or fallback["question"]),
    }
