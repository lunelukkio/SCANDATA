# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 22:31:27 2022

@author: lulul
"""
import unittest
from SCANDATA2.view.view_main import MainView
from SCANDATA2.controller.controller_main import ViewController
import tkinter as tk

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        
                
        root = tk.Tk()
        root.title("SCANDATA")
        self.view = MainView(root)
        self.view.controller = ViewController()
        
        self.view.mainloop()


if __name__ == '__main__':
    unittest.main()
