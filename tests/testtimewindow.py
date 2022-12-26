# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 00:06:40 2022

@author: lulul
"""



import unittest
from SCANDATA.model.controller_factory import RoiFactory, FrameWindowFactory
from SCANDATA.model.controller_factory import Roi, FrameWindow, FrameWindowVal
from SCANDATA.model.data_factory import CellImageFactory, FullFramesFactory
from SCANDATA.model.data_factory import ImageData
from SCANDATA.model.io_factory import TsmFileIO
import numpy as np

filename = '20408B002.tsm'
filepath = '..\\220408\\'

"""
class TestFrameWindowVal(unittest.TestCase):
    def test_check_val(self):
        framewindowval = FrameWindowVal()
        framewindowval.frame_window_val = [2,5]
        print('time_window_val test')
        print(framewindowval.frame_window_val)
"""

class TestRoiFrameWindow(unittest.TestCase):
    def test_FrameWindow(self):

        io_data = TsmFileIO(filename, filepath)
        data = io_data.full_frames
        interval = io_data.full_frame_interval
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
        cellimage.show_data()
        
        framewindow.add_data(0,0,8,1)
        cellimage.show_data()

        


if __name__ == '__main__':
    unittest.main()