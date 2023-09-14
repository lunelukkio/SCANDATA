# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 17:48:55 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.value_object import WholeFilename, TraceData
from SCANDATA2.model.model_main import Experiments
from SCANDATA2.model.file_io import TsmFileIo


filename_obj = WholeFilename('..\\220408\\20408B002.tsm')  # this is a value object

class Test(unittest.TestCase):
    def test(self):

        file_io = TsmFileIo(filename_obj)

        experiments = Experiments(filename_obj)
        experiments.trace["Full"].show_data()
        print("dane")


if __name__ == '__main__':
    unittest.main()