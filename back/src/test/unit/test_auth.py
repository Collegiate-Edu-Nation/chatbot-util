# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnusedFunction=false

import os
import unittest
from unittest import mock

import fastapi
from fastapi.testclient import TestClient

from chatbot_util import auth


def proxy_app(config: auth.ProxyAuthConfig) -> fastapi.FastAPI:
    """Create a minimal application using the proxy authentication middleware."""
    app = fastapi.FastAPI()
    app.add_middleware(auth.ProxyAuthenticationMiddleware, config=config)

    @app.get("/")
    def identity(request: fastapi.Request) -> dict[str, str | None]:
        return {"user": auth.authenticated_user(request)}

    return app


class TestProxyAuthConfig(unittest.TestCase):
    def test_reads_enabled_proxy_auth(self):
        with mock.patch.dict(
            os.environ,
            {
                auth.PROXY_AUTH_ENV: "true",
                auth.AUTH_HEADER_ENV: "X-OIDC-User",
            },
        ):
            config = auth.ProxyAuthConfig.from_environment()

        assert config.enabled
        assert config.user_header == "X-OIDC-User"

    def test_rejects_invalid_boolean(self):
        with mock.patch.dict(os.environ, {auth.PROXY_AUTH_ENV: "maybe"}):
            with self.assertRaises(RuntimeError):
                auth.ProxyAuthConfig.from_environment()

    def test_rejects_invalid_header_name(self):
        with self.assertRaises(ValueError):
            auth.ProxyAuthConfig(user_header="not a header")


class TestProxyAuthenticationMiddleware(unittest.TestCase):
    def test_disabled_mode_ignores_identity_header(self):
        client = TestClient(proxy_app(auth.ProxyAuthConfig()))
        response = client.get(
            "/", headers={auth.DEFAULT_AUTH_HEADER: "fake@example.com"}
        )

        assert response.status_code == 200
        assert response.json() == {"user": None}

    def test_enabled_mode_requires_identity_header(self):
        client = TestClient(proxy_app(auth.ProxyAuthConfig(enabled=True)))
        response = client.get("/")

        assert response.status_code == 401
        assert response.json() == {"detail": "Authentication required"}
        assert response.headers["cache-control"] == "no-store"

    def test_enabled_mode_accepts_proxy_identity(self):
        client = TestClient(proxy_app(auth.ProxyAuthConfig(enabled=True)))
        response = client.get(
            "/", headers={auth.DEFAULT_AUTH_HEADER: "admin@example.com"}
        )

        assert response.status_code == 200
        assert response.json() == {"user": "admin@example.com"}

    def test_enabled_mode_rejects_ambiguous_identity(self):
        client = TestClient(proxy_app(auth.ProxyAuthConfig(enabled=True)))
        response = client.get(
            "/",
            headers=[
                (auth.DEFAULT_AUTH_HEADER, "first@example.com"),
                (auth.DEFAULT_AUTH_HEADER, "second@example.com"),
            ],
        )

        assert response.status_code == 401
