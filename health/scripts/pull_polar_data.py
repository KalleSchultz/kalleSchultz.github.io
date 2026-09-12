#!/usr/bin/env python3
"""Pull new health data from the Polar AccessLink API and store it as JSON.

Runs daily via .github/workflows/polar-health-sync.yml. Requires:
    POLAR_ACCESS_TOKEN  - long-lived access token (see health/README.md)
    POLAR_USER_ID        - Polar user id for that token

Writes raw records under health/data/<category>/ and rebuilds a compact
health/data/summary.json that the dashboard (health/index.html) reads.
"""

import datetime
import json
import os
import sys
from pathlib import Path

import requests

API_BASE = "https://www.polaraccesslink.com/v3"
HEALTH_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = HEALTH_DIR / "data"
SUMMARY_PATH = DATA_DIR / "summary.json"
SUMMARY_HISTORY_DAYS = 90


def headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def pull_transaction_resource(session: requests.Session, user_id: str, resource: str, list_key: str):
    """Generic AccessLink transaction flow: create -> list -> fetch each -> commit.

    `resource` is e.g. "activity", "exercise", "physical-information".
    `list_key` is the JSON key in the listing response that holds item URLs.
    Returns a list of fetched item JSON bodies (possibly empty).
    """
    create_url = f"{API_BASE}/users/{user_id}/{resource}-transactions"
    resp = session.post(create_url)

    if resp.status_code == 204:
        return []  # nothing new since last sync
    if resp.status_code == 404:
        return []  # no transaction available
    resp.raise_for_status()

    transaction = resp.json()
    listing_url = transaction.get("resource-uri")
    if not listing_url:
        return []

    listing = session.get(listing_url)
    listing.raise_for_status()
    item_urls = listing.json().get(list_key, [])

    items = []
    for item_url in item_urls:
        item_resp = session.get(item_url)
        if item_resp.ok:
            items.append(item_resp.json())
        else:
            print(f"  warning: failed to fetch {item_url}: {item_resp.status_code}", file=sys.stderr)

    # Commit the transaction so Polar doesn't re-serve this data next time.
    commit_resp = session.put(listing_url)
    if not commit_resp.ok:
        print(f"  warning: failed to commit {resource} transaction: {commit_resp.status_code}", file=sys.stderr)

    return items


def pull_activity(session: requests.Session, user_id: str):
    items = pull_transaction_resource(session, user_id, "activity", "activity-log")
    for item in items:
        date = item.get("date", "unknown")
        save_json(DATA_DIR / "activity" / f"{date}.json", item)
    return items


def pull_exercise(session: requests.Session, user_id: str):
    items = pull_transaction_resource(session, user_id, "exercise", "exercises")
    for item in items:
        exercise_id = item.get("id") or item.get("start-time", "unknown")
        safe_id = str(exercise_id).replace(":", "-")
        save_json(DATA_DIR / "exercise" / f"{safe_id}.json", item)
    return items


def pull_physical_information(session: requests.Session, user_id: str):
    items = pull_transaction_resource(session, user_id, "physical-information", "physical-informations")
    for item in items:
        item_id = item.get("created") or "unknown"
        safe_id = str(item_id).replace(":", "-")
        save_json(DATA_DIR / "physical-information" / f"{safe_id}.json", item)
    return items


def pull_sleep(session: requests.Session, user_id: str):
    """Sleep endpoint returns up to the last 28 nights, not transaction-based."""
    resp = session.get(f"{API_BASE}/users/{user_id}/sleep")
    if not resp.ok:
        print(f"  warning: sleep fetch failed: {resp.status_code} {resp.text}", file=sys.stderr)
        return []
    nights = resp.json().get("nights", [])
    for night in nights:
        date = night.get("date", "unknown")
        save_json(DATA_DIR / "sleep" / f"{date}.json", night)
    return nights


