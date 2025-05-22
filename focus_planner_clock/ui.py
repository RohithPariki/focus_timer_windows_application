# ui.py
import tkinter as tk
from tkinter import ttk
style = ttk.Style()

style.configure("TaskCompleted.TLabel", foreground="gray", font=("Segoe UI", 10, "overstrike"))

def set_theme(root, dark_mode: bool):
    style = ttk.Style(root)
    # Use 'clam' theme for better styling options
    style.theme_use('clam')

    if dark_mode:
        bg = "#1e1e1e"
        fg = "#000000"
        accent = "#3a86ff"
        entry_bg = "#2e2e2e"
        btn_bg = "#3a3a3a"
    else:
        bg = "#000000"
        fg = "#073642"
        accent = "#268bd2"
        entry_bg = "#000000"
        btn_bg = "#000000"

    root.configure(bg=bg)

    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 13))
    style.configure("TButton",
                    background=btn_bg,
                    foreground=fg,
                    font=("Segoe UI", 12, "bold"),
                    padding=6)
    style.map("TButton",
              background=[('active', accent)])
    style.configure("TEntry",
                    fieldbackground=entry_bg,
                    foreground=fg,
                    font=("Segoe UI", 12),
                    padding=5)
    style.configure("TNotebook", background=bg, borderwidth=0)
    style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[12, 8])
    style.map("TNotebook.Tab",
              background=[("selected", accent)],
              foreground=[("selected", "#fff")])
