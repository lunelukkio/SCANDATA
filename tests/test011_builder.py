# -*- coding: utf-8 -*-
"""
Created on Sat May  6 00:05:42 2023

@author: lulul
"""

import unittest
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory, FullFrames, ChFrames
from SCANDATA.model.value_object import Filename
from SCANDATA.model.builder import Builder
import numpy as np

filename = Filename('..\\220408\\20408B002.tsm')  # this isa a value object

class TestBuilder(unittest.TestCase):
    def test_builder(self):
        builder = Builder()
        builder.read_file()


if __name__ == '__main__':
    unittest.main()