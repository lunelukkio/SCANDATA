# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:47:27 2023

@author: lulul
"""

import unittest
from SCANDATA.model.value_object import Filename
from SCANDATA.model.repository import DataRepository

filename = Filename('..\\220408\\20408B002.tsm')  # this isa a value object

class TestRepository(unittest.TestCase):
    def test_repository(self):
        repository = DataRepository(filename)
        repository.print_data(1,1)


if __name__ == '__main__':
    unittest.main()