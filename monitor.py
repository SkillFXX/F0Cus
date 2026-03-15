import time
import threading
from collections import defaultdict

import psutil
import pyautogui
import win32gui       # type: ignore
import win32process   # type: ignore
from pynput import keyboard

from data import commit_activity, load_settings


class ActivityMonitor(threading.Thread):

    def __init__(self, popup_callback):
        super().__init__(daemon=True)
        self._stop_event      = threading.Event()
        self._popup_callback  = popup_callback

        self._last_cursor     = pyautogui.position()
        self._keys: list      = []

        self._restricted_timers: dict = defaultdict(int)
        self._last_popup_ts: dict     = defaultdict(float)

        self._start_keyboard_listener()


    def _start_keyboard_listener(self):
        def on_press(key):
            try:
                self._keys.append(key.char)
            except AttributeError:
                self._keys.append(str(key))

        self._kb_listener = keyboard.Listener(on_press=on_press)
        self._kb_listener.start()


    def get_active_app(self) -> str | None:
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return psutil.Process(pid).name()
        except Exception:
            return None

    def _check_restricted(self, app_name: str, elapsed: int):
        settings = load_settings()
        for rule in settings.get("restricted_apps", []):
            if rule["name"].lower() != app_name.lower():
                continue

            self._restricted_timers[app_name] += elapsed
            total  = self._restricted_timers[app_name]
            limit  = rule.get("limit", 3600)
            action = rule.get("action", "popup")
            freq   = rule.get("popup_frequency", 300)

            if total < limit:
                continue

            if action == "kill":
                self._popup_callback(app_name, total, limit)
                self._kill_app(app_name)
            else:
                now = time.time()
                if now - self._last_popup_ts[app_name] >= freq:
                    self._last_popup_ts[app_name] = now
                    self._popup_callback(app_name, total, limit)

    def _kill_app(self, app_name: str):
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and proc.info["name"].lower() == app_name.lower():
                try:
                    proc.kill()
                except Exception:
                    pass

    def run(self):
        while not self._stop_event.is_set():
            settings = load_settings()
            interval = settings.get("refresh_interval", 5)
            time.sleep(interval)

            cursor = pyautogui.position()
            if cursor != self._last_cursor:
                detected = "cursor_movement"
                self._last_cursor = cursor
            elif self._keys:
                detected = "keyboard_input"
            else:
                detected = None

            if detected:
                app = self.get_active_app()
                if app:
                    commit_activity(app, interval, detected)
                    self._check_restricted(app, interval)
                self._keys.clear()

    def stop(self):
        self._stop_event.set()
        try:
            self._kb_listener.stop()
        except Exception:
            pass