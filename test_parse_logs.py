import unittest

from parse_logs import count_failed_logins


class TestCountFailedLogins(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(count_failed_logins([]), 0)

    def test_mixed_events(self):
        events = [
            {"event": "login_failed"},
            {"event": "login_success"},
            {"event": "login_failed"},
        ]

        self.assertEqual(count_failed_logins(events), 2)

    def test_only_successes(self):
        events = [
            {"event": "login_success"},
            {"event": "login_success"},
        ]

        self.assertEqual(count_failed_logins(events), 0)