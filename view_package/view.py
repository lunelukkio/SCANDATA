# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""

import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    def __init__(self):
        print('imported view')
        self.model = None
        self.controller = None

        root = tk.Tk()
        root.title("SCANDATA")
        main = MainWindow(self.controller, master = root)
        main.mainloop()
        #no programs are running after mainloop
        

class MainWindow(View):
    def __init__(self, controller, master=None):
        super().__init__(master)
        self.controller = controller



if __name__ == "__main__":
    test = View()