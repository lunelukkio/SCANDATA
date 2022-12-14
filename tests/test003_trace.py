# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:33:19 2022

@author: lulul
"""


import unittest
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.value_object import Filename, TraceData, FramesData
from SCANDATA.model.io_factory import TsmFileIOFactory
import numpy as np


filename = Filename('..\\220408\\20408B002.tsm')

"""
class TestTraceData(unittest.TestCase):
    def test_val(self):
        trace = TraceData(np.empty((100), dtype=float))
        print(trace.trace_data)
        
class TestTimeData(unittest.TestCase):
    def test_val(self):
        time = TimeData( np.empty((100), dtype=float))
        print(time.time_data)
"""

class TestTrace(unittest.TestCase):
    def test_gull_trace(self):
        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename)
        _, data = io_data.get_data()
        rawdata = data[:,:,:,0]
        _, interval = io_data.get_infor()
        pixel_size = 0.25

        data = FramesData(rawdata)
        
        #trace
        data_factory = ChFramesFactory()
        chframes = data_factory.create_data(data, interval, pixel_size)
        frames_data = chframes.get_data()
        
        data_factory = ChTraceFactory()
        
        chtrace = data_factory.create_data(frames_data, interval)
        chtrace._read_data([40,39,39,40])

        chtrace.show_data()




if __name__ == '__main__':
    unittest.main()