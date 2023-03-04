import psutil
import tkinter as tk
from tkinter.ttk import Progressbar

class MemoryUsageProgressBar(Progressbar):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.maximum = psutil.virtual_memory().total
        self.update_memory_usage()

    def update_memory_usage(self):
        memory_usage = psutil.Process().memory_info().rss
        self.configure(value=memory_usage, maximum=self.maximum)
        self.after(1000, self.update_memory_usage)

root = tk.Tk()
MemoryUsageProgressBar(master=root, length=200, mode="determinate").pack()
root.mainloop()