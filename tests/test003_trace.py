# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:33:19 2022

@author: lulul
"""     
import unittest
from SCANDATA2.model.value_object import WholeFilename, TraceData
from SCANDATA2.model.file_io import TsmFileIoFactory


filename = WholeFilename('..\\220408\\20408B002.tsm')  # this isa a value object

class Test(unittest.TestCase):
    def test(self):

        io_factory = TsmFileIoFactory()
        file_io = io_factory.create_file_io(filename)

        rawdata = file_io.get_3d()
        
        data_channel = 0  # 0:fullFrames 1,2: chFrames
        
        x = 40
        y = 40
        interval = 1
        
        data = rawdata[data_channel][x,y,:]
        
        test = TraceData(data, interval)
        
        test.show_data()


if __name__ == '__main__':
    unittest.main()