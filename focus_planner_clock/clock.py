# clock.py
import tkinter as tk
from tkinter import ttk
import time

class ClockFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.width = 700
        self.height = 300

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, highlightthickness=0, bg="#121212")
        self.canvas.pack(fill="both", expand=True)

        self.font_family = "Segoe UI"
        self.font_size = 100
        self.font_color = "#00fff7"

        self.update_clock()

    def update_clock(self):
        self.canvas.delete("all")

        current_time = time.strftime("%H:%M:%S")
        x, y = self.width // 2, self.height // 2

        # Draw shadow/glow layers for cool effect
        shadow_colors = ["#00332d", "#005a4d", "#008060"]
        offsets = [6, 4, 2]

        for color, offset in zip(shadow_colors, offsets):
            self.canvas.create_text(
                x + offset, y + offset, text=current_time,
                font=(self.font_family, self.font_size, "bold"),
                fill=color
            )

        # Main bright text
        self.canvas.create_text(
            x, y, text=current_time,
            font=(self.font_family, self.font_size, "bold"),
            fill=self.font_color
        )

        self.after(200, self.update_clock)
