# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:33:19 2022

@author: lulul
"""

import unittest
from SCANDATA.model.data_factory import FluoTraceFactory
from SCANDATA.model.value_object import Filename, FramesData
from SCANDATA.model.repository import DataRepository

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
        #read data
        data_channel = 1  # 0:fullFrames 1,2: chFrames
        repository = DataRepository(filename)
        rawdata = repository.original_data_3d[data_channel] # 0:fullFrames 1,2: chFrames
        interval = repository.original_data_infor[data_channel] # 0:fullFrames interval 1,2: chFrames interval
        # make frames value object
        data = FramesData(rawdata)
        
        #trace
        data_factory = FluoTraceFactory()
        trace = data_factory.create_data(data, interval)
        trace._read_data([40,40,30,5])

        trace.show_data()


if __name__ == '__main__':
    unittest.main()