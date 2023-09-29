# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:37:38 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.model_main import DataService
import matplotlib.pyplot as plt

class TestRoi(unittest.TestCase):
        data_service = DataService()      
        data_service.create_model('..\\220408\\20408B002.tsm')
        
        #make controller
        data_service.create_user_controller("Roi")

        #get ROI
        roi1 = data_service.get_user_controller("ROI1")
        
        #add filename to ROI1
        data_service.resister_filename2controller("20408B002.tsm", "Roi1")

        
        #roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        
        data_service.set_controller("ROI1", [78,1,1,1])
        roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #plt.figure()
        #data_service.set_controller("ROI1", [78,78,3,1])
        #roi1.data_dict["20408B002.tsm"]["CH1"].show_data()

        


if __name__ == '__main__':
    unittest.main()