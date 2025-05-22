# alarm.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import time
import os

try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

ALARM_SOUND = os.path.join("assets", "bell.mp3")

class AlarmFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.alarms = []  # list of datetime.time objects
        self.checking = False

        self.listbox = tk.Listbox(self, height=10, font=("Segoe UI", 12))
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        add_btn = ttk.Button(btn_frame, text="Add Alarm", command=self.add_alarm)
        add_btn.grid(row=0, column=0, padx=5)

        del_btn = ttk.Button(btn_frame, text="Delete Alarm", command=self.delete_alarm)
        del_btn.grid(row=0, column=1, padx=5)

        self.start_btn = ttk.Button(btn_frame, text="Start Checking", command=self.start_checking)
        self.start_btn.grid(row=0, column=2, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop Checking", command=self.stop_checking, state="disabled")
        self.stop_btn.grid(row=0, column=3, padx=5)

        self.refresh_listbox()

    def add_alarm(self):
        # Ask user for time input in HH:MM 24h format
        time_str = tk.simpledialog.askstring("Add Alarm", "Enter alarm time (HH:MM, 24-hour):")
        if not time_str:
            return
        try:
            alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            self.alarms.append(alarm_time)
            self.alarms.sort()
            self.refresh_listbox()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format.")

    def delete_alarm(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Delete Alarm", "No alarm selected!")
            return
        idx = selected[0]
        del self.alarms[idx]
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for alarm_time in self.alarms:
            self.listbox.insert(tk.END, alarm_time.strftime("%H:%M"))

    def start_checking(self):
        if not self.checking:
            self.checking = True
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="enabled")
            threading.Thread(target=self._check_alarms, daemon=True).start()

    def stop_checking(self):
        self.checking = False
        self.start_btn.config(state="enabled")
        self.stop_btn.config(state="disabled")

    def _check_alarms(self):
        while self.checking:
            now = datetime.datetime.now().time()
            for alarm_time in self.alarms[:]:
                # Check if current time matches alarm time (to the minute)
                if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                    self._trigger_alarm(alarm_time)
                    self.alarms.remove(alarm_time)
                    self.refresh_listbox()
            time.sleep(20)  # check every 20 seconds

    def _trigger_alarm(self, alarm_time):
        def show_alert():
            messagebox.showinfo("Alarm", f"Alarm for {alarm_time.strftime('%H:%M')}!")

        # Play sound if available
        if SOUND_AVAILABLE and os.path.exists(ALARM_SOUND):
            try:
                playsound(ALARM_SOUND)
            except Exception:
                pass

        # Show popup on main thread
        self.after(0, show_alert)
