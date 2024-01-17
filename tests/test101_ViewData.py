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
        view_data = ViewDataDict()
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set._key_dict)
        
        
        
        
        """
        view_data.set_view_data("CONTROLLER", "ROI1")
        print(view_data.view_dict)
        view_data.set_view_data_val("ROI1", False)  
        print(view_data.view_dict["CONTROLLER"])
        view_data.set_view_data_val("ROI1")  
        print(view_data.view_dict["CONTROLLER"])
        view_data.set_view_data("CONTROLLER", "ROI1")
        print(view_data.view_dict)
        """

if __name__ == '__main__':
    unittest.main()