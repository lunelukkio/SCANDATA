# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 08:38:14 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataService
import matplotlib.pyplot as plt

class Test(unittest.TestCase):
    def test(self):

        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')
        data_service.create_experiments('..\\220408\\20408B001.tsm')

        #delete ROI
        data_service.create_user_controller("Roi2")
        data_service.print_infor()
        
        #roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #roi1.data_dict["20408B001.tsm"]["FULL"].show_data()
        #roi3.data_dict["20408B001.tsm"]["CH2"].show_data()
        roi1 = data_service.get_user_controller("ROI1")
        data_service.set_controller_val("ROI1", [20,20,1,1])
        roi1.print_infor()
        roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        
        data_service.print_infor()
        print(data_service.get_infor("ROI1"))
        print(data_service.get_infor())
        
        
        
        


if __name__ == '__main__':
    unittest.main()
