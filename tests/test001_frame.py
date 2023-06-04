# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.value_object import Filename,FramesData
from SCANDATA.model.repository import DataRepository

filename = Filename('..\\220408\\20408B002.tsm')  # this isa a value object

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        
        repository = DataRepository(filename)
        rawdata = repository.original_data_3d[0]
        interval = repository.original_data_infor[0]
        data = FramesData(rawdata)
        pixel_size = 0.25
        
        data_factory = FullFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        
        fullframes.show_data(8)


if __name__ == '__main__':
    unittest.main()