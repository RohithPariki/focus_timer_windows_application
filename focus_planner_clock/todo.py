import tkinter as tk
from tkinter import ttk
import json
import os

TASKS_FILE = "storage/tasks.json"

class TodoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tasks = []
        self.load_tasks()

        self.filter_var = tk.StringVar(value="All")
        self.editing_idx = None  # Index of task currently being edited (in filtered list)

        self.setup_styles()
        self.setup_ui()
        self.refresh_tasks()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TaskCompleted.TLabel", foreground="gray", font=("Segoe UI", 12, "overstrike"))

    def setup_ui(self):
        self.columnconfigure(0, weight=1)

        # Entry to add new tasks
        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.entry.bind("<Return>", self.add_task)

        # Filter buttons
        filter_frame = ttk.Frame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=10)
        for val in ("All", "Active", "Completed"):
            rb = ttk.Radiobutton(filter_frame, text=val, variable=self.filter_var, value=val, command=self.refresh_tasks)
            rb.pack(side="left", padx=5)

        # Scrollable task list container
        self.task_container = ttk.Frame(self)
        self.task_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.rowconfigure(2, weight=1)

        self.canvas = tk.Canvas(self.task_container, highlightthickness=0)
        self.task_frame = ttk.Frame(self.canvas)
        self.v_scroll = ttk.Scrollbar(self.task_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")

        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def add_task(self, event=None):
        task_text = self.entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.entry.delete(0, "end")
            self.save_tasks()
            self.refresh_tasks()

    def toggle_task(self, idx):
        real_idx = self.filtered_to_real_index(idx)
        self.tasks[real_idx]["completed"] = not self.tasks[real_idx]["completed"]
        self.save_tasks()
        self.refresh_tasks()

    def delete_task(self, idx):
        real_idx = self.filtered_to_real_index(idx)
        if self.editing_idx == idx:
            self.editing_idx = None
        del self.tasks[real_idx]
        self.save_tasks()
        self.refresh_tasks()

    def start_edit(self, idx):
        if self.editing_idx is not None:
            return
        self.editing_idx = idx
        self.refresh_tasks()

    def save_edit(self, idx, new_text):
        real_idx = self.filtered_to_real_index(idx)
        new_text = new_text.strip()
        if new_text:
            self.tasks[real_idx]["text"] = new_text
            self.save_tasks()
        self.editing_idx = None
        self.refresh_tasks()

    def refresh_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        filtered = self.get_filtered_tasks()

        for idx, task in enumerate(filtered):
            frame = ttk.Frame(self.task_frame)
            frame.pack(fill="x", pady=2)

            var = tk.BooleanVar(value=task["completed"])
            cb = ttk.Checkbutton(frame, variable=var, command=lambda i=idx: self.toggle_task(i))
            cb.pack(side="left")

            if idx == self.editing_idx:
                entry = ttk.Entry(frame)
                entry.insert(0, task["text"])
                entry.pack(side="left", fill="x", expand=True, padx=5)
                entry.focus_set()

                def save_and_exit(event=None):
                    self.save_edit(idx, entry.get())

                entry.bind("<Return>", save_and_exit)
                entry.bind("<FocusOut>", save_and_exit)
            else:
                lbl = ttk.Label(frame, text=task["text"])
                lbl.pack(side="left", fill="x", expand=True, padx=5)
                lbl.bind("<Double-Button-1>", lambda e, i=idx: self.start_edit(i))

                if task["completed"]:
                    lbl.configure(style="TaskCompleted.TLabel")

            del_btn = ttk.Button(frame, text="✕", width=2, command=lambda i=idx: self.delete_task(i))
            del_btn.pack(side="right")

    def get_filtered_tasks(self):
        filter_mode = self.filter_var.get()
        if filter_mode == "All":
            return self.tasks
        elif filter_mode == "Active":
            return [t for t in self.tasks if not t["completed"]]
        else:
            return [t for t in self.tasks if t["completed"]]

    def filtered_to_real_index(self, filtered_idx):
        filtered = self.get_filtered_tasks()
        target_task = filtered[filtered_idx]
        for i, task in enumerate(self.tasks):
            if task is target_task:
                return i
        return filtered_idx  # fallback

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)
