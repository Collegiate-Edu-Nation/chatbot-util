# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

"""Create Ollama clients for local development and authenticated cloud use."""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from ollama import Client

from chatbot_util import file_io

API_KEY_ENV = "OLLAMA_API_KEY"
API_KEY_FILE_ENV = "OLLAMA_API_KEY_FILE"
SYSTEMD_CREDENTIAL_NAME = "ollama-api-key"
SYSTEMD_CREDENTIALS_DIRECTORY_ENV = "CREDENTIALS_DIRECTORY"


@dataclass(frozen=True)
class OllamaSettings:
    """Resolved Ollama connection settings without exposing secrets in repr."""

    host: str
    model: str
    api_key: str | None = field(default=None, repr=False)


def _read_api_key_file(filename: str) -> str:
    """Read a non-empty API key from a protected file."""
    try:
        api_key = Path(filename).read_text(encoding="utf-8").strip()
    except OSError as error:
        raise RuntimeError("Failed to read the Ollama API key file") from error

    if not api_key:
        raise RuntimeError("The Ollama API key file is empty")
    return api_key


def _api_key() -> str | None:
    """Resolve an API key from an environment value or protected file."""
    environment_key = os.getenv(API_KEY_ENV)
    if environment_key is not None:
        normalized_key = environment_key.strip()
        if not normalized_key:
            raise RuntimeError(f"{API_KEY_ENV} is empty")
        return normalized_key

    configured_file = os.getenv(API_KEY_FILE_ENV)
    if configured_file is not None:
        return _read_api_key_file(configured_file)

    credentials_directory = os.getenv(SYSTEMD_CREDENTIALS_DIRECTORY_ENV)
    if credentials_directory is not None:
        credential = Path(credentials_directory) / SYSTEMD_CREDENTIAL_NAME
        if credential.is_file():
            return _read_api_key_file(str(credential))

    return None


def read_settings() -> OllamaSettings:
    """Resolve and validate the active Ollama host, model, and credential."""
    config = file_io.read_config()
    settings = OllamaSettings(
        host=config["url"].strip(),
        model=config["model"].strip(),
        api_key=_api_key(),
    )
    parsed_host = urlsplit(settings.host)
    hostname = parsed_host.hostname

    if not settings.host:
        raise RuntimeError("The Ollama host is empty")
    if not settings.model:
        raise RuntimeError("The Ollama model is empty")

    if hostname == "ollama.com":
        if parsed_host.scheme != "https":
            raise RuntimeError("Ollama Cloud must use https://ollama.com")
        if settings.api_key is None:
            raise RuntimeError("OLLAMA_API_KEY is required for Ollama Cloud")

    if (
        settings.api_key is not None
        and parsed_host.scheme == "http"
        and hostname not in {"127.0.0.1", "::1", "localhost"}
    ):
        raise RuntimeError("Refusing to send an Ollama API key over plaintext HTTP")

    return settings


def create_client(settings: OllamaSettings) -> Client:
    """Create an Ollama client, adding a bearer token only when configured."""
    headers = (
        {"Authorization": f"Bearer {settings.api_key}"}
        if settings.api_key is not None
        else None
    )
    return Client(host=settings.host, headers=headers)


def check() -> None:
    """Check that the configured model is available."""
    settings = read_settings()
    client = create_client(settings)
    try:
        client.show(settings.model)
    finally:
        client.close()


def generate(prompt: str, options: Mapping[str, Any]) -> str:
    """Generate a response using the configured local or cloud model."""
    settings = read_settings()
    client = create_client(settings)
    try:
        response = client.generate(
            model=settings.model,
            prompt=prompt,
            options=options,
        )
    finally:
        client.close()
    if response.response is None:
        raise RuntimeError("Ollama returned an empty response")
    return response.response
