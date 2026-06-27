"""AI helper functions with graceful fallback behavior."""

from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv()


def has_ai_key() -> bool:
    """Return whether an AI provider key is configured."""
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY"))


def ai_status_message() -> str:
    """Return a user-facing AI status message."""
    if has_ai_key():
        return "AI key detected. The app can be extended to call the configured provider."
    return "No AI API key detected. Using stable rule-based analysis."
