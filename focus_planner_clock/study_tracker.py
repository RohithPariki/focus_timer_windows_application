import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json
import os

class StudyTrackerFrame(tk.Frame):
    DATA_FILE = "study_tracker_data.json"

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.study_sessions = {}  # key: 'YYYY-MM-DD', value: minutes studied

        self.load_data()

        self.title_label = tk.Label(self, text="Study Tracker", font=("Segoe UI", 18, "bold"), bg="white")
        self.title_label.pack(pady=10)

        self.date_label = tk.Label(self, text=date.today().strftime("%A, %B %d, %Y"), font=("Segoe UI", 12), bg="white")
        self.date_label.pack()

        self.progress_label = tk.Label(self, text="Today's Study Progress:", font=("Segoe UI", 12), bg="white")
        self.progress_label.pack(pady=(20, 5))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate", variable=self.progress_var, maximum=240)  # Max 4 hours
        self.progress_bar.pack(pady=5)

        self.progress_text = tk.Label(self, text="0 / 240 minutes", font=("Segoe UI", 10), bg="white")
        self.progress_text.pack()

        self.add_session_frame = tk.Frame(self, bg="white")
        self.add_session_frame.pack(pady=20)

        tk.Label(self.add_session_frame, text="Add Study Session (minutes):", bg="white", font=("Segoe UI", 12)).pack(side="left", padx=5)
        self.minutes_entry = tk.Entry(self.add_session_frame, width=5, font=("Segoe UI", 12))
        self.minutes_entry.pack(side="left", padx=5)
        self.add_btn = tk.Button(self.add_session_frame, text="Add", command=self.add_session)
        self.add_btn.pack(side="left", padx=5)

        self.session_log_label = tk.Label(self, text="Today's Sessions:", font=("Segoe UI", 12, "underline"), bg="white")
        self.session_log_label.pack(pady=(20, 5))

        self.sessions_listbox = tk.Listbox(self, width=50, height=8, font=("Segoe UI", 10))
        self.sessions_listbox.pack()

        self.refresh_ui()

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    self.study_sessions = json.load(f)
            except Exception:
                self.study_sessions = {}

    def save_data(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.study_sessions, f, indent=4)

    def add_session(self):
        minutes_text = self.minutes_entry.get()
        if not minutes_text.isdigit():
            messagebox.showerror("Invalid input", "Please enter a valid number of minutes.")
            return
        minutes = int(minutes_text)
        if minutes <= 0:
            messagebox.showerror("Invalid input", "Please enter a positive number of minutes.")
            return

        today_str = date.today().isoformat()
        self.study_sessions.setdefault(today_str, [])
        self.study_sessions[today_str].append(minutes)
        self.save_data()
        self.minutes_entry.delete(0, tk.END)
        self.refresh_ui()

    def refresh_ui(self):
        today_str = date.today().isoformat()
        sessions = self.study_sessions.get(today_str, [])
        total = sum(sessions)

        self.progress_var.set(min(total, 240))
        self.progress_text.config(text=f"{total} / 240 minutes")

        self.sessions_listbox.delete(0, tk.END)
        for i, session in enumerate(sessions, 1):
            self.sessions_listbox.insert(tk.END, f"Session {i}: {session} minutes")
