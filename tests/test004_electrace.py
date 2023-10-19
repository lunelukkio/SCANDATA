# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:45:19 2022

lunelukkio@gmail.com
"""
import unittest
from SCANDATA.common_class import WholeFilename
from SCANDATA.model.value_object import TraceData
from SCANDATA.model.file_io import TsmFileIo


filename_obj = WholeFilename('..\\220408\\20408B002.tsm')  # this is a value object

class Test(unittest.TestCase):
    def test(self):

        file_io = TsmFileIo(filename_obj)

        rawdata = file_io.get_1d()
        

        data_channel = 0  # 0:fullFrames 1,2: chFrames
        interval = 1
        
        data = rawdata[data_channel]
        
        test = TraceData(data, interval)
        
        test.show_data()


if __name__ == '__main__':
    unittest.main()