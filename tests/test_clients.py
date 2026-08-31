from io import BytesIO
from unittest.mock import MagicMock, patch

from wyoming_stt_api.clients.openai import OpenAIClient
from wyoming_stt_api.clients.openrouter import OpenRouterClient


def test_openai_client():
    client = OpenAIClient(api_key="sk-test", model="gpt-transcribe")
    assert client.provider_name == "OpenAI"
    assert client.model_name == "gpt-transcribe"

    mock_transcription = MagicMock()
    mock_transcription.text = "Hello world"

    with patch.object(
        client._client.audio.transcriptions, "create", return_value="Hello world"
    ) as mock_create:
        audio = BytesIO(b"fake-audio")
        result = client.speech_to_text(audio, file_extension="wav", language="en")
        assert result == "Hello world"

        mock_create.assert_called_once()
        kwargs = mock_create.call_args.kwargs
        assert kwargs["model"] == "gpt-transcribe"
        assert kwargs["language"] == "en"


def test_openrouter_client():
    client = OpenRouterClient(
        api_key="sk-or-test",
        model="openai/whisper-large-v3-turbo",
        http_referer="https://home-assistant.io",
        x_title="Wyoming STT API",
    )
    assert client.provider_name == "OpenRouter"
    assert client.model_name == "openai/whisper-large-v3-turbo"

    mock_transcription = MagicMock()
    mock_transcription.text = "Hello from OpenRouter"

    with patch.object(
        client._client.audio.transcriptions, "create", return_value=mock_transcription
    ) as mock_create:
        audio = BytesIO(b"fake-audio")
        result = client.speech_to_text(audio, file_extension="wav", language="es")
        assert result == "Hello from OpenRouter"

        mock_create.assert_called_once()
        kwargs = mock_create.call_args.kwargs
        assert kwargs["model"] == "openai/whisper-large-v3-turbo"
        assert kwargs["response_format"] == "json"
        assert kwargs["language"] == "es"
