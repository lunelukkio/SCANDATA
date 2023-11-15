# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 13:22:05 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataService

class ModTest(unittest.TestCase):
    def test_mod(self):
        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')

        #get IC
        ic1 = data_service.get_user_controller("TRACE_Controller1")
        
        
        #ic1.data_dict["20408B002.tsm"]["FULL"].show_data()
        data_service.set_controller_val("TRACE_Controller1", [1,10])
        ic1.data_dict["20408B002.tsm"]["ELEC1"].show_data()
        
        
        
        
if __name__ == '__main__':
    unittest.main()