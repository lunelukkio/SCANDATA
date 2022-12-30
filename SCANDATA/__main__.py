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
        self.model = Experiments()
        self.view = View(root)
        self.controller = Controller()
        
        # The view knows controller .
        self.view.controller = self.controller
        
        # The controller knows model and view. 
        self.controller.model = self.model
        self.controller.view = self.view
        

        self.view.mainloop()

if __name__ == '__main__':
    scandata = Main()