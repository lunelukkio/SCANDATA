# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import DataKeySet, DataSwitchSet
class Test(unittest.TestCase):
    def test(self):
        data_key_set = DataKeySet()
        data_key_set.set_data_key("controller", "ROI1")
        data_key_set.set_data_key("controller", "ROI2")


        dict1 = DataSwitchSet()
        
        data_key_set.add_observer(dict1)
        data_key_set.set_data_key("controller", "ROI3")
        print(dict1.switch_set)
        dict1.set_val("CONTROLLER","ROI2")
        print(dict1.switch_set)
        
        data_key_set.set_data_key("controller", "ROI4")
        print(dict1.switch_set)
        print(dict1.switch_set)
        
        



if __name__ == '__main__':
    unittest.main()
    
    
