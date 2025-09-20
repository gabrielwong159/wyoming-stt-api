from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True, cli_kebab_case=True)

    openai_api_key: str
    # See link for available model names:
    # https://platform.openai.com/docs/api-reference/audio/createTranscription
    openai_model: str = "gpt-4o-mini-transcribe"

    server_host: str = "0.0.0.0"
    server_port: int = 10300

    max_audio_duration_s: int = 10
