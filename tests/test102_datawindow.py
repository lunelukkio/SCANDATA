# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:51:35 2022

lunelukkio@gmail.com
"""

import unittest
from  SCANDATA2.view.view_main import DataWindow
from SCANDATA2.common_class import WholeFilename

import tkinter as tk

fullname = '..\\220408\\20408B002.tsm'
filename_obj = WholeFilename(fullname)

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
                
        root = tk.Tk()
        root.title("SCANDATA")
        view = DataWindow(root, filename_obj)
        root.mainloop()
        
        


if __name__ == '__main__':
    unittest.main()