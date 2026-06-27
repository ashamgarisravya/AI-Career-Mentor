import json
import urllib.error

import pytest

from utils import ai

# pylint: disable=protected-access


def test_ai_json_returns_fallback_without_api_key() -> None:
    fallback = {"summary": "rule based"}

    result = ai.ai_json(
        task="resume analysis",
        prompt="{}",
        fallback=fallback,
        expected_type=dict,
    )

    assert result == fallback
    assert ai.configured_provider() == ""
    assert not ai.has_ai_key()
    assert "rule-based" in ai.ai_status_message()


def test_ai_json_uses_openai_when_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_post(
        url: str, headers: dict[str, str], payload: dict[str, object]
    ) -> dict[str, object]:
        assert url == "https://api.openai.com/v1/chat/completions"
        assert headers["Authorization"] == "Bearer test-key"
        assert payload["response_format"] == {"type": "json_object"}
        return {"choices": [{"message": {"content": '{"score": 91}'}}]}

    monkeypatch.setattr(ai, "_post_json", fake_post)

    assert ai.ai_json(task="career", prompt="{}", fallback={}, expected_type=dict) == {"score": 91}
    assert ai.configured_provider() == "openai"


def test_ai_json_uses_gemini_and_extracts_fenced_json(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def fake_post(
        url: str, headers: dict[str, str], payload: dict[str, object]
    ) -> dict[str, object]:
        assert "key=test-key" in url
        assert headers["Content-Type"] == "application/json"
        assert "contents" in payload
        return {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": '```json\n{"recommendations": ["AI Engineer"]}\n```'}]
                    }
                }
            ]
        }

    monkeypatch.setattr(ai, "_post_json", fake_post)

    result = ai.ai_json(task="career", prompt="{}", fallback={}, expected_type=dict)

    assert result == {"recommendations": ["AI Engineer"]}
    assert ai.configured_provider() == "gemini"


def test_ai_json_falls_back_on_provider_error(monkeypatch: pytest.MonkeyPatch) -> None:
    fallback = {"safe": True}
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def broken_post(*args: object, **kwargs: object) -> dict[str, object]:
        raise urllib.error.URLError("network unavailable")

    monkeypatch.setattr(ai, "_post_json", broken_post)

    assert ai.ai_json(task="resume", prompt="{}", fallback=fallback, expected_type=dict) == fallback


def test_timeout_and_json_extraction_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_TIMEOUT_SECONDS", "1")
    assert ai._timeout() == 3.0

    monkeypatch.setenv("AI_TIMEOUT_SECONDS", "45")
    assert ai._timeout() == 30.0

    monkeypatch.setenv("AI_TIMEOUT_SECONDS", "bad")
    assert ai._timeout() == 12.0

    assert ai._extract_json('prefix {"ok": true} suffix') == {"ok": True}
    with pytest.raises(json.JSONDecodeError):
        ai._extract_json("not json")
