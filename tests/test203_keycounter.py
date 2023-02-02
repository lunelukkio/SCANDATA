# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 22:31:27 2022

@author: lulul
"""
import unittest
from SCANDATA.model.model_main import Experiments
import matplotlib.pyplot as plt
from SCANDATA.view.view_main import KeyCounter


filename = '..\\220408\\20408B002.tsm'

class TestKeyCounter(unittest.TestCase):
    def test_key_count(self):
        exp = Experiments()
        exp.help()
        #make dataset
        exp.create_data_set(filename)

        print(KeyCounter.count_key(exp.data_set['20408B002.tsm'].data ,'ChFrames'))



if __name__ == '__main__':
    unittest.main()