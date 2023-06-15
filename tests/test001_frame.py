# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.data_factory import FluoFramesFactory
from SCANDATA.model.value_object import Filename,FramesData
from SCANDATA.model.repository import DataRepository

filename = Filename('..\\220408\\20408B002.tsm')  # this isa a value object

class TestFullFrames(unittest.TestCase):
    def test_full_frame(self):
        data_channel = 0  # 0:fullFrames 1,2: chFrames
        repository = DataRepository(filename)
        rawdata = repository.original_data_3d[data_channel]  
        interval = repository.original_data_infor[data_channel]  # 0:fullFrames interval 1,2: chFrames interval
        data = FramesData(rawdata)
        pixel_size = 0.25
        
        data_factory = FluoFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        
        fullframes.show_data(8)


if __name__ == '__main__':
    unittest.main()