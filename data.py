import csv
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

from config import (
    ACTIVITY_PATH, SETTINGS_PATH,
    DEFAULT_SETTINGS,
)


# ── Settings ───────────────────────────────────────────────────

def load_settings() -> dict:
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict) -> None:
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def ensure_csv() -> None:
    if not os.path.exists(ACTIVITY_PATH):
        with open(ACTIVITY_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["date", "app", "active_time", "detected_activity"])


def commit_activity(app_name: str, active_time: int, detected_activity: str) -> None:
    ensure_csv()
    with open(ACTIVITY_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            app_name, active_time, detected_activity,
        ])


def load_activity_last_7_days() -> dict:
    ensure_csv()
    result: dict = defaultdict(lambda: defaultdict(int))
    cutoff = datetime.now() - timedelta(days=7)
    try:
        with open(ACTIVITY_PATH, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    dt = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
                    if dt >= cutoff:
                        result[dt.strftime("%d/%m")][row["app"]] += int(row["active_time"])
                except Exception:
                    pass
    except Exception:
        pass
    return result


def load_app_totals_7_days() -> dict:
    ensure_csv()
    result: dict = defaultdict(int)
    cutoff = datetime.now() - timedelta(days=7)
    try:
        with open(ACTIVITY_PATH, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    dt = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
                    if dt >= cutoff:
                        result[row["app"]] += int(row["active_time"])
                except Exception:
                    pass
    except Exception:
        pass
    return dict(result)

def load_app_totals_today() -> dict:
    ensure_csv()
    result: dict = defaultdict(int)
    today = datetime.now().date()
    try:
        with open(ACTIVITY_PATH, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    dt = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
                    if dt.date() == today:
                        result[row["app"]] += int(row["active_time"])
                except Exception:
                    pass
    except Exception:
        pass
    return dict(result)

def fmt_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"