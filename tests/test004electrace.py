# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:45:19 2022

lunelukkio@gmail.com
"""


import unittest
from SCANDATA.model.data_factory import CameraSyncElecTraceFactory
from SCANDATA.model.io_factory import TsmFileIOFactory, TbnFileIOFactory


filename = '20408B002.tsm'
filepath = '..\\220408\\'



class TestTrace(unittest.TestCase):
    def test_gull_trace(self):

        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename, filepath)
        io_factory = TbnFileIOFactory()
        io_elec_data = io_factory.create_file_io(filename, filepath, io_data)

        interval = io_elec_data.get_infor()
        elec_data = io_elec_data.get_data()
        print(elec_data.shape[1])
        
        data_factory = CameraSyncElecTraceFactory()
        
        trace = data_factory.create_data(elec_data[:,0], interval)

        trace.show_data()
        trace.print_infor()



if __name__ == '__main__':
    unittest.main()