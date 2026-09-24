import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from parse_logs import main

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

    def test_invalid_json_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            log_path = Path(folder) / "broken.json"
            log_path.write_text('{"event":', encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                load_events(log_path)

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

class TestMain(unittest.TestCase):
    def test_invalid_json_stops_before_writing_report(self):
        error = json.JSONDecodeError("Invalid JSON", '{"event":', 9)

        with patch("parse_logs.load_events", side_effect=error):
            with patch("parse_logs.write_report") as mock_write:
                with patch("sys.stderr") as mock_stderr:
                    with self.assertRaises(SystemExit) as stopped:
                        main()

        self.assertEqual(stopped.exception.code, 1)
        mock_write.assert_not_called()

        error_text = "".join(
            call.args[0] for call in mock_stderr.write.call_args_list
        )
        self.assertIn("invalid JSON", error_text)

    def test_missing_file_stops_before_writing_report(self):
        with patch("parse_logs.load_events", side_effect=FileNotFoundError):
            with patch("parse_logs.write_report") as mock_write:
                with patch("sys.stderr") as mock_stderr:
                    with self.assertRaises(SystemExit) as stopped:
                        main()

        self.assertEqual(stopped.exception.code, 1)
        mock_write.assert_not_called()

        error_text = "".join(
            call.args[0] for call in mock_stderr.write.call_args_list
        )
        self.assertIn("file not found", error_text)