# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import FramesData, FullFrames, ChFrames
from SCANDATA.model.io_factory import TsmFileIOFactory
import numpy as np

filename = '20408B002.tsm'
filepath = '..\\220408\\'



"""
class TestFramesData(unittest.TestCase):
    def test_val(self):
        frames = FramesData(np.empty((1, 1, 1), dtype=float))
        print(frames.frames_data)
"""

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename, filepath)
        data, _ = io_data.get_data()
        interval, _ = io_data.get_infor()

        pixel_size = 0.25
        
        data_factory = FullFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        
        fullframes.show_data(1)
        data = fullframes.get_data()[0]

if __name__ == '__main__':
    unittest.main()