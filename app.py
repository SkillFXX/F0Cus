import threading
import tkinter as tk

import customtkinter as ctk
import pystray                        
from PIL import Image, ImageDraw      

from config import COLORS, ICON_PATH, APP_FONT
from monitor import ActivityMonitor
from views import DashboardView, SettingsView
from widgets import LimitPopup

def _make_tray_icon() -> Image.Image:
    try:
        return Image.open(ICON_PATH).resize((64, 64))
    except Exception:
        img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((4, 4, 60, 60), fill="#5B8CFF")
        draw.text((18, 16), "F0", fill="white")
        return img

class F0CusApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("F0Cus")
        self.geometry("860x620")
        self.minsize(780, 540)
        self.configure(fg_color=COLORS["bg"])

        self._tray_icon: pystray.Icon | None = None # type: ignore | Seems to work
        self._monitor:   ActivityMonitor | None = None

        self._build_layout()
        self._show_view("dashboard")
        self._start_monitor()
        self._start_tray()

        self.protocol("WM_DELETE_WINDOW", self._hide_to_tray)

    def _build_layout(self):
        sidebar = ctk.CTkFrame(self, width=200, fg_color=COLORS["surface"],
                               corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo.pack(pady=(28, 32), padx=20)
        ctk.CTkLabel(logo, text="F0C",
                     font=ctk.CTkFont(APP_FONT, 28, "bold"),
                     text_color=COLORS["accent"]).pack(side="left")
        ctk.CTkLabel(logo, text="us",
                     font=ctk.CTkFont(APP_FONT, 28, "bold"),
                     text_color=COLORS["text"]).pack(side="left")

        self._nav_buttons: dict = {}
        for key, icon, label in [
            ("dashboard", "📊", "Tableau de bord"),
            ("settings",  "⚙",  "Paramètres"),
        ]:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {label}",
                font=ctk.CTkFont(APP_FONT, 13),
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS["surface2"],
                text_color=COLORS["text_dim"],
                corner_radius=10,
                height=42,
                command=lambda k=key: self._show_view(k),
            )
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_buttons[key] = btn

        # Indicateur monitoring
        ctk.CTkLabel(sidebar, text="F0Cus (v0.2.2) by Flow Studio",
                     font=ctk.CTkFont(APP_FONT, 9),
                     text_color=COLORS["text_muted"]).pack(side="bottom", pady=(0, 2))

        # Zone contenu
        self._content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self._content.pack(side="left", fill="both", expand=True)

    def _show_view(self, key: str):
        for k, btn in self._nav_buttons.items():
            btn.configure(
                fg_color=COLORS["surface2"] if k == key else "transparent",
                text_color=COLORS["accent"] if k == key else COLORS["text_dim"],
            )
        for w in self._content.winfo_children():
            w.destroy()

        if key == "dashboard":
            DashboardView(self._content).pack(fill="both", expand=True)
        elif key == "settings":
            SettingsView(self._content).pack(fill="both", expand=True)
     
    def _start_monitor(self):
        def popup_cb(app_name: str, total: int, limit: int):
            self.after(0, lambda: self.show_limit_popup(app_name, total, limit)) # I don't really understand but it works

        self._monitor = ActivityMonitor(popup_callback=popup_cb)
        self._monitor.start()

    def show_limit_popup(self, app_name: str, total: int, limit: int):
        LimitPopup(self, app_name, total, limit)

    def _start_tray(self):
        image = _make_tray_icon()

        menu = pystray.Menu(
            pystray.MenuItem("Ouvrir F0Cus", self._show_from_tray, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quitter",      self._quit_app),
        )
        self._tray_icon = pystray.Icon("F0Cus", image, "F0Cus — Monitoring actif", menu)

        threading.Thread(target=self._tray_icon.run, daemon=True).start()

    def _hide_to_tray(self):
        """Cache la fenêtre sans arrêter le monitoring."""
        self.withdraw()

    def _show_from_tray(self, icon=None, item=None):
        """Rappelle la fenêtre depuis le systray."""
        self.after(0, self._restore_window)

    def _restore_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def _quit_app(self, icon=None, item=None):
        """Arrêt propre : monitoring + systray + fenêtre."""
        if self._monitor:
            self._monitor.stop()
        if self._tray_icon:
            self._tray_icon.stop()
        self.after(0, self.destroy)