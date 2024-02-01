# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:01:25 2024

@author: lunel
"""

import unittest
from SCANDATA.model.model_main import DataRepository



class Test(unittest.TestCase):
    def test(self):
        #data = {"ROI0":1}
        data = {"ROI0": {"CH0": 0, "CH1": 1, "CH2":2}, "TRACE_CONTROLLER":{"ELEC0": 3, "ELEC1": 4}}

        repository = DataRepository()
        #repository.save("00101A001", 1)
        repository.save("00101A001", data)
        print(repository.data)
        print(repository.get_infor())

if __name__ == '__main__':
    unittest.main()
