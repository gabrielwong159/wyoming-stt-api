[private]
@default:
    just --list

@run:
    uv run python -m wyoming_stt_api.main

@lint:
    uv run ruff check --fix
    uv run ruff format
    uv run mypy .
