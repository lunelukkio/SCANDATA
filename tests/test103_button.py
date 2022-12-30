# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 21:50:02 2022

lunelukkio@gmail.com
"""

import unittest
import tkinter as tk
import tkinter.filedialog
from  SCANDATA.view.view_main import ButtonFn

fullname = '..\\220408\\20408B002.tsm'

class TestFullFrames(unittest.TestCase):
    def test_get_whole_name(self):

        root = tk.Tk()       
        button = ButtonFn(Controller_test())
        wholename = button.menu_open_click(fullname)
        print(wholename)
        root.destroy()
        
class Controller_test:
    pass


if __name__ == '__main__':
    unittest.main()