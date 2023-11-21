# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import WholeFilename
from SCANDATA.model.model_main import Experiments
import matplotlib.pyplot as plt


filename_obj = WholeFilename('..\\70127A\\70127A101.da')  # this is a value object

class Test(unittest.TestCase):
    def test(self):

        experiments = Experiments(filename_obj)
        plt.figure()
        experiments.frames_dict["FULL"].show_data()
        plt.figure()
        experiments.trace_dict["ELEC1"].show_data()
        experiments.print_infor()
        experiments.get_default()


if __name__ == '__main__':
    unittest.main()