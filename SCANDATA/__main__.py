# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:41:14 2022

lunelukkio@gmail.com
"""

    
from SCANDATA.model.model_main import Experiments
from SCANDATA.view.view_main import View
from SCANDATA.controller.controller_main import Controller
import tkinter as tk
import gc


class Main:
    def __init__(self):
        gc.collect()
        
        print('start SCANDATA')
        
        root = tk.Tk()
        root.title("SCANDATA")

        # Make instance of a model, a view and a controller
        controller = Controller()
        model = Experiments()
        view = View(root)
        
        # The view knows controller .
        view.controller = controller
        
        # The controller knows model and view. 
        controller.model = model
        controller.view = view
        

        view.mainloop()

if __name__ == '__main__':
    scandata = Main()