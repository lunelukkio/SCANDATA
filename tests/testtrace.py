# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:33:19 2022

@author: lulul
"""


import unittest
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory, FullFramesFactory
from SCANDATA.model.data_factory import TraceData, TimeData
from SCANDATA.model.io_factory import TsmFileIO
import numpy as np

filename = '20408B002.tsm'
filepath = '..\\220408\\'


class TestTraceData(unittest.TestCase):
    def test_val(self):
        trace = TraceData()
        trace.trace_data =  np.empty((100), dtype=float)
        print(trace.trace_data)
        
class TestTimeData(unittest.TestCase):
    def test_val(self):
        time = TimeData()
        time.time_data =  np.empty((100), dtype=float)
        print(time.time_data)


class TestTrace(unittest.TestCase):
    def test_gull_trace(self):

        io_data = TsmFileIO(filename, filepath)
        data = io_data.full_frames
        interval = io_data.full_frame_interval
        pixel_size = 0.25
        
        data_factory = FullFramesFactory()
        fullframes = data_factory.create_data(data, interval, pixel_size)
        frames_data, _, _, _ = fullframes.get_data()
        
        data_factory = FullTraceFactory()
        
        fulltrace = data_factory.create_data(frames_data, interval)
        fulltrace._read_data([1,1,1,1])
        #fulltrace.print_infor()
        fulltrace.show_data()
        #fulltrace.print_name()


if __name__ == '__main__':
    unittest.main()