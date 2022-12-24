# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.data_factory import FrameData, FullFrame, ChFrame
from SCANDATA.model.io_factory import TsmFileIO

filename = '20408B002.tsm'
filepath = '..\\220408\\'

frame = FrameData()
io_data = TsmFileIO(filename, filepath)
fullframe = ChFrame(io_data)

class TestFrameData(unittest.TestCase):
    def test_check_val(self):
        frame.check_val()

class TestFullFrame(unittest.TestCase):
    def test_full_frame(self):
        fullframe.print_infor()
        fullframe.show_data(1)
        fullframe.print_name()


if __name__ == '__main__':
    unittest.main()