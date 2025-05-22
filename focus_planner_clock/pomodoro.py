# pomodoro.py
import tkinter as tk
from tkinter import ttk, messagebox

class PomodoroFrame(ttk.Frame):
    WORK_MIN = 25
    BREAK_MIN = 5

    def __init__(self, parent):
        super().__init__(parent)

        self.is_running = False
        self.is_work_time = True
        self.minutes = self.WORK_MIN
        self.seconds = 0
        self.timer_id = None

        self.label = ttk.Label(self, text=self._format_time(), font=("Segoe UI", 48, "bold"))
        self.label.pack(pady=30)

        self.status_label = ttk.Label(self, text="Work Time", font=("Segoe UI", 14))
        self.status_label.pack(pady=5)

        controls = ttk.Frame(self)
        controls.pack(pady=10)

        self.start_btn = ttk.Button(controls, text="Start", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.pause_btn = ttk.Button(controls, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = ttk.Button(controls, text="Reset", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=2, padx=5)

    def _format_time(self):
        return f"{self.minutes:02d}:{self.seconds:02d}"

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="enabled")
            self.count_down()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.after_cancel(self.timer_id)
            self.start_btn.config(state="enabled")
            self.pause_btn.config(state="disabled")

    def reset_timer(self):
        self.pause_timer()
        self.is_work_time = True
        self.minutes = self.WORK_MIN
        self.seconds = 0
        self.label.config(text=self._format_time())
        self.status_label.config(text="Work Time")

    def count_down(self):
        if self.is_running:
            if self.seconds == 0:
                if self.minutes == 0:
                    self.timer_done()
                    return
                else:
                    self.minutes -= 1
                    self.seconds = 59
            else:
                self.seconds -= 1

            self.label.config(text=self._format_time())
            self.timer_id = self.after(1000, self.count_down)

    def timer_done(self):
        self.is_running = False
        self.start_btn.config(state="enabled")
        self.pause_btn.config(state="disabled")

        # Alert popup
        if self.is_work_time:
            messagebox.showinfo("Pomodoro", "Work session complete! Time for a break.")
            self.is_work_time = False
            self.minutes = self.BREAK_MIN
            self.seconds = 0
            self.status_label.config(text="Break Time")
        else:
            messagebox.showinfo("Pomodoro", "Break over! Time to work.")
            self.is_work_time = True
            self.minutes = self.WORK_MIN
            self.seconds = 0
            self.status_label.config(text="Work Time")

        self.label.config(text=self._format_time())
