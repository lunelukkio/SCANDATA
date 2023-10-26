# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:03:01 2023

@author: lulul
"""

import unittest
from SCANDATA.model.model_main import DataService

class Test_elec_controller(unittest.TestCase):
    def test_data_set(self):
        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')

        #get IC
        ic1 = data_service.get_user_controller("TRACE_Controller1")
        
        
        #ic1.data_dict["20408B002.tsm"]["FULL"].show_data()
        data_service.set_controller_val("TRACE_Controller1", [1,10])
        ic1.data_dict["20408B002.tsm"]["ELEC1"].show_data()

        
if __name__ == '__main__':
    unittest.main()