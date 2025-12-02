# SPDX-FileCopyrightText: Collegiate Edu-Nation
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from fastapi.testclient import TestClient

from chatbot_util import api, chain

client = TestClient(api.app)


class TestChain(unittest.TestCase):
    def test_interrupt(self):
        # index = 0 indicates progress has been reset, so we should exit the loop
        # immediately w/ 200 code and be ready for generation
        response = client.get("/api/interrupt")
        chain.handle_interrupt()
        assert response.status_code == 200
        assert not chain.interrupt