def pull_continuous_heart_rate(session: requests.Session, user_id: str, date: str):
    resp = session.get(f"{API_BASE}/users/{user_id}/continuous-heart-rate/{date}")
    if resp.status_code == 404:
        return None
    if not resp.ok:
        print(f"  warning: continuous HR fetch failed for {date}: {resp.status_code}", file=sys.stderr)
        return None
    data = resp.json()
    save_json(DATA_DIR / "continuous-heart-rate" / f"{date}.json", data)
    return data


def load_existing(category: str) -> dict:
    """Load all saved JSON files for a category, keyed by filename stem."""
    records = {}
    folder = DATA_DIR / category
    if not folder.exists():
        return records
    for path in folder.glob("*.json"):
        try:
            records[path.stem] = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
    return records


def build_summary() -> dict:
    cutoff = (datetime.date.today() - datetime.timedelta(days=SUMMARY_HISTORY_DAYS)).isoformat()

    activity_rows = []
    for date, item in sorted(load_existing("activity").items()):
        if date < cutoff:
            continue
        activity_rows.append(
            {
                "date": date,
                "steps": item.get("active-steps") or item.get("steps"),
                "calories": item.get("calories"),
                "active_calories": item.get("active-calories"),
            }
        )

    sleep_rows = []
    for date, item in sorted(load_existing("sleep").items()):
        if date < cutoff:
            continue
        sleep_rows.append(
            {
                "date": date,
                "total_sleep_seconds": item.get("total-sleep-duration") or item.get("total_sleep_duration"),
                "sleep_score": item.get("sleep-score") or item.get("sleep_score"),
            }
        )

    exercise_rows = []
    for _id, item in sorted(load_existing("exercise").items(), key=lambda kv: kv[1].get("start-time", "")):
        exercise_rows.append(
            {
                "date": (item.get("start-time") or "")[:10],
                "sport": item.get("sport") or item.get("detailed-sport-info"),
                "duration": item.get("duration"),
                "calories": item.get("calories"),
                "distance_m": item.get("distance"),
            }
        )
    exercise_rows = [r for r in exercise_rows if r["date"] >= cutoff]

    hr_rows = []
    for date, item in sorted(load_existing("continuous-heart-rate").items()):
        if date < cutoff:
            continue
        samples = item.get("heart-rate-samples") or item.get("heart_rate_samples") or []
        bpm_values = [s.get("heart-rate") for s in samples if isinstance(s, dict) and s.get("heart-rate")]
        hr_rows.append(
            {
                "date": date,
                "avg_bpm": round(sum(bpm_values) / len(bpm_values), 1) if bpm_values else None,
                "min_bpm": min(bpm_values) if bpm_values else None,
                "max_bpm": max(bpm_values) if bpm_values else None,
                "sample_count": len(samples),
            }
        )

    return {
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "activity": activity_rows,
        "sleep": sleep_rows,
        "exercise": exercise_rows,
        "continuous_heart_rate": hr_rows,
    }


def main() -> None:
    token = os.environ.get("POLAR_ACCESS_TOKEN")
    user_id = os.environ.get("POLAR_USER_ID")
    if not token or not user_id:
        sys.exit("POLAR_ACCESS_TOKEN and POLAR_USER_ID must be set (see health/README.md).")

    session = requests.Session()
    session.headers.update(headers(token))
    session.request = _with_timeout(session.request)

    print("Pulling activity data...")
    pull_activity(session, user_id)

    print("Pulling exercise data...")
    pull_exercise(session, user_id)

    print("Pulling physical information...")
    pull_physical_information(session, user_id)

    print("Pulling sleep data...")
    pull_sleep(session, user_id)

    print("Pulling continuous heart rate for the last 3 days...")
    today = datetime.date.today()
    for days_ago in range(1, 4):
        date = (today - datetime.timedelta(days=days_ago)).isoformat()
        pull_continuous_heart_rate(session, user_id, date)

    print("Rebuilding summary.json...")
    save_json(SUMMARY_PATH, build_summary())

    print("Done.")


def _with_timeout(request_fn, timeout: int = 30):
    def wrapped(*args, **kwargs):
        kwargs.setdefault("timeout", timeout)
        return request_fn(*args, **kwargs)

    return wrapped


if __name__ == "__main__":
    main()
