# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:53 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataService
import matplotlib.pyplot as plt

class TestImageController(unittest.TestCase):
        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')


        #get IC
        ic1 = data_service.get_user_controller("IMAGE_CONTROLLER1")
        data_service.set_controller_val("IMAGE_CONTROLLER1", [1,50])
        ic1.data_dict["CH1"].show_data()



        


if __name__ == '__main__':
    unittest.main()