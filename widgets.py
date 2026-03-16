import math
import tkinter as tk
from datetime import datetime, timedelta

import customtkinter as ctk

from colors import app_color
from config import COLORS, APP_FONT
from data import fmt_time, t


# Donut chart by Sonnet 4.6

class DonutChart(tk.Canvas):
    def __init__(self, master, data: dict, size: int = 200, **kwargs):
        super().__init__(master, width=size, height=size,
                         bg=COLORS["surface"], highlightthickness=0, **kwargs)
        self._size = size
        self.draw(data)

    def draw(self, data: dict):
        self.delete("all")
        filtered = {k: v for k, v in data.items() if v > 0}
        if not filtered:
            self._draw_empty()
            return

        total  = sum(filtered.values())
        cx, cy = self._size / 2, self._size / 2
        R_out  = self._size * 0.42
        R_in   = self._size * 0.26
        GAP    = 1.5   # demi-espace en degrés entre chaque segment

        start = -90.0
        for name, value in sorted(filtered.items(), key=lambda x: x[1], reverse=True):
            sweep = (value / total) * 360.0
            gap   = GAP if sweep > GAP * 4 else 0
            self._draw_segment(cx, cy, R_in, R_out,
                                start + gap, sweep - gap * 2,
                                app_color(name))
            start += sweep

        # Trou central
        self.create_oval(cx - R_in, cy - R_in, cx + R_in, cy + R_in,
                         fill=COLORS["surface"], outline="")
        # Texte central
        self.create_text(cx, cy - 9, text=fmt_time(total),
                         fill=COLORS["text"], font=(APP_FONT, 11, "bold"))
        self.create_text(cx, cy + 9, text=t("seven_days"),
                         fill=COLORS["text_muted"], font=(APP_FONT, 8))

    def _draw_segment(self, cx, cy, r_in, r_out, start_deg, sweep_deg, color):
        if abs(sweep_deg) < 0.2:
            return
        steps = max(4, int(abs(sweep_deg) / 2))
        pts = []
        for i in range(steps + 1):
            a = math.radians(start_deg + sweep_deg * i / steps)
            pts += [cx + r_out * math.cos(a), cy + r_out * math.sin(a)]
        for i in range(steps + 1):
            a = math.radians(start_deg + sweep_deg * (steps - i) / steps)
            pts += [cx + r_in * math.cos(a), cy + r_in * math.sin(a)]
        self.create_polygon(pts, fill=color, outline="", smooth=False)

    def _draw_empty(self):
        cx, cy = self._size / 2, self._size / 2
        r = self._size * 0.42
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         outline=COLORS["border"], width=2, fill="")
        self.create_text(cx, cy, text=t("no_data"),
                         fill=COLORS["text_muted"], font=(APP_FONT, 9),
                         justify="center")


# Bar chart by Sonnet 4.6

class BarChart(tk.Canvas):

    def __init__(self, master, daily_data: dict,
                 width: int = 520, height: int = 200, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg=COLORS["surface"], highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.draw(daily_data)

    def draw(self, daily_data: dict):
        self.delete("all")

        PAD_L, PAD_R, PAD_T, PAD_B = 52, 16, 18, 36
        draw_w = self.width - PAD_L - PAD_R
        draw_h = self.height - PAD_T - PAD_B

        today      = datetime.now()
        days_order = [(today - timedelta(days=6 - i)).strftime("%d/%m")
                      for i in range(7)]

        max_val = max(
            (sum(daily_data.get(d, {}).values()) for d in days_order),
            default=1
        ) or 1

        # Axes
        self.create_line(PAD_L, PAD_T, PAD_L, PAD_T + draw_h,
                         fill=COLORS["border"], width=1)
        self.create_line(PAD_L, PAD_T + draw_h, PAD_L + draw_w, PAD_T + draw_h,
                         fill=COLORS["border"], width=1)

        # Y-ticks
        for pct in (0.25, 0.5, 0.75, 1.0):
            y = PAD_T + draw_h - pct * draw_h
            self.create_line(PAD_L, y, PAD_L + draw_w, y,
                             fill=COLORS["border"], dash=(2, 5), width=1)
            self.create_text(PAD_L - 4, y, text=fmt_time(int(max_val * pct)),
                             fill=COLORS["text_muted"], font=(APP_FONT, 6),
                             anchor="e")

        bar_w   = draw_w / 7
        spacing = bar_w * 0.15

        for i, day in enumerate(days_order):
            apps_day = daily_data.get(day, {})
            x0 = PAD_L + i * bar_w + spacing
            x1 = PAD_L + (i + 1) * bar_w - spacing
            y  = PAD_T + draw_h

            for app_name, secs in sorted(apps_day.items(), key=lambda x: x[1]):
                if secs <= 0:
                    continue
                bar_h = max((secs / max_val) * draw_h, 1.5)
                self.create_rectangle(x0, y - bar_h, x1, y,
                                      fill=app_color(app_name), outline="")
                y -= bar_h

            is_today = (day == today.strftime("%d/%m"))
            self.create_text((x0 + x1) / 2, PAD_T + draw_h + 14,
                             text=day,
                             fill=COLORS["accent"] if is_today else COLORS["text_muted"],
                             font=(APP_FONT, 7))


class LegendItem(ctk.CTkFrame):
    def __init__(self, master, app_name: str, value_str: str, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        color = app_color(app_name)

        dot = tk.Canvas(self, width=12, height=12,
                        bg=COLORS["surface2"], highlightthickness=0)
        dot.create_oval(1, 1, 11, 11, fill=color, outline="")
        dot.pack(side="left", padx=(0, 7))

        ctk.CTkLabel(self, text=app_name,
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkLabel(self, text=value_str,
                     font=ctk.CTkFont(APP_FONT, 11),
                     text_color=COLORS["text_muted"]).pack(side="right", padx=(10, 0))

class LimitPopup(ctk.CTkToplevel):

    def __init__(self, master, app_name: str, total: int, limit: int):
        super().__init__(master)
        self.title(t("time_exceeded"))
        self.geometry("380x230")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["surface"])
        self.attributes("-topmost", True)

        ctk.CTkLabel(self, text=t("time_exceeded"),
                     font=ctk.CTkFont(APP_FONT, 17, "bold"),
                     text_color=COLORS["danger"]).pack(pady=(24, 6))
        ctk.CTkLabel(self,
                     text=(f"Vous avez utilisé {app_name}\n"
                           f"pendant {fmt_time(total)}  (limite : {fmt_time(limit)})"),
                     font=ctk.CTkFont(APP_FONT, 12),
                     text_color=COLORS["text"], justify="center").pack(pady=8)
        ctk.CTkLabel(self, text=t("take_a_break"),
                     font=ctk.CTkFont(APP_FONT, 11),
                     text_color=COLORS["text_muted"]).pack(pady=4)
        ctk.CTkButton(self, text=t("ok_understood"),
                      font=ctk.CTkFont(APP_FONT, 12, "bold"),
                      fg_color=COLORS["danger"], hover_color="#DC2626",
                      corner_radius=10, height=36,
                      command=self.destroy).pack(pady=16)