# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:41:14 2022

lunelukkio@gmail.com
"""

    
from SCANDATA.view.view_main import MainView
from SCANDATA.controller.controller_main import MainController
import tkinter as tk
import gc


class Main:
    def __init__(self):
        gc.collect()
        
        print('start SCANDATA')
        
        root = tk.Tk()
        root.title("SCANDATA")

        # Make instance of a model, a view and a controller
        view = MainView(root)
        controller = MainController()
        
        # The view knows a model and controller .

        
        # The controller knows model and view. 
        controller.view = view
        

        root.mainloop()

if __name__ == '__main__':
    scandata = Main()