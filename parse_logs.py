import json
from pathlib import Path

def count_failed_logins(events):
    failed_count = 0

    for event in events:
        if event["event"] == "login_failed":
            failed_count += 1 

    return failed_count

def main():
    log_path = Path(__file__).parent / "data" / "sample_auth.json"

    with log_path.open(encoding="utf-8") as file:
        events = json.load(file)

    print(f"Loaded {len(events)} events")

    for event in events:
        print(f"{event['timestamp']} | {event['username']} | {event['event']}")

    failed_count = count_failed_logins(events)
    print(f"Failed logins: {failed_count}")

if __name__ == "__main__":
    main()