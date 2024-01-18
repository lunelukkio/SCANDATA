# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import DataKeySet, ViewDataDict

class Test(unittest.TestCase):
    def test(self):
        key_set = DataKeySet()
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set.key_dict)
        key_set.set_data_key("CONTROLLER", "ROI2")
        print(key_set.key_dict)
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set.key_dict)
        


if __name__ == '__main__':
    unittest.main()
    
    
