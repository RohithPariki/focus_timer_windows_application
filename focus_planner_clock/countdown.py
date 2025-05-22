# countdown.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime

class CountdownFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.target_datetime = None
        self.timer_id = None

        self.label = ttk.Label(self, text="No countdown set", font=("Segoe UI", 24))
        self.label.pack(pady=40)

        btn_frame = ttk.Frame(self)
        btn_frame.pack()

        set_btn = ttk.Button(btn_frame, text="Set Countdown", command=self.set_countdown)
        set_btn.grid(row=0, column=0, padx=5)

        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_countdown)
        reset_btn.grid(row=0, column=1, padx=5)

    def set_countdown(self):
        # Ask user for target date and time (YYYY-MM-DD HH:MM)
        input_str = tk.simpledialog.askstring("Set Countdown", "Enter target date and time (YYYY-MM-DD HH:MM):")
        if not input_str:
            return
        try:
            self.target_datetime = datetime.datetime.strptime(input_str, "%Y-%m-%d %H:%M")
            if self.target_datetime <= datetime.datetime.now():
                messagebox.showerror("Invalid Date", "Please enter a future date and time.")
                self.target_datetime = None
                return
            self.update_countdown()
        except ValueError:
            messagebox.showerror("Invalid Format", "Please use format YYYY-MM-DD HH:MM.")

    def reset_countdown(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.target_datetime = None
        self.label.config(text="No countdown set")

    def update_countdown(self):
        if not self.target_datetime:
            return

        now = datetime.datetime.now()
        diff = self.target_datetime - now

        if diff.total_seconds() <= 0:
            self.label.config(text="Time's up!")
            messagebox.showinfo("Countdown", "The countdown has finished!")
            self.target_datetime = None
            return

        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        self.label.config(text=f"Time remaining: {days}d {hours}h {minutes}m")
        self.timer_id = self.after(60000, self.update_countdown)  # update every minute
