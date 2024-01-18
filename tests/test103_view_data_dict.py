# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:47:44 2024

@author: lunel
"""

import unittest
from SCANDATA.common_class import DataKeySet, ViewDataDict

class Test(unittest.TestCase):
    def test(self):
        key_set = DataKeySet()
        data = ViewDataDict()
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set.key_dict)
        key_set.set_data_key("CONTROLLER", "ROI2")
        print(key_set.key_dict)
        key_set.add_observer(data)
        
        
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set.key_dict)
        
        
        
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
