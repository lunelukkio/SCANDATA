# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 11:25:49 2022

@author: lulul
"""


import unittest
from SCANDATA.model.data_factory import CellImageFactory, FullFramesFactory
from SCANDATA.model.data_factory import ImageData
from SCANDATA.model.io_factory import TsmFileIO
import numpy as np

filename = '20408B002.tsm'
filepath = '..\\220408\\'



class TestImageData(unittest.TestCase):
    def test_val(self):
        image = ImageData( np.empty((1, 1), dtype=float))
        print(image.image_data)


class Testimage(unittest.TestCase):
    def test_cell_image(self):

        io_data = TsmFileIO(filename, filepath)
        data = io_data.full_frames
        interval = io_data.full_frame_interval
        pixel_size = 0.25
        
        data_factory = FullFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        frames_data, _, _, _ = fullframes.get_data()
        
        data_factory = CellImageFactory()
        
        cellimage = data_factory.create_data(frames_data, [0,3], pixel_size)
        cellimage.print_infor()
        cellimage.show_data()
        cellimage.print_name()


if __name__ == '__main__':
    unittest.main()