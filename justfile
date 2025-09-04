set dotenv-load

[private]
@default:
    just --list

@run:
    uv run python -m wyoming_stt_api

@run-file *args:
    uv run python -m wyoming_stt_api.cli {{args}}

@lint:
    uv run ruff check --fix
    uv run ruff format
    uv run mypy .
