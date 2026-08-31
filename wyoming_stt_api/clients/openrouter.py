import logging
import time
from typing import BinaryIO

from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenRouterClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        http_referer: str | None = None,
        x_title: str | None = None,
    ):
        headers: dict[str, str] = {}
        if http_referer:
            headers["HTTP-Referer"] = http_referer
        if x_title:
            headers["X-Title"] = x_title

        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers=headers if headers else None,
        )
        self._model = model

    def speech_to_text(
        self,
        audio_file: BinaryIO,
        file_extension: str | None = None,
        language: str | None = None,
    ) -> str:
        # A file extension is needed for cases where audio_file does not have a
        # name, such as when using in-memory files. The OpenAI SDK needs a name
        # to infer the file type, so we pass in a dummy file name.
        file: BinaryIO | tuple[str, BinaryIO]
        if file_extension is not None:
            file = (f"dummy.{file_extension}", audio_file)
        else:
            file = audio_file

        # OpenRouter expects response_format to be "json" or "verbose_json".
        kwargs: dict = {
            "model": self._model,
            "file": file,
            "response_format": "json",
        }
        if language is not None:
            kwargs["language"] = language

        start_time = time.time()
        result = self._client.audio.transcriptions.create(**kwargs)
        logger.info(f"Time taken to transcribe: {time.time() - start_time:.2f}s")

        if hasattr(result, "text"):
            text: str = result.text
        elif isinstance(result, dict):
            text = result.get("text", "")
        else:
            text = str(result)

        logger.info(f"Transcription: {text}")
        return text

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider_name(self) -> str:
        return "OpenRouter"

    @property
    def provider_url(self) -> str:
        return "https://openrouter.ai/models"
