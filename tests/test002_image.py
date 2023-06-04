# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 11:25:49 2022

@author: lulul
"""


import unittest
from SCANDATA.model.data_factory import CellImageFactory, FullFramesFactory
from SCANDATA.model.value_object import Filename, FramesData
from SCANDATA.model.repository import DataRepository

filename = Filename('..\\220408\\20408B002.tsm')  # this is a value object

"""
class TestImageData(unittest.TestCase):
    def test_val(self):
        image = ImageData( np.empty((1, 1), dtype=float))
        print(image.data)
"""

class Testimage(unittest.TestCase):
    def test_cell_image(self):
        #read data
        repository = DataRepository(filename)
        rawdata = repository.original_data_3d[0]
        interval = repository.original_data_infor[0]
        # make frames value object
        data = FramesData(rawdata)
        pixel_size = 0.25
        # make frames entity
        data_factory = FullFramesFactory()
        fullframes_entity = data_factory.create_data(data, interval, pixel_size)
        fullframes_entity.show_data(8)
        fullframes_value_obj = fullframes_entity.frames_obj

        # full frame image
        data_factory = CellImageFactory()
        
        cellimage = data_factory.create_data(fullframes_value_obj)
        cellimage.update([2,90])
        cellimage.show_data()
        cellimage.print_infor()


if __name__ == '__main__':
    unittest.main()