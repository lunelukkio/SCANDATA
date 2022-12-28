# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:45:19 2022

lunelukkio@gmail.com
"""


import unittest
from SCANDATA.model.data_factory import ChElecTraceFactory
from SCANDATA.model.io_factory import TsmFileIOFactory, TbnFileIOFactory
from SCANDATA.model.data_factory import ValueObjConverter


filename = '20408B002.tsm'
filepath = '..\\220408\\'



class TestTrace(unittest.TestCase):
    def test_gull_trace(self):
        converter = ValueObjConverter()
        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename, filepath)
        io_factory = TbnFileIOFactory()
        io_elec_data = io_factory.create_file_io(filename, filepath, io_data)

        interval = io_elec_data.get_infor()
        rawelec_data = io_elec_data.get_data()
        print(rawelec_data.shape[1])
        
        elec_data = converter.elec_trace_converter(rawelec_data[:,0], interval)
        
        data_factory = ChElecTraceFactory()
        
        trace = data_factory.create_data(elec_data, interval)

        trace.show_data()
        trace.print_infor()



if __name__ == '__main__':
    unittest.main()