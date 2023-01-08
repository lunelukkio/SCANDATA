# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:03:01 2023

@author: lulul
"""

import unittest
from SCANDATA.model.model_main import DataSet
from SCANDATA.model.value_object import Filename
from SCANDATA.model.mod_factory import BgComp
import matplotlib.pyplot as plt


filename = Filename('..\\220408\\20408B002.tsm')
dataset = DataSet(filename)


class TestMod(unittest.TestCase):
    def test_mod(self):

        trace = dataset.get_data('ChTrace1')
        bgtrace = dataset.get_data('BgChTrace1')
        bg = BgComp(bgtrace)
        bg.mod_data(trace)

        
        



        
if __name__ == '__main__':
    unittest.main()