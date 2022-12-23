# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:37:56 2022

lunelukkio@gmail.com
"""


import pytest
from data_factory import FrameData 

data = FrameData()

class TestFrame(object):
    def test_frame_data(self):
        assert FrameData.add(1,1) == 2