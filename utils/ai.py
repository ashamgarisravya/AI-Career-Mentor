"""Optional AI provider integration with rule-based fallbacks."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from dotenv import load_dotenv


load_dotenv()

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def configured_provider() -> str:
    """Return the configured AI provider, if one has a key."""
    preferred = _env("AI_PROVIDER").lower()
    has_openai = bool(_env("OPENAI_API_KEY"))
    has_gemini = bool(_env("GEMINI_API_KEY"))
    if preferred == "openai" and has_openai:
        return "openai"
    if preferred == "gemini" and has_gemini:
        return "gemini"
    if has_openai:
        return "openai"
    if has_gemini:
        return "gemini"
    return ""


def has_ai_key() -> bool:
    """Return whether an AI provider key is configured."""
    return bool(configured_provider())


def ai_status_message() -> str:
    """Return a user-facing AI status message."""
    provider = configured_provider()
    if provider:
        return f"{provider.title()} key detected. AI-enhanced analysis is enabled with rule-based fallback."
    return "No AI API key detected. Using stable rule-based analysis."


def ai_json(
    *,
    task: str,
    prompt: str,
    fallback: Any,
    expected_type: type = dict,
) -> Any:
    """Return provider JSON output, or fallback when AI is unavailable or invalid."""
    provider = configured_provider()
    if not provider:
        return fallback
    try:
        if provider == "openai":
            result = _openai_json(task, prompt)
        else:
            result = _gemini_json(task, prompt)
    except (OSError, TimeoutError, urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return fallback
    return result if isinstance(result, expected_type) else fallback


def _timeout() -> float:
    try:
        return max(3.0, min(30.0, float(_env("AI_TIMEOUT_SECONDS", "12"))))
    except ValueError:
        return 12.0


def _system_prompt(task: str) -> str:
    return (
        "You are AI Career Mentor, a career guidance engine. "
        "Return only valid JSON. Do not include markdown, prose, code fences, or extra keys. "
        f"Task: {task}."
    )


def _extract_json(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()
    start_obj = cleaned.find("{")
    start_arr = cleaned.find("[")
    starts = [index for index in (start_obj, start_arr) if index >= 0]
    if starts:
        start = min(starts)
        end = max(cleaned.rfind("}"), cleaned.rfind("]"))
        if end >= start:
            cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=_timeout()) as response:
        return json.loads(response.read().decode("utf-8"))


def _openai_json(task: str, prompt: str) -> Any:
    model = _env("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _system_prompt(task)},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    data = _post_json(
        "https://api.openai.com/v1/chat/completions",
        {
            "Authorization": f"Bearer {_env('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        },
        payload,
    )
    return _extract_json(data["choices"][0]["message"]["content"])


def _gemini_json(task: str, prompt: str) -> Any:
    model = _env("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={_env('GEMINI_API_KEY')}"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": _system_prompt(task)},
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }
    data = _post_json(url, {"Content-Type": "application/json"}, payload)
    return _extract_json(data["candidates"][0]["content"]["parts"][0]["text"])
