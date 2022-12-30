# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 22:31:27 2022

@author: lulul
"""
import unittest
from SCANDATA.view.view_main import View
from SCANDATA.controller.controller_main import Controller
import tkinter as tk

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        
                
        root = tk.Tk()
        root.title("SCANDATA")
        self.view = View(root)
        self.view.controller = Controller()
        
        self.view.mainloop()


if __name__ == '__main__':
    unittest.main()
