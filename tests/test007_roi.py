# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:37:38 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.user_controller import RoiFactory
from SCANDATA2.model.value_object import WholeFilename, RoiVal, FramesData
from SCANDATA2.model.model_main import DataService

import matplotlib.pyplot as plt

class TestRoi(unittest.TestCase):
    def test_Roi(self):
        data_service = DataService()
        data_service.create_model('..\\220408\\20408B002.tsm')
        factory = RoiFactory()

        


if __name__ == '__main__':
    unittest.main()