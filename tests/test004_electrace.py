# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:45:19 2022

lunelukkio@gmail.com
"""


import unittest
from SCANDATA.model.data_factory import ElecTraceFactory
from SCANDATA.model.repository import DataRepository
from SCANDATA.model.value_object import Filename, TraceData

filename = Filename('..\\220408\\20408B002.tsm')

class TestTrace(unittest.TestCase):
    def test_gull_trace(self):
        # read data
        data_channel = 1  # 1-8 elec ch
        repository = DataRepository(filename)
        rawdata = repository.original_data_1d[data_channel-1]
        interval = repository.original_data_infor[data_channel+2]

        
        elec_data = TraceData(rawdata, interval)
        
        data_factory = ElecTraceFactory()
        
        trace = data_factory.create_data(elec_data, interval)
        trace.show_data()
        trace.print_infor()


if __name__ == '__main__':
    unittest.main()