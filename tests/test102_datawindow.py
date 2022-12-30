# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:51:35 2022

lunelukkio@gmail.com
"""

import unittest
from  SCANDATA.view.view_main import View, DataWindow
import tkinter as tk

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        
                
        root = tk.Tk()
        root.title("SCANDATA")
        self.view = DataWindow(root)
        
        self.view.mainloop()


if __name__ == '__main__':
    unittest.main()