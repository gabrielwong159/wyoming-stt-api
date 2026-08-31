import asyncio
import logging

from wyoming.server import AsyncTcpServer

from wyoming_stt_api.clients.base import BaseSTTClient
from wyoming_stt_api.clients.openai import OpenAIClient
from wyoming_stt_api.clients.openrouter import OpenRouterClient
from wyoming_stt_api.services.wyoming import WyomingEventHandler
from wyoming_stt_api.settings import Settings

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s %(name)s %(asctime)s %(message)s"
)

settings = Settings()

stt_client: BaseSTTClient
fallback_language: str | None

if settings.stt_provider == "openrouter":
    assert settings.openrouter_api_key is not None
    stt_client = OpenRouterClient(
        api_key=settings.openrouter_api_key,
        model=settings.openrouter_model,
        http_referer=settings.openrouter_http_referer,
        x_title=settings.openrouter_x_title,
    )
    fallback_language = settings.openrouter_language
else:
    assert settings.openai_api_key is not None
    stt_client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    fallback_language = settings.openai_language

# Alias for backwards compatibility
openai_client = stt_client
server = AsyncTcpServer(settings.server_host, settings.server_port)


def create_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    return WyomingEventHandler(
        stt_client,
        settings.max_audio_duration_s,
        fallback_language,
        reader,
        writer,
    )
