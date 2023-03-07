
from tkinter import ttk
import tkinter as tk

root = tk.Tk()

combo = ttk.Combobox(root, values=["Item 1", "Item 2", "Item 3"])
combo.current(2)
combo.pack()

root.mainloop()