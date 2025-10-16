import unittest

from fastapi.testclient import TestClient

from chatbot_util import api

client = TestClient(api.app)


class TestChain(unittest.TestCase):
    def test_progress(self):
        response = client.get("/api/progress")
        assert response.status_code == 200
        assert response.json() == {"index": 0, "total": 0}
