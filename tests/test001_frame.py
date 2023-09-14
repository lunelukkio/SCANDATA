# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.value_object import WholeFilename, FramesData
from SCANDATA2.model.file_io import TsmFileIo


filename_obj = WholeFilename('..\\220408\\20408B002.tsm')  # this isa a value object

class TestFrames(unittest.TestCase):
    def test_frame(self):

        file_io = TsmFileIo(filename_obj)

        rawdata = file_io.get_3d()
        
        data_channel = 0  # 0:fullFrames 1,2: chFrames
        frame_num = 0
        
        print(rawdata[data_channel])
        
        test = FramesData(rawdata[data_channel])
        test.show_data(frame_num)


if __name__ == '__main__':
    unittest.main()