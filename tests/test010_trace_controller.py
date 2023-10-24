# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:03:01 2023

@author: lulul
"""

import unittest
from SCANDATA.model.model_main import DataService
import matplotlib.pyplot as plt

class Test_elec_controller(unittest.TestCase):
    def test_data_set(self):
        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')
        
        #make controller
        data_service.set_user_controller("TRACE_Controller")

        #get IC
        ic1 = data_service.get_user_controller("Image_Controller1")
        
        #add filename to IC1
        data_service.bind_filename2controller("20408B002.tsm", "image_controller1")

        
        #ic1.data_dict["20408B002.tsm"]["FULL"].show_data()
        exp = data_service.get_experiments("20408B002.tsm")
        exp.frames_dict["CH1"].show_data()
        plt.figure()
        data_service.set_controller("image_controller1", [99,1])
        ic1.data_dict["20408B002.tsm"]["CH1"].show_data()

        
if __name__ == '__main__':
    unittest.main()