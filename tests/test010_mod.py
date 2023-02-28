# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:03:01 2023

@author: lulul
"""

import unittest
from SCANDATA.model.model_main import DataSet

class TestMod(unittest.TestCase):
    def test_data_set(self):
        filename = ('..\\220408\\20408B002.tsm')
        dataset = DataSet(filename)
        dataset.create_data('Trace')
        dataset.add_mod('Trace', 'Normalize')

        trace = dataset.get_data('ChTrace1')
        trace.show_data()


        
if __name__ == '__main__':
    unittest.main()