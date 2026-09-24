import json
from pathlib import Path

def count_failed_logins(events):
    failed_count = 0

    for event in events:
        if event["event"] == "login_failed":
            failed_count += 1 

    return failed_count

def load_events(log_path):
    with log_path.open(encoding="utf-8") as file:
        return json.load(file)

def write_report(report, report_path):
    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

def main():
    log_path = Path(__file__).parent / "data" / "sample_auth.json"

    events = load_events(log_path)

    print(f"Loaded {len(events)} events")

    for event in events:
        print(f"{event['timestamp']} | {event['username']} | {event['event']}")

    failed_count = count_failed_logins(events)
    print(f"Failed logins: {failed_count}")

    report = {
        "total_events": len(events),
        "failed_logins": failed_count,
    }

    report_path = Path(__file__).parent / "data" / "auth_report.json"
    write_report(report, report_path)
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()