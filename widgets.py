import math
import tkinter as tk
from datetime import datetime, timedelta
from io import BytesIO

import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from colors import app_color
from config import COLORS, APP_FONT
from data import fmt_time, t


# Donut chart using matplotlib

class DonutChart(tk.Frame):
    def __init__(self, master, data: dict, size: int = 200, **kwargs):
        super().__init__(master, bg=COLORS["surface"], **kwargs)
        self.size = size
        self.data = data
        self._create_chart()

    def _create_chart(self):
        # Create figure with matplotlib
        fig = Figure(figsize=(self.size/100, self.size/100), dpi=100, 
                     facecolor=COLORS["surface"], edgecolor='none')
        ax = fig.add_subplot(111)
        
        filtered = {k: v for k, v in self.data.items() if v > 0}
        
        if not filtered:
            # Draw empty state
            ax.text(0.5, 0.5, t("no_data"), 
                   ha='center', va='center', 
                   color=COLORS["text_muted"],
                   fontsize=10, transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # Sort by value descending
            sorted_data = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
            labels = [app for app, _ in sorted_data]
            sizes = [val for _, val in sorted_data]
            colors = [app_color(app) for app in labels]
            
            # Create donut chart
            wedges, texts = ax.pie(sizes, labels=None, colors=colors,
                                   wedgeprops=dict(width=0.4, edgecolor=COLORS["surface"]),
                                   startangle=90)
            
            # Add center text
            total = sum(sizes)
            centre_circle = plt.Circle((0, 0), 0.70, fc=COLORS["surface"], 
                                       edgecolor='none')
            ax.add_artist(centre_circle)
            
            # Add text in center
            ax.text(0, 0.05, fmt_time(total), 
                   ha='center', va='center',
                   color=COLORS["text"],
                   fontsize=11, fontweight='bold')
            ax.text(0, -0.15, t("seven_days"),
                   ha='center', va='center',
                   color=COLORS["text_muted"],
                   fontsize=8)
        
        ax.axis('equal')
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.fig = fig
        self.canvas = canvas

    def draw(self, data: dict):
        """Update the chart with new data"""
        self.data = data
        # Clear the frame
        for widget in self.winfo_children():
            widget.destroy()
        plt.close(self.fig)
        # Recreate the chart
        self._create_chart()


# Bar chart using matplotlib

class BarChart(tk.Frame):
    def __init__(self, master, daily_data: dict,
                 width: int = 520, height: int = 200, **kwargs):
        super().__init__(master, bg=COLORS["surface"], **kwargs)
        self.width = width
        self.height = height
        self.daily_data = daily_data
        self._create_chart()

    def _create_chart(self):
        # Create figure
        fig = Figure(figsize=(self.width/100, self.height/100), dpi=100,
                     facecolor=COLORS["surface"], edgecolor='none')
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS["surface"])

        today = datetime.now()
        days_order = [(today - timedelta(days=6 - i)).strftime("%d/%m")
                      for i in range(7)]
        
        # Prepare data
        all_apps = set()
        for day_data in self.daily_data.values():
            all_apps.update(day_data.keys())
        all_apps = sorted(list(all_apps))
        
        # Build stacked bar data
        x_pos = np.arange(len(days_order))
        bottom = np.zeros(len(days_order))
        
        if not all_apps:
            ax.text(0.5, 0.5, t("no_data"),
                   ha='center', va='center',
                   color=COLORS["text_muted"],
                   fontsize=10, transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # Plot each app as a stack
            for app in all_apps:
                values = []
                for day in days_order:
                    day_data = self.daily_data.get(day, {})
                    values.append(day_data.get(app, 0))
                
                ax.bar(x_pos, values, bottom=bottom,
                      label=app, color=app_color(app),
                      width=0.6, edgecolor='none')
                
                # Add values to each segment
                for i, val in enumerate(values):
                    if val > 0:
                        bottom[i] += val
            
            # Set x-axis labels
            ax.set_xticks(x_pos)
            ax.set_xticklabels(days_order, fontsize=8)
            
            # Highlight today
            today_str = today.strftime("%d/%m")
            if today_str in days_order:
                today_idx = days_order.index(today_str)
                ax.get_xticklabels()[today_idx].set_color(COLORS["accent"])
                ax.get_xticklabels()[today_idx].set_fontweight('bold')
            
            # Format y-axis with time labels
            ax.yaxis.set_major_formatter(plt.FuncFormatter(
                lambda x, p: fmt_time(int(x))
            ))
            
            # Style
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(COLORS["border"])
            ax.spines['bottom'].set_color(COLORS["border"])
            
            ax.tick_params(axis='y', colors=COLORS["text_muted"], labelsize=7)
            ax.tick_params(axis='x', colors=COLORS["text_muted"], labelsize=8)
            
            # Grid
            ax.grid(axis='y', alpha=0.2, linestyle='--', color=COLORS["border"])
            ax.set_axisbelow(True)
        
        fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.fig = fig
        self.canvas = canvas

    def draw(self, daily_data: dict):
        """Update the chart with new data"""
        self.daily_data = daily_data
        # Clear the frame
        for widget in self.winfo_children():
            widget.destroy()
        plt.close(self.fig)
        # Recreate the chart
        self._create_chart()


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