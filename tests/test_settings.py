import pytest
from pydantic import ValidationError

from wyoming_stt_api.settings import Settings


def test_settings_default_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-proj-test1234")
    settings = Settings()

    assert settings.stt_provider == "openai"
    assert settings.openai_api_key == "sk-proj-test1234"
    assert settings.openai_model == "gpt-transcribe"
    assert settings.server_port == 10300


def test_settings_auto_detect_openrouter(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test1234")
    settings = Settings()

    assert settings.stt_provider == "openrouter"
    assert settings.openrouter_api_key == "sk-or-v1-test1234"
    assert settings.openrouter_model == "openai/whisper-large-v3-turbo"


def test_settings_explicit_provider(monkeypatch):
    monkeypatch.setenv("STT_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.setenv("OPENROUTER_MODEL", "google/chirp-3")
    settings = Settings()

    assert settings.stt_provider == "openrouter"
    assert settings.openrouter_model == "google/chirp-3"


def test_settings_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("STT_PROVIDER", raising=False)

    with pytest.raises(ValidationError):
        Settings()
