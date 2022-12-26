# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:37:38 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.controller_factory import RoiFactory
from SCANDATA.model.controller_factory import RoiVal, Roi
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.io_factory import TsmFileIO
import numpy as np
import matplotlib.pyplot as plt

filename = '20408B002.tsm'
filepath = '..\\220408\\'

"""
class TestRoiVal(unittest.TestCase):
    def test_check_val(self):
        roival = RoiVal(2,5,1,1)
        print(roival.roi_val)
"""

class TestRoi(unittest.TestCase):
    def test_Roi(self):
        
        # make a 3D data
        io_data = TsmFileIO(filename, filepath)
        data = io_data.ch_frames[:,:,:,0]
        interval = io_data.ch_frame_interval
        pixel_size = 0.25
        
        #make a chframes
        data_factory = ChFramesFactory()
        chframes = data_factory.create_data(data, interval, pixel_size)
        frames_data, _, _, _ = chframes.get_data()
        
        data_factory = ChTraceFactory()
        trace = data_factory.create_data(frames_data, interval)
        
        controller_factory = RoiFactory()

        roi = controller_factory.create_model_controller()
        roi.add_observer(trace)
        roi.set_data(0,0,1,1)
        a = plt.figure()
        trace.show_data()
        
        roi.add_data(2,3,60,70)
        b = plt.figure()
        trace.show_data()
        
        roi.reset()
        c = plt.figure()
        trace.show_data()
        trace.print_name()
    


if __name__ == '__main__':
    unittest.main()