import unittest
from fastapi.testclient import TestClient

from api import app


class TestAnalyzeAPI(unittest.TestCase):
    def test_mixed_events(self):
        client = TestClient(app)

        events = [
            {"event": "login_failed"},
            {"event": "login_success"},
            {"event": "login_failed"},
        ]

        response = client.post("/analyze", json=events)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"failed_logins": 2})

    def test_empty_events(self):
        client = TestClient(app)

        events = []

        response = client.post("/analyze", json=events)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"failed_logins": 0})