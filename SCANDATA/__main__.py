# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:41:14 2022

lunelukkio@gmail.com
"""

    
from SCANDATA.view.view_main import MainView
import tkinter as tk
import gc


class Main:
    def __init__(self):
        gc.collect()
        
        print('start SCANDATA')
        
        root = tk.Tk()
        root.title("SCANDATA")

        view = MainView(root)

        root.mainloop()

if __name__ == '__main__':
    scandata = Main()