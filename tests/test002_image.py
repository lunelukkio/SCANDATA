# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 11:25:49 2022

@author: lulul
"""


import unittest
from SCANDATA.model.data_factory import CellImageFactory, FullFramesFactory
from SCANDATA.model.value_object import Filename, FramesData, ImageData
from SCANDATA.model.io_factory import TsmFileIOFactory
import numpy as np


filename = Filename('..\\220408\\20408B002.tsm')  # this is a value object

"""
class TestImageData(unittest.TestCase):
    def test_val(self):
        image = ImageData( np.empty((1, 1), dtype=float))
        print(image.data)
"""

class Testimage(unittest.TestCase):
    def test_cell_image(self):
        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename)
        rawdata, _ = io_data.get_data()
        interval, _ = io_data.get_infor()
        pixel_size = 0.25
        data = FramesData(rawdata)
        
        data_factory = FullFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        frames_data = fullframes.get_data()

        # image
        data_factory = CellImageFactory()
        
        cellimage = data_factory.create_data(frames_data)
        cellimage.update([0,0])
        cellimage.show_data()


if __name__ == '__main__':
    unittest.main()