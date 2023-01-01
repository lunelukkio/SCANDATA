# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:37:38 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.controller_factory import RoiFactory
from SCANDATA.model.value_object import RoiVal, ValueObjConverter
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.io_factory import TsmFileIOFactory
import matplotlib.pyplot as plt
from SCANDATA.model.model_main import Filename


filename = Filename('..\\220408\\20408B002.tsm')

"""
class TestRoiVal(unittest.TestCase):
    def test_check_val(self):
        roival = RoiVal(2,5,1,1)
        print(roival.data)
        roival2 = RoiVal(1,1,1,1)
        
        a = roival + roival2
        print(a.data)
"""

class TestRoi(unittest.TestCase):
    def test_Roi(self):
        converter = ValueObjConverter()
        # make a 3D data
        io_factory = TsmFileIOFactory()
        io_data = io_factory.create_file_io(filename)
        _, data = io_data.get_data()
        _, interval = io_data.get_infor()
        rawdata = data[:,:,:,0]
        pixel_size = 0.25
        data = converter.frames_converter(rawdata)
        
        #make a chframes
        data_factory = ChFramesFactory()
        chframes = data_factory.create_data(data, interval, pixel_size)
        frames_data = chframes.get_data()
        
        data_factory = ChTraceFactory()
        trace = data_factory.create_data(frames_data, interval)
        
        controller_factory = RoiFactory()

        roi = controller_factory.create_controller()
        roi.add_observer(trace)
        roi.set_data(0,0,1,1)
        a = plt.figure()
        trace.show_data()
        
        roi.add_data(2,5,60,70)
        b = plt.figure()
        trace.show_data()
        
        roi.reset()
        c = plt.figure()
        trace.show_data()
        #trace.print_infor()
      


if __name__ == '__main__':
    unittest.main()