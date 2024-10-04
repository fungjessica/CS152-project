#references: 
#https://www.pythonguis.com/tutorials/create-gui-tkinter/

import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        root.title("Grocery To-do List")
        root.configure(background="white")
        root.minsize(400,400)
        root.maxsize(800,800)
        root.geometry("300x300+50+50")

        text = tk.Label(self.root, text="Grocery To-do List")
        text.pack(pady=10)

        text2 = tk.Label(self.root, text = "Add")
        text2.pack(pady=10)

        task_entry = tk.Entry(self.root, width=25)
        task_entry.pack(pady=10)

        task_listbox = tk.Listbox(self.root, width=40, height=10)
        task_listbox.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()