import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar
from datetime import datetime

class CalendarFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.events = {}  # key: 'YYYY-MM-DD', value: list of event strings

        self.header = tk.Frame(self, bg='white')
        self.header.pack(pady=10)

        self.prev_btn = tk.Button(self.header, text='<', command=self.prev_month)
        self.prev_btn.pack(side='left', padx=10)

        self.month_year_label = tk.Label(self.header, text='', font=('Segoe UI', 16), bg='white')
        self.month_year_label.pack(side='left', padx=20)

        self.next_btn = tk.Button(self.header, text='>', command=self.next_month)
        self.next_btn.pack(side='left', padx=10)

        self.calendar_frame = tk.Frame(self, bg='white')
        self.calendar_frame.pack()

        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_year_label.config(text=f'{calendar.month_name[self.current_month]} {self.current_year}')

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            lbl = tk.Label(self.calendar_frame, text=day, font=('Segoe UI', 10, 'bold'), bg='white')
            lbl.grid(row=0, column=i, padx=5, pady=5)

        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        for r, week in enumerate(month_calendar, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    lbl = tk.Label(self.calendar_frame, text='', bg='white', width=4, height=2)
                    lbl.grid(row=r, column=c, padx=2, pady=2)
                else:
                    date_str = f'{self.current_year}-{self.current_month:02d}-{day:02d}'
                    btn = tk.Button(self.calendar_frame, text=str(day), width=4, height=2,
                                    command=lambda ds=date_str: self.add_event(ds))
                    btn.grid(row=r, column=c, padx=2, pady=2)

                    if date_str in self.events and self.events[date_str]:
                        btn.config(bg='#a3d2ca')

    def add_event(self, date_str):
        event_text = simpledialog.askstring("Add Event", f"Add event for {date_str}:")
        if event_text:
            self.events.setdefault(date_str, []).append(event_text)
            messagebox.showinfo("Event Added", f"Added event on {date_str}:\n{event_text}")
            self.draw_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.draw_calendar()
