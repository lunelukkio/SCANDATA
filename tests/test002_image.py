# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 11:25:49 2022

@author: lulul
"""


import unittest
from SCANDATA.common_class import WholeFilename
from SCANDATA.model.value_object import ImageData
from SCANDATA.model.file_io import TsmFileIo


filename_obj = WholeFilename('..\\220408\\20408B002.tsm')  # this isa a value object

class Test(unittest.TestCase):
    def test(self):

        file_io = TsmFileIo(filename_obj)

        rawdata = file_io.get_3d()
        
        data_channel = 0  # 0:fullFrames 1,2: chFrames
        frame_num = 0
        
        data = rawdata[data_channel][:,:,frame_num]
        
        test = ImageData(data)
        
        test.show_data()


if __name__ == '__main__':
    unittest.main()