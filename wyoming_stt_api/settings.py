from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    # See link for available model names:
    # https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create
    openai_model: str = "gpt-transcribe"

    server_host: str = "0.0.0.0"
    server_port: int = 10300

    max_audio_duration_s: int = 10
