import logging

from wyoming_stt_api.clients.openai import OpenAIClient
from wyoming_stt_api.settings import Settings

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s %(name)s %(asctime)s %(message)s"
)


settings = Settings()
openai_client = OpenAIClient(
    api_key=settings.openai_api_key, model=settings.openai_model
)
