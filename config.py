import os
import customtkinter as ctk

APP_FOLDER        = "F0Cus"
ACTIVITY_FILENAME = "activity.csv"
SETTINGS_FILENAME = "settings.json"
LOG_FILENAME      = "app.log"
ICON_FILENAME     = "icon.ico"

_appdata   = os.getenv("APPDATA", os.path.expanduser("~"))
APP_DIR    = os.path.join(_appdata, APP_FOLDER)
os.makedirs(APP_DIR, exist_ok=True)

ACTIVITY_PATH = os.path.join(APP_DIR, ACTIVITY_FILENAME)
SETTINGS_PATH = os.path.join(APP_DIR, SETTINGS_FILENAME)
LOG_PATH      = os.path.join(APP_DIR, LOG_FILENAME)
ICON_PATH     = os.path.join(os.path.dirname(__file__), ICON_FILENAME)

DEFAULT_SETTINGS: dict = {
    "refresh_interval": 5,
    "restricted_apps": [
        {"name": "Fortnite.exe", "limit": 1800, "action": "popup", "popup_frequency": 300},
        {"name": "netflix.exe",  "limit": 3600, "action": "popup", "popup_frequency": 600},
    ],
    "daily_limit": {"enabled": False, "limit": 7200, "action": "popup", "popup_frequency": 600},
}

COLORS: dict[str, str] = {
    "bg":         "#0D0F14",
    "surface":    "#13161E",
    "surface2":   "#1A1E2A",
    "border":     "#252A38",
    "accent":     "#5B8CFF",
    "text":       "#E8EAF0",
    "text_muted": "#6B7280",
    "text_dim":   "#9CA3AF",
    "success":    "#4ADE80",
    "warning":    "#FBBF24",
    "danger":     "#F87171",
}

APP_FONT = "Arial"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")