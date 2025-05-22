import tkinter as tk
from tkinter import filedialog

class NotesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')

        self.text_area = tk.Text(self, wrap='word', font=("Consolas", 12), bg="#fefefe", fg="#2c3e50")
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        self.toolbar = tk.Frame(self, bg='#ecf0f1')
        self.toolbar.pack(fill='x', side='bottom')

        save_btn = tk.Button(self.toolbar, text='💾 Save', command=self.save_note)
        save_btn.pack(side='left', padx=5, pady=5)

        load_btn = tk.Button(self.toolbar, text='📂 Load', command=self.load_note)
        load_btn.pack(side='left', padx=5, pady=5)

        clear_btn = tk.Button(self.toolbar, text='🗑 Clear', command=self.clear_note)
        clear_btn.pack(side='left', padx=5, pady=5)

    def save_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text_area.get("1.0", tk.END))

    def load_note(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, f.read())

    def clear_note(self):
        self.text_area.delete("1.0", tk.END)
