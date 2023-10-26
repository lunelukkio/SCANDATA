# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:53 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataService
import matplotlib.pyplot as plt

class TestRoi(unittest.TestCase):
        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')


        #get IC
        ic1 = data_service.get_user_controller("Image_Controller1")


        #ic1.data_dict["20408B002.tsm"]["FULL"].show_data()
        exp = data_service.get_experiments("20408B002.tsm")
        exp.frames_dict["CH1"].show_data()
        plt.figure()
        data_service.set_controller_val("image_controller1", [99,1])
        ic1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #roi1.data_dict["20408B002.tsm"]["FULL"].show_data()

        


if __name__ == '__main__':
    unittest.main()