# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import DataKeySet, KeyDict

class Test(unittest.TestCase):
    def test(self):
        data_key_set = DataKeySet()
        data_key_set.set_data_key("controller", "ROI1")
        print(data_key_set.key_dict["CONTROLLER"].key_list)
        data_key_set.set_data_key("controller", "ROI2")
        print(data_key_set.key_dict["CONTROLLER"].key_list)
        data_key_set.set_data_key("controller", "ROI1")
        print(data_key_set.key_dict["CONTROLLER"].key_list)
        
        dict1 = KeyDict()
        dict1.set_data_key("ROI1")
        print(dict1.key_dict)
        dict1.set_data_key("ROI2")
        print(dict1.key_dict)
        dict1.set_data_key("ROI1")
        print(dict1.key_dict)


if __name__ == '__main__':
    unittest.main()
    
    
