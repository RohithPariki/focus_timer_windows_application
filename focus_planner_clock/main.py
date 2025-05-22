import tkinter as tk
from tkinter import ttk

import todo
import pomodoro
import clock
import alarm
import countdown
import notes
import weather
import calendar_view
import study_tracker

class FocusPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Focus Planner Clock")
        self.geometry("900x600")
        self.configure(bg="#000000")

        self.sidebar = tk.Frame(self, bg="#2c3e50", width=180)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        self.frames = {}
        self.buttons = {}

        features = [
            ("To-Do", todo.TodoFrame),
            ("Pomodoro", pomodoro.PomodoroFrame),
            ("Clock", clock.ClockFrame),
            ("Alarm", alarm.AlarmFrame),
            ("Countdown", countdown.CountdownFrame),
            ("Notes", notes.NotesFrame),
            ("Weather", weather.WeatherFrame),
            ("Calendar", calendar_view.CalendarFrame),
            ("Study Tracker", study_tracker.StudyTrackerFrame),
        ]

        for i, (name, FrameClass) in enumerate(features):
            btn = tk.Button(self.sidebar, text=name, fg="white", bg="#34495e",
                            relief="flat", anchor="w", padx=10,
                            command=lambda n=name: self.show_frame(n))
            btn.pack(fill="x", pady=2)
            self.buttons[name] = btn

            frame = FrameClass(self.content)
            frame.place(relwidth=1, relheight=1)
            self.frames[name] = frame

        self.show_frame("To-Do")

    def show_frame(self, name):
        for fname, frame in self.frames.items():
            frame.lower()
            self.buttons[fname].configure(bg="#002447")
        self.frames[name].lift()
        self.buttons[name].configure(bg="#1abc9c")

if __name__ == "__main__":
    app = FocusPlannerApp()
    app.mainloop()
