# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from chatbot_util import file_io, ollama_client

from .. import utilities


def config(
    host: str = "http://127.0.0.1:11434", model: str = "mistral"
) -> file_io.Config:
    """Return a complete application config for Ollama settings tests."""
    return {
        "host": "127.0.0.1",
        "port": 8080,
        "url": host,
        "model": model,
        "faq": "",
        "other": "",
    }


class TestOllamaSettings(unittest.TestCase):
    def test_local_ollama_does_not_require_api_key(self):
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(
                ollama_client.file_io, "read_config", return_value=config()
            ),
        ):
            settings = ollama_client.read_settings()

        assert settings.host == "http://127.0.0.1:11434"
        assert settings.model == "mistral"
        assert settings.api_key is None

    def test_cloud_ollama_reads_environment_api_key(self):
        with (
            mock.patch.dict(
                os.environ, {ollama_client.API_KEY_ENV: "cloud-secret"}, clear=True
            ),
            mock.patch.object(
                ollama_client.file_io,
                "read_config",
                return_value=config("https://ollama.com", "gpt-oss:120b"),
            ),
        ):
            settings = ollama_client.read_settings()

        assert settings.api_key == "cloud-secret"
        assert "cloud-secret" not in repr(settings)

    def test_cloud_ollama_requires_api_key(self):
        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(
                ollama_client.file_io,
                "read_config",
                return_value=config("https://ollama.com", "gpt-oss:120b"),
            ),
            self.assertRaises(RuntimeError),
        ):
            ollama_client.read_settings()

    def test_reads_api_key_from_file(self):
        with utilities.TestFileContent(["cloud-secret\n"]) as secret_file:
            with (
                mock.patch.dict(
                    os.environ,
                    {ollama_client.API_KEY_FILE_ENV: secret_file.filename},
                    clear=True,
                ),
                mock.patch.object(
                    ollama_client.file_io,
                    "read_config",
                    return_value=config("https://ollama.com", "gpt-oss:120b"),
                ),
            ):
                settings = ollama_client.read_settings()

        assert settings.api_key == "cloud-secret"

    def test_reads_api_key_from_systemd_credential(self):
        with tempfile.TemporaryDirectory() as credentials_directory:
            credential = (
                Path(credentials_directory) / ollama_client.SYSTEMD_CREDENTIAL_NAME
            )
            credential.write_text("cloud-secret\n", encoding="utf-8")

            with (
                mock.patch.dict(
                    os.environ,
                    {
                        ollama_client.SYSTEMD_CREDENTIALS_DIRECTORY_ENV: credentials_directory
                    },
                    clear=True,
                ),
                mock.patch.object(
                    ollama_client.file_io,
                    "read_config",
                    return_value=config("https://ollama.com", "gpt-oss:120b"),
                ),
            ):
                settings = ollama_client.read_settings()

        assert settings.api_key == "cloud-secret"

    def test_rejects_api_key_over_remote_plaintext_http(self):
        with (
            mock.patch.dict(
                os.environ, {ollama_client.API_KEY_ENV: "cloud-secret"}, clear=True
            ),
            mock.patch.object(
                ollama_client.file_io,
                "read_config",
                return_value=config("http://ollama.internal", "private-model"),
            ),
            self.assertRaises(RuntimeError),
        ):
            ollama_client.read_settings()


class TestOllamaClient(unittest.TestCase):
    def test_adds_bearer_header(self):
        settings = ollama_client.OllamaSettings(
            host="https://ollama.com",
            model="gpt-oss:120b",
            api_key="cloud-secret",
        )

        with mock.patch.object(ollama_client, "Client") as constructor:
            ollama_client.create_client(settings)

        constructor.assert_called_once_with(
            host="https://ollama.com",
            headers={"Authorization": "Bearer cloud-secret"},
        )

    def test_generate_uses_configured_model_and_closes_client(self):
        settings = ollama_client.OllamaSettings(
            host="https://ollama.com",
            model="gpt-oss:120b",
            api_key="cloud-secret",
        )
        client = mock.MagicMock()
        client.generate.return_value.response = "generated"

        with (
            mock.patch.object(ollama_client, "read_settings", return_value=settings),
            mock.patch.object(ollama_client, "create_client", return_value=client),
        ):
            response = ollama_client.generate("prompt", {"seed": 39})

        assert response == "generated"
        client.generate.assert_called_once_with(
            model="gpt-oss:120b",
            prompt="prompt",
            options={"seed": 39},
        )
        client.close.assert_called_once_with()
