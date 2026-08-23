from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    # See link for available model names:
    # https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create
    openai_model: str = "gpt-transcribe"
    # Fallback language (ISO 639-1, e.g. "en", "de") used when the Wyoming
    # client doesn't specify one via the Transcribe event. None lets the
    # OpenAI API auto-detect the spoken language.
    openai_language: str | None = None

    server_host: str = "0.0.0.0"
    server_port: int = 10300

    max_audio_duration_s: int = 10
