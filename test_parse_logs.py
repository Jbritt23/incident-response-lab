import unittest
import json
import tempfile
from pathlib import Path

from parse_logs import count_failed_logins, load_events, write_report


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

class TestLoadEvents(unittest.TestCase):
    def test_reads_events_from_file(self):
        expected_events = [{"event": "login_failed"}]

        with tempfile.TemporaryDirectory() as folder:
            log_path = Path(folder) / "events.json"
            log_path.write_text(
                json.dumps(expected_events),
                encoding="utf-8",
            )

            actual_events = load_events(log_path)

        self.assertEqual(actual_events, expected_events)

class TestWriteReport(unittest.TestCase):
    def test_saves_report_as_json(self):
        report = {
            "total_events": 3,
            "failed_logins": 2,
        }

        with tempfile.TemporaryDirectory() as folder:
            report_path = Path(folder) / "reports" / "summary.json"

            write_report(report, report_path)

            with report_path.open(encoding="utf-8") as file:
                saved_report = json.load(file)

        self.assertEqual(saved_report, report)