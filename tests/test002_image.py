# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 11:25:49 2022

@author: lulul
"""


import unittest
from SCANDATA.model.data_factory import FluoImageFactory
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
        data_channel = 2  # 0:fullFrames 1,2: chFrames
        repository = DataRepository(filename)
        rawdata = repository.original_data_3d[data_channel] # 0:fullFrames 1,2: chFrames
        # make frames value object
        data = FramesData(rawdata)

        # full frame image
        data_factory = FluoImageFactory()
        
        cellimage = data_factory.create_data(data)
        cellimage.update([3,5])
        cellimage.show_data()
        cellimage.print_infor()


if __name__ == '__main__':
    unittest.main()