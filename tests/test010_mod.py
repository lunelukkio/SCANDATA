# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:03:01 2023

@author: lulul
"""

import unittest
from SCANDATA.model.model_main import DataSet
from SCANDATA.model.value_object import ImageData, TraceData
import numpy as np

class TestMod(unittest.TestCase):
    def test_data_set(self):
        filename = ('..\\220408\\20408B002.tsm')
        dataset = DataSet(filename)
        dataset.create_data('Trace')
        dataset.create_data('Trace')
        dataset.update_data('Roi1')
        dataset.update_data('Roi2')
        
        dataset.add_mod('Trace', 'BgComp')
        
        trace = dataset.get_data('ChTrace3')
        trace.show_data()


        
if __name__ == '__main__':
    unittest.main()