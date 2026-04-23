import time
import threading
from collections import defaultdict
import subprocess

import psutil
import pyautogui
import win32gui
import win32process
from pynput import keyboard

from data import commit_activity, load_settings, load_total_today, log

class ActivityMonitor(threading.Thread):

    def __init__(self, popup_callback):
        super().__init__(daemon=True)

        self.stop_event = threading.Event()
        self.popup = popup_callback

        self.last_cursor = pyautogui.position()
        self.keys = []

        self.restricted_time = defaultdict(int)
        self.last_popup = defaultdict(float)
        self.last_daily_popup = 0

        self.start_keyboard_listener()

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                self.keys.append(key.char)
            except:
                self.keys.append(str(key))

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def get_active_app(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return psutil.Process(pid).name()
        except:
            log("Unable to retrieve the active application", "ERROR")
            return None

    def kill_app(self, name):
        for p in psutil.process_iter(["name"]):
            if p.info["name"] and p.info["name"].lower() == name.lower():
                try:
                    p.kill()
                except:
                    log("Unable to kill the application", "ERROR")
                    pass

    def run(self):

        while not self.stop_event.is_set():

            settings = load_settings()
            interval = settings.get("refresh_interval", 5)

            time.sleep(interval)

            cursor = pyautogui.position()

            if cursor != self.last_cursor:
                activity = "cursor_movement"
                self.last_cursor = cursor

            elif self.keys:
                activity = "keyboard_input"

            else:
                activity = None

            if not activity:
                continue

            app = self.get_active_app()
            if not app:
                continue

            commit_activity(app, interval, activity)

            # restricted apps
            for rule in settings.get("restricted_apps", []):

                if rule["name"].lower() != app.lower():
                    continue

                self.restricted_time[app] += interval

                total = self.restricted_time[app]
                limit = rule.get("limit", 3600)
                action = rule.get("action", "popup")
                freq = rule.get("popup_frequency", 300)

                if total < limit:
                    continue

                now = time.time()

                if action == "kill":
                    self.popup(app, total, limit)
                    self.kill_app(app)

                elif now - self.last_popup[app] >= freq:
                    self.last_popup[app] = now
                    self.popup(app, total, limit)

            # daily limit
            daily = settings.get("daily_limit", {})

            if daily.get("enabled", False):

                total_today = load_total_today()
                limit = daily.get("limit", 7200)
                action = daily.get("action", "popup")
                freq = daily.get("popup_frequency", 600)

                if total_today >= limit:

                    now = time.time()

                    if now - self.last_daily_popup >= freq:

                        self.last_daily_popup = now
                        self.popup(None, total_today, limit)

                    if action == "kill":
                        subprocess.run(["shutdown", "/s", "/t", "100"])

            self.keys.clear()

    def stop(self):
        self.stop_event.set()
        try:
            self.listener.stop()
        except:
            log("Unable to stop keyboard listening", "ERROR")
            pass