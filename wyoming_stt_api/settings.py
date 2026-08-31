from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    stt_provider: Literal["openai", "openrouter"] | None = None

    # OpenAI settings
    openai_api_key: str | None = None
    # See link for available model names:
    # https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create
    openai_model: str = "gpt-transcribe"
    # Fallback language (ISO 639-1, e.g. "en", "de") used when the Wyoming
    # client doesn't specify one via the Transcribe event. None lets the
    # OpenAI API auto-detect the spoken language.
    openai_language: str | None = None

    # OpenRouter settings
    openrouter_api_key: str | None = None
    # See link for available model names:
    # https://openrouter.ai/models?output_modalities=transcription
    openrouter_model: str = "openai/whisper-large-v3-turbo"
    openrouter_language: str | None = None
    openrouter_http_referer: str | None = "https://home-assistant.io"
    openrouter_x_title: str | None = "Wyoming STT API"

    server_host: str = "0.0.0.0"
    server_port: int = 10300

    max_audio_duration_s: int = 10

    @model_validator(mode="after")
    def validate_provider_and_keys(self) -> "Settings":
        if self.stt_provider is None:
            if self.openrouter_api_key and not self.openai_api_key:
                self.stt_provider = "openrouter"
            else:
                self.stt_provider = "openai"

        if self.stt_provider == "openai" and not self.openai_api_key:
            raise ValueError("openai_api_key must be set when stt_provider is 'openai'")
        if self.stt_provider == "openrouter" and not self.openrouter_api_key:
            raise ValueError(
                "openrouter_api_key must be set when stt_provider is 'openrouter'"
            )

        return self
