# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:53 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.model_main import DataService
import matplotlib.pyplot as plt

class TestRoi(unittest.TestCase):
        data_service = DataService()      
        data_service.create_model('..\\220408\\20408B002.tsm')
        
        #make controller
        data_service.create_user_controller("ImageController")

        #get IC
        ic1 = data_service.get_user_controller("ImageController1")
        
        #add filename to IC1
        data_service.resister_filename2controller("20408B002.tsm", "imagecontroller1")

        
        #ic1.data_dict["20408B002.tsm"]["FULL"].show_data()
        exp = data_service.get_experiments("20408B002.tsm")
        exp.frames_dict["CH1"].show_data()
        plt.figure()
        data_service.set_controller("imagecontroller1", [99,1])
        ic1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #roi1.data_dict["20408B002.tsm"]["FULL"].show_data()

        


if __name__ == '__main__':
    unittest.main()