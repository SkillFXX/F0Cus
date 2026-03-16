import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from colors import app_color
from config import COLORS, APP_FONT, DEFAULT_LANGUAGE
from data import (
    load_app_totals_today, load_settings, save_settings,
    load_activity_last_7_days, load_app_totals_7_days,
    fmt_time, load_total_today, t, load_available_language
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
        ctk.CTkLabel(self, text=f"{t("activity")} — {t("today")}",
                     font=ctk.CTkFont(APP_FONT, 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(22, 2))
        ctk.CTkLabel(self, text=t("screen_time_today"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=28, pady=(0, 16))
        
        # Today screen time
        today_time = fmt_time(load_total_today())
        
        
        today_time_card = self._card(self)
        today_time_card.pack(fill="x", padx=28, pady=(0, 14))
        
        ctk.CTkLabel(today_time_card, text=t("time_spend_today"),
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 4))
        ctk.CTkLabel(today_time_card, text=f"{today_time}",
                     font=ctk.CTkFont(APP_FONT, 36, "bold"),
                     text_color=COLORS["text"]).pack(pady=(0, 12))
        
        # Today screen time per app
        leg_card = self._card(self)
        leg_card.pack(fill="x", padx=28, pady=(0, 14))
        ctk.CTkLabel(leg_card, text=t("details_per_app"),
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 6))
        
        app_totals_today = load_app_totals_today()

        apps_list = ctk.CTkFrame(leg_card, fg_color="transparent")
        apps_list.pack(fill="x", padx=14, pady=(0, 10))

        col1 = ctk.CTkFrame(apps_list, fg_color="transparent")
        col2 = ctk.CTkFrame(apps_list, fg_color="transparent")
        col1.pack(side="left", fill="both", expand=True, padx=(0, 5))
        col2.pack(side="left", fill="both", expand=True, padx=(5, 0))

        sorted_apps = sorted(app_totals_today.items(), key=lambda x: x[1], reverse=True)
        for i, (app, secs) in enumerate(sorted_apps[:10]):
            parent = col1 if i % 2 == 0 else col2
            cell = ctk.CTkFrame(parent, fg_color=COLORS["surface2"], corner_radius=8)
            cell.pack(fill="x", pady=4)
            LegendItem(cell, app, fmt_time(secs)).pack(fill="x", padx=10, pady=6)
            
        
        
        # 7 Last days activity infos

        ctk.CTkLabel(self, text=f"{t("activity")} — {t("last_7_days")}",
                     font=ctk.CTkFont(APP_FONT, 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(22, 2))
        ctk.CTkLabel(self, text=t("global_view_screen_time"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=28, pady=(0, 16))

        daily_data_7_days = load_activity_last_7_days()
        app_totals_7_days = load_app_totals_7_days()

            # Graphs
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=28, pady=(0, 14))

        bar_card = self._card(row)
        bar_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(bar_card, text=t("daily_activity"),
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 4))
        BarChart(bar_card, daily_data_7_days, width=500, height=190).pack(padx=12, pady=(0, 10))

        donut_card = self._card(row)
        donut_card.pack(side="right")
        ctk.CTkLabel(donut_card, text=t("distribution"),
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 4))
        DonutChart(donut_card, app_totals_7_days, size=190).pack(padx=16, pady=(0, 10))

        # Legends
        leg_card = self._card(self)
        leg_card.pack(fill="x", padx=28, pady=(0, 14))
        ctk.CTkLabel(leg_card, text=t("details_per_app"),
                     font=ctk.CTkFont(APP_FONT, 12, "bold"),
                     text_color=COLORS["text_dim"]).pack(anchor="w", padx=14, pady=(12, 6))

        apps_list = ctk.CTkFrame(leg_card, fg_color="transparent")
        apps_list.pack(fill="x", padx=14, pady=(0, 10))

        col1 = ctk.CTkFrame(apps_list, fg_color="transparent")
        col2 = ctk.CTkFrame(apps_list, fg_color="transparent")
        col1.pack(side="left", fill="both", expand=True, padx=(0, 5))
        col2.pack(side="left", fill="both", expand=True, padx=(5, 0))

        sorted_apps = sorted(app_totals_7_days.items(), key=lambda x: x[1], reverse=True)
        for i, (app, secs) in enumerate(sorted_apps[:10]):
            parent = col1 if i % 2 == 0 else col2
            cell = ctk.CTkFrame(parent, fg_color=COLORS["surface2"], corner_radius=8)
            cell.pack(fill="x", pady=4)
            LegendItem(cell, app, fmt_time(secs)).pack(fill="x", padx=10, pady=6)

        ctk.CTkButton(self, text=f"↻  {t("refresh")}",
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

        ctk.CTkLabel(self, text=t("settings"),
                     font=ctk.CTkFont(APP_FONT, 18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=28, pady=(22, 2))
        ctk.CTkLabel(self, text=t("general_settings"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text_muted"]).pack(anchor="w", padx=28, pady=(0, 16))

        gen = self._card(self)
        gen.pack(fill="x", padx=28, pady=(0, 12))
        ctk.CTkLabel(gen, text=t("general"),
                     font=ctk.CTkFont(APP_FONT, 13, "bold"),
                     text_color=COLORS["accent"]).pack(anchor="w", padx=16, pady=(12, 6))

        row_ri = ctk.CTkFrame(gen, fg_color="transparent")
        row_ri.pack(fill="x", padx=16, pady=(0, 12))

        # Language
        row_lang = ctk.CTkFrame(row_ri, fg_color="transparent")
        row_lang.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(row_lang, text=t("software_language"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        self._language_var = ctk.StringVar(value=self._settings.get("language", DEFAULT_LANGUAGE))
        ctk.CTkOptionMenu(row_lang, variable=self._language_var, width=80,
                     font=ctk.CTkFont(APP_FONT, 12),
                     fg_color=COLORS["surface2"], values=load_available_language()).pack(side="right")

        # Refresh interval
        row_refresh = ctk.CTkFrame(row_ri, fg_color="transparent")
        row_refresh.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(row_refresh, text=f"{t('update_time')} ({t('seconds')})",
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        self._refresh_var = ctk.StringVar(
            value=str(self._settings.get("refresh_interval", 5)))
        ctk.CTkEntry(row_refresh, textvariable=self._refresh_var, width=80,
                     font=ctk.CTkFont(APP_FONT, 12),
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"]).pack(side="right")

        ctk.CTkFrame(row_ri, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=10)

        # Daily limit enabler
        row_daily = ctk.CTkFrame(row_ri, fg_color="transparent")
        row_daily.pack(fill="x", pady=(0, 8))
        self._daily_limit_var = ctk.BooleanVar(value=self._settings.get("daily_limit", {}).get("enabled", False))
        ctk.CTkLabel(row_daily, text=t("enable_daily_limit"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkCheckBox(
            row_daily,
            text="",
            variable=self._daily_limit_var,
            command=self._toggle_daily_limit
        ).pack(side="right")

        # Daily limit frame
        self._daily_limit_frame = ctk.CTkFrame(row_ri, fg_color="transparent")
        self._daily_limit_frame.pack(fill="x")

        self._toggle_daily_limit()

        # Daily limit time
        self._daily_limit_time_var = ctk.StringVar(value=str(self._settings.get("daily_limit", {}).get("limit", 7200)))
        row_limit = ctk.CTkFrame(self._daily_limit_frame, fg_color="transparent")
        row_limit.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(row_limit, text=t("daily_limit_seconds"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkEntry(row_limit, textvariable=self._daily_limit_time_var, width=80,
                     font=ctk.CTkFont(APP_FONT, 12),
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"]).pack(side="right")

        # Daily limit action
        row_action = ctk.CTkFrame(self._daily_limit_frame, fg_color="transparent")
        row_action.pack(fill="x", pady=(0, 6))
        self._daily_limit_action_var = ctk.StringVar(value=self._settings["daily_limit"]["action"])
        ctk.CTkRadioButton(row_action, text=t("action_popup"), variable=self._daily_limit_action_var, value="popup").pack(side="left", padx=(0, 6))
        ctk.CTkRadioButton(row_action, text=t("action_shutdown"), variable=self._daily_limit_action_var, value="kill").pack(side="left")

        # Daily limit popup action
        row_popup = ctk.CTkFrame(self._daily_limit_frame, fg_color="transparent")
        row_popup.pack(fill="x", pady=(0, 6))
        self._daily_limit_popup_var = ctk.StringVar(value=str(self._settings.get("daily_limit", {}).get("popup_frequency", 600)))
        ctk.CTkLabel(row_popup, text=t("popup_frequency_seconds"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkEntry(row_popup, textvariable=self._daily_limit_popup_var, width=80,
                     font=ctk.CTkFont(APP_FONT, 12),
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"]).pack(side="right")
        
        
        # Restricted apps
        rest = self._card(self)
        rest.pack(fill="x", padx=28, pady=(0, 12))

        hdr = ctk.CTkFrame(rest, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(12, 6))
        ctk.CTkLabel(hdr, text=t("restricted_apps_label"),
                     font=ctk.CTkFont(APP_FONT, 13, "bold"),
                     text_color=COLORS["accent"]).pack(side="left")
        ctk.CTkButton(hdr, text=t("add_app_button"),
                      font=ctk.CTkFont(APP_FONT, 11),
                      fg_color=COLORS["accent"], hover_color="#3B6FE8",
                      corner_radius=8, height=28, width=90,
                      command=lambda: self._open_dialog()).pack(side="right")

        self._apps_frame = ctk.CTkFrame(rest, fg_color="transparent")
        self._apps_frame.pack(fill="x", padx=16, pady=(0, 12))
        self._render_apps()
        
        ctk.CTkButton(self, text=t("save_button"),
                      font=ctk.CTkFont(APP_FONT, 13, "bold"),
                      fg_color=COLORS["success"], hover_color="#22C55E",
                      text_color="#000", corner_radius=10, height=38,
                      command=self._save).pack(anchor="e", padx=28, pady=(4, 24))

    def _toggle_daily_limit(self):
        if self._daily_limit_var.get():
            self._daily_limit_frame.pack(fill="x")
        else:
            self._daily_limit_frame.pack_forget()

    def _render_apps(self):
        for w in self._apps_frame.winfo_children():
            w.destroy()

        apps = self._settings.get("restricted_apps", [])
        if not apps:
            ctk.CTkLabel(self._apps_frame, text=t("no_restricted_apps"),
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
                     text=t("kill_action") if is_kill else t("popup_action"),
                     font=ctk.CTkFont(APP_FONT, 10),
                     text_color=COLORS["danger"] if is_kill else COLORS["warning"],
                     fg_color=COLORS["surface"], corner_radius=6,
                     width=70, height=22).pack(side="left", padx=8)

        ctk.CTkLabel(row, text=f"{t('limit_word')} {fmt_time(app['limit'])}",
                     font=ctk.CTkFont(APP_FONT, 11),
                     text_color=COLORS["text_dim"]).pack(side="left", padx=4)

        if not is_kill:
            ctk.CTkLabel(row,
                         text=f"{t('reminder')} {fmt_time(app.get('popup_frequency', 300))}",
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
            daily_limit_enabled = self._daily_limit_var.get()
            daily_limit_time = int(self._daily_limit_time_var.get())
            daily_limit_action = self._daily_limit_action_var.get()
            daily_limit_popup_frequency = int(self._daily_limit_popup_var.get())
            language = self._language_var.get()
        except ValueError:
            messagebox.showerror(t("error"), t("invalid_values"))
            return
        self._settings["refresh_interval"] = interval
        self._settings["daily_limit"]["enabled"] = daily_limit_enabled
        self._settings["daily_limit"]["limit"] = daily_limit_time
        self._settings["daily_limit"]["action"] = daily_limit_action
        self._settings["daily_limit"]["popup_frequency"] = daily_limit_popup_frequency
        self._settings["language"] = language.lower()
        save_settings(self._settings)
        self._build()
        messagebox.showinfo(t("error"), t("settings_saved"))

    @staticmethod
    def _card(parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(parent, fg_color=COLORS["surface"],
                            corner_radius=14, border_width=1,
                            border_color=COLORS["border"])

class AppDialog(ctk.CTkToplevel):
    def __init__(self, master, settings: dict, edit_idx=None, on_save=None):
        super().__init__(master)
        self.title(t("restricted_app_title"))
        self.geometry("440x440")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["surface"])

        self._settings  = settings
        self._edit_idx  = edit_idx
        self._on_save   = on_save
        editing = settings["restricted_apps"][edit_idx] if edit_idx is not None else {}

        P = dict(padx=20, pady=6)

        ctk.CTkLabel(self, text=t("executable_name"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", **P)
        self._name_var = ctk.StringVar(value=editing.get("name", ""))
        ctk.CTkEntry(self, textvariable=self._name_var,
                     placeholder_text=t("example_exe"),
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"],
                     font=ctk.CTkFont(APP_FONT, 12)).pack(fill="x", **P)

        ctk.CTkLabel(self, text=t("time_limit_seconds"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", **P)
        self._limit_var = ctk.StringVar(value=str(editing.get("limit", 3600)))
        ctk.CTkEntry(self, textvariable=self._limit_var,
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"],
                     font=ctk.CTkFont(APP_FONT, 12)).pack(fill="x", **P)

        ctk.CTkLabel(self, text=t("action_on_exceed"),
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
        ctk.CTkLabel(self._freq_frame, text=t("popup_frequency_label"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(6, 2))
        self._freq_var = ctk.StringVar(value=str(editing.get("popup_frequency", 300)))
        ctk.CTkEntry(self._freq_frame, textvariable=self._freq_var,
                     fg_color=COLORS["surface2"], border_color=COLORS["border"],
                     text_color=COLORS["text"],
                     font=ctk.CTkFont(APP_FONT, 12)).pack(fill="x", padx=20)

        self._toggle_freq(self._action_var.get())

        ctk.CTkButton(self, text=t("save_app_button"),
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
            messagebox.showerror(t("error"), t("name_required"), parent=self)
            return
        try:
            limit = int(self._limit_var.get())
            freq  = int(self._freq_var.get()) if self._action_var.get() == "popup" else 300
        except ValueError:
            messagebox.showerror(t("error"), t("invalid_numeric_values"), parent=self)
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