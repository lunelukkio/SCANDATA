# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 00:06:40 2022

@author: lulul
"""



import unittest
from SCANDATA.model.controller_factory import FrameWindowFactory
from SCANDATA.model.controller_factory import FrameWindow, FrameWindowVal
from SCANDATA.model.data_factory import CellImageFactory, FullFramesFactory
from SCANDATA.model.data_factory import ImageData
from SCANDATA.model.io_factory import TsmFileIOFactory
import numpy as np
import matplotlib.pyplot as plt

filename = '20408B002.tsm'
filepath = '..\\220408\\'

"""
class TestFrameWindowVal(unittest.TestCase):
    def test_check_val(self):
        framewindowval = FrameWindowVal()
        framewindowval.frame_window_val = [2,5]
        print(framewindowval.frame_window_val)
"""

class TestFrameWindow(unittest.TestCase):
    def test_FrameWindow(self):

        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename, filepath)
        

        data, _ = io_data.get_data()
        interval, _ = io_data.get_infor()
        pixel_size = 0.25
        
        data_factory = FullFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        frames_data, _, _, _ = fullframes.get_data()
        
        data_factory = CellImageFactory()
        cellimage = data_factory.create_data(frames_data, [0,3], pixel_size)
        
        controller_factory = FrameWindowFactory()

        framewindow = controller_factory.create_model_controller()
        framewindow.add_observer(cellimage)
        framewindow.set_data(0,0,1,1)
        a = plt.figure()
        cellimage.show_data()
        
        framewindow.add_data(1,40)
        b = plt.figure()
        cellimage.show_data()
        framewindow.reset()
        c = plt.figure()
        cellimage.show_data()

        


if __name__ == '__main__':
    unittest.main()