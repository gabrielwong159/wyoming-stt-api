import logging
import time
from typing import BinaryIO

from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def speech_to_text(self, audio_file: BinaryIO) -> str:
        start_time = time.time()
        result: str = self._client.audio.transcriptions.create(
            model=self._model,
            file=audio_file,
            language="en",
            response_format="text",
        )
        logger.info(f"Time taken to transcribe: {time.time() - start_time:.2f}s")
        logger.info(f"Transcription: {result}")
        return result

    @property
    def model_name(self) -> str:
        return self._model
