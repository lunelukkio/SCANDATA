# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 08:38:14 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.model_main import DataService
import matplotlib.pyplot as plt

class Test(unittest.TestCase):
    def test(self):

        data_service = DataService()      
        data_service.create_model('..\\220408\\20408B002.tsm')
        data_service.create_model('..\\220408\\20408B001.tsm')
        
        #make controller
        data_service.create_user_controller("Roi")
        data_service.create_user_controller("Roi")
        data_service.create_user_controller("Roi")
        
        #get ROI
        roi1 = data_service.get_user_controller("ROI1")
        roi2 = data_service.get_user_controller("ROI2")
        roi3 = data_service.get_user_controller("ROI3")
        
        #delete ROI
        data_service.create_user_controller("Roi2")
        data_service.print_infor()
        

        #add filename to ROI1
        data_service.bind_filename2controller("20408B002.tsm", "Roi1")
        data_service.bind_filename2controller("20408B001.tsm", "Roi1")
        data_service.bind_filename2controller("20408B001.tsm", "Roi3")
        
        #roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #roi1.data_dict["20408B001.tsm"]["FULL"].show_data()
        #roi3.data_dict["20408B001.tsm"]["CH2"].show_data()
        
        data_service.set_controller("ROI1", [20,20,20,20])
        roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #plt.figure()
        data_service.reset("ROI1")
        roi1.show_data("20408B002.tsm","CH1")
        data_service.print_infor()
        data_service.create_user_controller("Roi")
        data_service.print_infor()
        
        
        
        


if __name__ == '__main__':
    unittest.main()
