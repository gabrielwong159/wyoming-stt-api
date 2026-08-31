import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from wyoming.asr import Transcribe, Transcript
from wyoming.audio import AudioChunk, AudioStart, AudioStop
from wyoming.info import Describe, Info

from wyoming_stt_api.clients.base import BaseSTTClient
from wyoming_stt_api.services.wyoming import WyomingEventHandler


@pytest.mark.asyncio
async def test_wyoming_event_handler_describe():
    mock_client = MagicMock(spec=BaseSTTClient)
    mock_client.model_name = "openai/whisper-large-v3-turbo"
    mock_client.provider_name = "OpenRouter"
    mock_client.provider_url = "https://openrouter.ai/models"

    reader = AsyncMock(spec=asyncio.StreamReader)
    writer = AsyncMock(spec=asyncio.StreamWriter)

    handler = WyomingEventHandler(
        mock_client,
        max_audio_duration_s=10,
        default_language=None,
        reader=reader,
        writer=writer,
    )
    handler.write_event = AsyncMock()

    handled = await handler.handle_event(Describe().event())
    assert handled is True
    handler.write_event.assert_called_once()

    info_event = handler.write_event.call_args[0][0]
    info = Info.from_event(info_event)
    assert info.asr[0].models[0].name == "openai/whisper-large-v3-turbo"
    assert info.asr[0].models[0].attribution.name == "OpenRouter"


@pytest.mark.asyncio
async def test_wyoming_event_handler_transcribe():
    mock_client = MagicMock(spec=BaseSTTClient)
    mock_client.speech_to_text.return_value = "Turn on the lights"

    reader = AsyncMock(spec=asyncio.StreamReader)
    writer = AsyncMock(spec=asyncio.StreamWriter)

    handler = WyomingEventHandler(
        mock_client,
        max_audio_duration_s=10,
        default_language="en",
        reader=reader,
        writer=writer,
    )
    handler.write_event = AsyncMock()

    await handler.handle_event(Transcribe(language="de").event())
    assert handler._language == "de"

    await handler.handle_event(AudioStart(rate=16000, width=2, channels=1).event())
    await handler.handle_event(
        AudioChunk(audio=b"\x00" * 3200, rate=16000, width=2, channels=1).event()
    )
    await handler.handle_event(AudioStop().event())

    mock_client.speech_to_text.assert_called_once()
    assert mock_client.speech_to_text.call_args[1]["language"] == "de"

    handler.write_event.assert_called_once()
    transcript = Transcript.from_event(handler.write_event.call_args[0][0])
    assert transcript.text == "Turn on the lights"
