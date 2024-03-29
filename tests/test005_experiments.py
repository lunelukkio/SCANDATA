# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:48:55 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import WholeFilename
from SCANDATA.model.model_main import Experiments
import matplotlib.pyplot as plt


filename_obj = WholeFilename('..\\220408\\20408B002.tsm')  # this is a value object

class Test(unittest.TestCase):
    def test(self):

        experiments = Experiments(filename_obj)
        plt.figure()
        experiments.frames_dict["CH0"].show_data()
        plt.figure()
        experiments.trace_dict["ELEC1"].show_data()
        experiments.print_infor()


if __name__ == '__main__':
    unittest.main()


