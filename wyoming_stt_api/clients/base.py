from typing import BinaryIO, Protocol


class BaseSTTClient(Protocol):
    def speech_to_text(
        self,
        audio_file: BinaryIO,
        file_extension: str | None = None,
        language: str | None = None,
    ) -> str: ...

    @property
    def model_name(self) -> str: ...

    @property
    def provider_name(self) -> str: ...

    @property
    def provider_url(self) -> str: ...
