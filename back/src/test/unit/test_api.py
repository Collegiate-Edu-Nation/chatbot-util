# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false

import unittest

from fastapi.testclient import TestClient

from chatbot_util import api

client = TestClient(api.app)


class TestChain(unittest.TestCase):
    def test_generate_rate_limit(self):
        # monkey patch to simulate current generation
        api.allow_generate = False

        response = client.post(
            "/api/generate",
            headers={api.auth.APPLICATION_REQUEST_HEADER: "1"},
        )
        assert response.status_code == 429
        assert response.json() == {"verified": None}

        # reset monkey patch to prevent muddying state for other tests
        api.allow_generate = True

    def test_generate_rejects_request_without_application_marker(self):
        response = client.post("/api/generate")
        assert response.status_code == 403
        assert response.json() == {"detail": "Missing application request marker"}

    def test_session_reports_local_mode(self):
        response = client.get("/api/session")
        assert response.status_code == 200
        assert response.json() == {"authenticated": False, "user": None}
        assert response.headers["cache-control"] == "no-store"

    def test_progress(self):
        response = client.get("/api/progress")
        assert response.status_code == 200
        assert response.json() == {"index": 0, "total": 0}
