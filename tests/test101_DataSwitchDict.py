# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import DataSwitchDict
class Test(unittest.TestCase):
    def test(self):
        dict1 = DataSwitchDict()
        dict1.set_data_key("ROI1")
        dict1.set_data_key("ROI2")
        print(dict1)
        dict1.set_data_key("ROI1")
        print(dict1)
        dict1.set_val("ROI2", False)
        print(dict1)
        dict1.set_val("ROI2")
        print(dict1)

if __name__ == '__main__':
    unittest.main()
    
    
