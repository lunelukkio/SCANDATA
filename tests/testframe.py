# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:02:18 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.data_factory import FrameData, FullFrame

frame = FrameData()
fullframe = FullFrame()

class TestFrameData(unittest.TestCase):
    def test_check_val(self):
        frame.check_val()

class TestFullFrame(unittest.TestCase):
    def test_full_frame(self):
        fullframe.print()


if __name__ == '__main__':
    unittest.main()