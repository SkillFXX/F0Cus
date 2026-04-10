import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
import sqlite3
import csv

from config import (
    DEFAULT_SETTINGS, TRANSLATIONS, DEFAULT_LANGUAGE, DATABASE_PATH, APP_DIR
)

def migrate():        
    init_db()
    old_settings_path = os.path.join(APP_DIR, "settings.json")
    if os.path.exists(old_settings_path):
        log("Migrating settings...")
        try:
            with open(os.path.join(APP_DIR, "settings.json"), "r", encoding="utf-8") as f:
                old_settings = json.load(f)
            save_settings(old_settings)
            os.rename(old_settings_path, f"{old_settings_path}.bak")
            log("Settings successfully migrated.")
        except Exception as e:
            log(f"Error during parameter migration : {e}", "ERROR")
    
    old_activity_path = os.path.join(APP_DIR, "activity.csv")
    if os.path.exists(old_activity_path):
        try:
            with open(old_activity_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data_to_import = []
                for row in reader:
                    data_to_import.append((
                        row["date"],
                        row["app"],
                        int(row["active_time"]),
                        row["detected_activity"]
                    ))
                if data_to_import:
                    with get_connection() as conn:
                        cursor = conn.cursor()
                        cursor.executemany('''INSERT INTO activity (date, app, active_time, detected_activity)
                                              VALUES (?, ?, ?, ?)''', data_to_import)
                        conn.commit()
            os.rename(old_activity_path, f"{old_activity_path}.bak")
            log(f"{len(data_to_import)} activity entries migrated.")
        except Exception as e:
            log(f"Error during activity migration : {e}", "ERROR")

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATETIME, app TEXT, active_time INTEGER, detected_activity TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp DATETIME,level TEXT,message TEXT)")
        cursor.execute("PRAGMA db_version = 2")
        conn.commit()
        
def log(message, level = "INFO"):
    init_db() 
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), level.upper(), message))
            conn.commit()
    except Exception as e:
        print(f"CRITICAL: Unable to write the log : {e}")

def load_settings():
    init_db()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings")
            rows = cursor.fetchall()
            if not rows:
                save_settings(DEFAULT_SETTINGS)
                return DEFAULT_SETTINGS.copy()
            return {row[0]: json.loads(row[1]) for row in rows}
    except Exception:
        log("No settings could be loaded, loading default settings", "WARN")
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        for key, value in settings.items():
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, json.dumps(value)))
        conn.commit()

def commit_activity(app_name, active_time, detected_activity):
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO activity (date, app, active_time, detected_activity) VALUES (?, ?, ?, ?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  app_name, active_time, detected_activity))
        conn.commit()

def load_activity_last_7_days():
    init_db()
    result = defaultdict(lambda: defaultdict(int))
    cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT strftime('%d/%m', date) as day, app, SUM(active_time) FROM activity WHERE date >= ? GROUP BY day, app", (cutoff,))
        for day, app, total in cursor.fetchall():
            result[day][app] = total
    return result

def load_app_totals_7_days():
    init_db()
    cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT app, SUM(active_time) FROM activity WHERE date >= ? GROUP BY app", (cutoff,))
        return dict(cursor.fetchall())

def load_app_totals_today():
    init_db()
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT app, SUM(active_time) FROM activity WHERE date LIKE ? GROUP BY app", (f"{today}%",))
        return dict(cursor.fetchall())

def load_total_today():
    init_db()
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(active_time) FROM activity WHERE date LIKE ?", (f"{today}%",))
        res = cursor.fetchone()[0]
        return res if res else 0

def fmt_time(seconds):
    if seconds < 60: return f"{seconds}s"
    elif seconds < 3600: return f"{seconds // 60}m {seconds % 60}s"
    else: return f"{seconds // 3600}h {(seconds % 3600) // 60}m"
    
def load_user_language():
    settings = load_settings()
    language = settings.get("language", DEFAULT_LANGUAGE)
    return language if language in TRANSLATIONS else DEFAULT_LANGUAGE

def t(key):
    language = load_user_language()
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(key, key))

def load_available_language():
    return [lang.capitalize() for lang in TRANSLATIONS.keys()]