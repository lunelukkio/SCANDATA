# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:55:16 2022

lunelukkio@gmail.com
"""


import unittest
from SCANDATA.controller.controller_main import WholeFilename

import numpy as np

filename = '..\\220408\\20408B002.tsm'  # this isa  value object

"""
class TestFramesData(unittest.TestCase):
    def test_val(self):
        frames = FramesData(np.empty((1, 1, 1), dtype=float))
        print(frames.frames_data)
"""

class TestWholeFileName(unittest.TestCase):
    def test_whole_filename(self):
        filename_obj = WholeFilename(filename)
        filename_obj.print_infor()


if __name__ == '__main__':
    unittest.main()