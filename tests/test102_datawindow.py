# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:51:35 2022

lunelukkio@gmail.com
"""

import unittest
from  SCANDATA.view.view_main import View, DataWindow
from SCANDATA.controller.controller_main import Controller, WholeFilename
from SCANDATA.model.model_main import Experiments
import tkinter as tk

fullname = '..\\220408\\20408B002.tsm'
filename_obj = WholeFilename(fullname)

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
                
        root = tk.Tk()
        root.title("SCANDATA")
        
        controller = Controller()
        controller.model = Experiments()
        controller.model.create_data_set(fullname)

        view = DataWindow(root, filename_obj, controller)
        view.initialize()
        
        view.mainloop()


if __name__ == '__main__':
    unittest.main()