from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    # See link for available model names:
    # https://platform.openai.com/docs/api-reference/audio/createTranscription
    openai_model: str = "gpt-4o-mini-transcribe"
