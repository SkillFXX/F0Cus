import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from colors import app_color
from config import COLORS, APP_FONT
from data import (
    load_app_totals_today, load_settings, save_settings,
    load_activity_last_7_days, load_app_totals_7_days,
    fmt_time,
)
from widgets import BarChart, DonutChart, LegendItem

# Dashboard

class DashboardView(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"],
                         scrollbar_button_color=COLORS["border"],
                         scrollbar_button_hover_color=COLORS["surface2"],
                         **kwargs)
        self._build()

    def _build(self):
        for w in self.winfo_children():
            w.destroy()
        
        # Today activity infos
        ctk.CTkLabel(self, text="Activité — Aujourd'hui",
                     font=ctk.CTkFont(APP_FONT, 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(22, 2))
        ctk.CTkLabel(self, text="Votre temps d'écran de ce jour.",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=28, pady=(0, 16))
        
        leg_card = self._card(self)
        leg_card.pack(fill="x", padx=28, pady=(0, 14))
        ctk.CTkLabel(leg_card, text="Détail par application",
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 6))
        
        app_totals_today = load_app_totals_today()

        grid = ctk.CTkFrame(leg_card, fg_color="transparent")
        grid.pack(fill="x", padx=14, pady=(0, 10))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        sorted_apps = sorted(app_totals_today.items(), key=lambda x: x[1], reverse=True)
        for i, (app, secs) in enumerate(sorted_apps[:10]):
            cell = ctk.CTkFrame(grid, fg_color=COLORS["surface2"], corner_radius=8)
            cell.grid(row=i // 2, column=i % 2, padx=5, pady=4, sticky="ew") 
            LegendItem(cell, app, fmt_time(secs)).pack(fill="x", padx=10, pady=6)
            
        
        
        # 7 Last days activity infos

        ctk.CTkLabel(self, text="Activité — 7 derniers jours",
                     font=ctk.CTkFont(APP_FONT, 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(22, 2))
        ctk.CTkLabel(self, text="Vue d'ensemble de votre temps d'écran",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=28, pady=(0, 16))

        daily_data_7_days = load_activity_last_7_days()
        app_totals_7_days = load_app_totals_7_days()

            # Graphs
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=28, pady=(0, 14))

        bar_card = self._card(row)
        bar_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(bar_card, text="Activité quotidienne",
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 4))
        BarChart(bar_card, daily_data_7_days, width=500, height=190).pack(padx=12, pady=(0, 10))

        donut_card = self._card(row)
        donut_card.pack(side="right")
        ctk.CTkLabel(donut_card, text="Répartition",
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 4))
        DonutChart(donut_card, app_totals_7_days, size=190).pack(padx=16, pady=(0, 10))

        # Legends
        leg_card = self._card(self)
        leg_card.pack(fill="x", padx=28, pady=(0, 14))
        ctk.CTkLabel(leg_card, text="Détail par application",
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 6))

        grid = ctk.CTkFrame(leg_card, fg_color="transparent")
        grid.pack(fill="x", padx=14, pady=(0, 10))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        sorted_apps = sorted(app_totals_7_days.items(), key=lambda x: x[1], reverse=True)
        for i, (app, secs) in enumerate(sorted_apps[:10]):
            cell = ctk.CTkFrame(grid, fg_color=COLORS["surface2"], corner_radius=8)
            cell.grid(row=i // 2, column=i % 2, padx=5, pady=4, sticky="ew") 
            LegendItem(cell, app, fmt_time(secs)).pack(fill="x", padx=10, pady=6)

        ctk.CTkButton(self, text="↻  Actualiser",
                      font=ctk.CTkFont(APP_FONT, 12),
                      fg_color=COLORS["surface2"], hover_color=COLORS["border"],
                      text_color=COLORS["text"], corner_radius=8, width=130, height=32,
                      command=self._build).pack(anchor="e", padx=28, pady=(0, 20))

    @staticmethod
    def _card(parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent, fg_color=COLORS["surface"],
                            corner_radius=14, border_width=1,
                            border_color=COLORS["border"])


# Settings

class SettingsView(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg"],
                         scrollbar_button_color=COLORS["border"],
                         scrollbar_button_hover_color=COLORS["surface2"],
                         **kwargs)
        self._settings = load_settings()
        self._build()

    def _build(self):
        for w in self.winfo_children():
            w.destroy()
        self._settings = load_settings()

        ctk.CTkLabel(self, text="Paramètres",
                     font=ctk.CTkFont(APP_FONT, 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(22, 2))
        ctk.CTkLabel(self, text="Configuration générale de F0Cus",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=28, pady=(0, 16))

        gen = self._card(self)
        gen.pack(fill="x", padx=28, pady=(0, 12))
        ctk.CTkLabel(gen, text="Général",
                     font=ctk.CTkFont(APP_FONT, 13, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=16, pady=(12, 6))

        row_ri = ctk.CTkFrame(gen, fg_color="transparent")
        row_ri.pack(fill="x", padx=16, pady=(0, 12))
        ctk.CTkLabel(row_ri, text="Intervalle de rafraîchissement (secondes)",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        self._refresh_var = ctk.StringVar(
            value=str(self._settings.get("refresh_interval", 5)))
        ctk.CTkEntry(row_ri, textvariable=self._refresh_var, width=80,
                     font=ctk.CTkFont(APP_FONT, 12),
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"]).pack(side="right")

        rest = self._card(self)
        rest.pack(fill="x", padx=28, pady=(0, 12))

        hdr = ctk.CTkFrame(rest, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(12, 6))
        ctk.CTkLabel(hdr, text="Applications restreintes",
                     font=ctk.CTkFont(APP_FONT, 13, "bold"),
                     text_color=COLORS["accent"]).pack(side="left")
        ctk.CTkButton(hdr, text="+ Ajouter",
                      font=ctk.CTkFont(APP_FONT, 11),
                      fg_color=COLORS["accent"], hover_color="#3B6FE8",
                      corner_radius=8, height=28, width=90,
                      command=lambda: self._open_dialog()).pack(side="right")

        self._apps_frame = ctk.CTkFrame(rest, fg_color="transparent")
        self._apps_frame.pack(fill="x", padx=16, pady=(0, 12))
        self._render_apps()

        ctk.CTkButton(self, text="💾  Sauvegarder",
                      font=ctk.CTkFont(APP_FONT, 13, "bold"),
                      fg_color=COLORS["success"], hover_color="#22C55E",
                      text_color="#000", corner_radius=10, height=38,
                      command=self._save).pack(anchor="e", padx=28, pady=(4, 24))


    def _render_apps(self):
        for w in self._apps_frame.winfo_children():
            w.destroy()

        apps = self._settings.get("restricted_apps", [])
        if not apps:
            ctk.CTkLabel(self._apps_frame, text="Aucune application restreinte",
                         text_color=COLORS["text_muted"],
                         font=ctk.CTkFont(APP_FONT, 11)).pack(pady=6)
            return

        for idx, app in enumerate(apps):
            self._render_app_row(app, idx)

    def _render_app_row(self, app: dict, idx: int):
        row = ctk.CTkFrame(self._apps_frame, fg_color=COLORS["surface2"], corner_radius=8)
        row.pack(fill="x", pady=4)

        ctk.CTkLabel(row, text=app["name"],
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text"]).pack(side="left", padx=12, pady=8)

        is_kill = app.get("action") == "kill"
        ctk.CTkLabel(row,
                     text="💀 Kill" if is_kill else "🔔 Popup",
                     font=ctk.CTkFont(APP_FONT, 10),
                     text_color=COLORS["danger"] if is_kill else COLORS["warning"],
                     fg_color=COLORS["surface"], corner_radius=6,
                     width=70, height=22).pack(side="left", padx=8)

        ctk.CTkLabel(row, text=f"Limite : {fmt_time(app['limit'])}",
                     font=ctk.CTkFont(APP_FONT, 11),
                     text_color=COLORS["text_dim"]).pack(side="left", padx=4)

        if not is_kill:
            ctk.CTkLabel(row,
                         text=f"Rappel : {fmt_time(app.get('popup_frequency', 300))}",
                         font=ctk.CTkFont(APP_FONT, 11),
                         text_color=COLORS["text_dim"]).pack(side="left", padx=4)

        # boutons
        ctk.CTkButton(row, text="✕", width=28, height=28,
                      font=ctk.CTkFont(APP_FONT, 11),
                      fg_color=COLORS["danger"], hover_color="#DC2626",
                      corner_radius=6,
                      command=lambda i=idx: self._delete_app(i)).pack(side="right", padx=8)
        ctk.CTkButton(row, text="✏", width=28, height=28,
                      font=ctk.CTkFont(APP_FONT, 11),
                      fg_color=COLORS["surface"], hover_color=COLORS["border"],
                      text_color=COLORS["text_dim"], corner_radius=6,
                      command=lambda i=idx: self._open_dialog(edit_idx=i)).pack(side="right", padx=2)

    def _delete_app(self, idx: int):
        self._settings["restricted_apps"].pop(idx)
        self._render_apps()

    def _open_dialog(self, edit_idx=None):
        dlg = AppDialog(self, self._settings, edit_idx=edit_idx,
                        on_save=self._render_apps)
        dlg.grab_set()

    def _save(self):
        try:
            interval = int(self._refresh_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "L'intervalle doit être un entier.")
            return
        self._settings["refresh_interval"] = interval
        save_settings(self._settings)
        messagebox.showinfo("Sauvegardé", "Paramètres sauvegardés ✓")

    @staticmethod
    def _card(parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent, fg_color=COLORS["surface"],
                            corner_radius=14, border_width=1,
                            border_color=COLORS["border"])

class AppDialog(ctk.CTkToplevel):
    def __init__(self, master, settings: dict, edit_idx=None, on_save=None):
        super().__init__(master)
        self.title("Application restreinte")
        self.geometry("440x440")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["surface"])

        self._settings  = settings
        self._edit_idx  = edit_idx
        self._on_save   = on_save
        editing = settings["restricted_apps"][edit_idx] if edit_idx is not None else {}

        P = dict(padx=20, pady=6)

        ctk.CTkLabel(self, text="Nom de l'exécutable (.exe)",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", **P)
        self._name_var = ctk.StringVar(value=editing.get("name", ""))
        ctk.CTkEntry(self, textvariable=self._name_var,
                     placeholder_text="ex: chrome.exe",
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"],
                     font=ctk.CTkFont(APP_FONT, 12)).pack(fill="x", **P)

        ctk.CTkLabel(self, text="Limite de temps (secondes)",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", **P)
        self._limit_var = ctk.StringVar(value=str(editing.get("limit", 3600)))
        ctk.CTkEntry(self, textvariable=self._limit_var,
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"],
                     font=ctk.CTkFont(APP_FONT, 12)).pack(fill="x", **P)

        ctk.CTkLabel(self, text="Action en cas de dépassement",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", **P)
        self._action_var = ctk.StringVar(value=editing.get("action", "popup"))
        ctk.CTkSegmentedButton(self, values=["popup", "kill"],
                               variable=self._action_var,
                               font=ctk.CTkFont(APP_FONT, 12),
                               fg_color=COLORS["surface2"],
                               selected_color=COLORS["accent"],
                               command=self._toggle_freq).pack(fill="x", **P)

        self._freq_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._freq_frame.pack(fill="x")
        ctk.CTkLabel(self._freq_frame, text="Fréquence popup (secondes)",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(6, 2))
        self._freq_var = ctk.StringVar(value=str(editing.get("popup_frequency", 300)))
        ctk.CTkEntry(self._freq_frame, textvariable=self._freq_var,
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"],
                     font=ctk.CTkFont(APP_FONT, 12)).pack(fill="x", padx=20)

        self._toggle_freq(self._action_var.get())

        ctk.CTkButton(self, text="Enregistrer",
                      font=ctk.CTkFont(APP_FONT, 13, "bold"),
                      fg_color=COLORS["accent"], hover_color="#3B6FE8",
                      corner_radius=10, height=38,
                      command=self._save).pack(fill="x", padx=20, pady=20)

    def _toggle_freq(self, val: str):
        if val == "kill":
            self._freq_frame.pack_forget()
        else:
            self._freq_frame.pack(fill="x")

    def _save(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Nom requis.", parent=self)
            return
        try:
            limit = int(self._limit_var.get())
            freq  = int(self._freq_var.get()) if self._action_var.get() == "popup" else 300
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs numériques invalides.", parent=self)
            return

        entry = {"name": name, "limit": limit,
                 "action": self._action_var.get(), "popup_frequency": freq}

        if self._edit_idx is not None:
            self._settings["restricted_apps"][self._edit_idx] = entry
        else:
            self._settings["restricted_apps"].append(entry)

        if self._on_save:
            self._on_save()
        self.destroy()