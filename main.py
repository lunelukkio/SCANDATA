# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:37:41 2022

@author: kenichi_miyazaki
This is the main program
"""


from model_package.model import Model
from view_package.view import View
from controller_package.controller import Controller
import tkinter as tk
import gc


class Main:
    def __init__(self):
        gc.collect()
        
        print('start the program')
        
        root = tk.Tk()
        root.title("SCANDATA")

        
        # Make instance of a model, a view and a controller
        self.model = Model()
        self.view = View(root)
        self.controller = Controller()
        
        # The view knows model and controller .
        self.view.model = self.model
        self.view.controller = self.controller
        
        # The controller knows model and view. 
        self.controller.model = self.model
        self.controller.view = self.view
        

        self.view.mainloop()

if __name__ == '__main__':
    scandata = Main()
