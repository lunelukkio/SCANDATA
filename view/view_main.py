# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""

import tkinter as tk
import view.gui_view
from tkinter import ttk



class View(tk.Tk):
    def __init__(self, controller):
        print('imported view')
        self.controller = controller

        root = tk.Tk()
        root.title("SCANDATA")
        main = view.gui_view.MainWindow(master = root)
        main.mainloop()
        #no programs are running after mainloop

    def main(self):
        print('In main of veiw')

if __name__ == "__main__":
    pass
