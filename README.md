# Wyoming server with speech-to-text API

A Wyoming server that uses third-party speech-to-text APIs to transcribe audio.
For now, only the [OpenAI API](https://platform.openai.com/docs/guides/speech-to-text) is supported.


## Setup

This project uses [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for package management.

```bash
git clone https://github.com/gabrielwong159/wyoming-stt-api.git
cd wyoming-stt-api/
uv sync
```

Visit the [OpenAI developer platform](https://platform.openai.com/docs/overview)
to get an API key. You will need to place your API key in a `.env` file:

```
OPENAI_API_KEY=sk-proj-abc123
```

The server transcribes in whatever language your Wyoming client (e.g. Home
Assistant's Assist pipeline) requests. If a client doesn't specify one, it
falls back to `OPENAI_LANGUAGE` if set, or auto-detects the spoken language
otherwise:

```
OPENAI_LANGUAGE=en
```

## Usage

To run the server, use the following command:

```bash
just run
```

Optionally, refer to the `justfile` to inspect the command.

You can also run the speech-to-text API directly on a local file for testing:

```bash
just run-file /path/to/audio.wav
```
