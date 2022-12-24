# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import FramesData, FullFrames, ChFrames
from SCANDATA.model.io_factory import TsmFileIO

filename = '20408B002.tsm'
filepath = '..\\220408\\'




class TestFramesData(unittest.TestCase):
    def test_check_val(self):
        frames = FramesData()
        
        frames.check_val()

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        io_data = TsmFileIO(filename, filepath)
        data = io_data.full_frames
        interval = io_data.full_frame_interval
        pixel_size = 0.25
        
        data_factory = FullFramesFactory()

        fullframes = data_factory.create_data(data, interval, pixel_size)
        
        fullframes.print_infor()
        fullframes.show_data(1)
        fullframes.print_name()


if __name__ == '__main__':
    unittest.main()