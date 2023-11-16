# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:37:38 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataService

class TestRoi(unittest.TestCase):
        data_service = DataService()      
        data_service.create_experiments('..\\220408\\20408B002.tsm')
        

        #get ROI
        roi1 = data_service.get_user_controller("ROI1")

        #roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        
        data_service.set_controller_val("ROI1", [18,0,2,1])
        roi1.data_dict["CH1"].show_data()

        #plt.figure()
        #data_service.set_controller("ROI1", [78,78,3,1])
        #roi1.data_dict["20408B002.tsm"]["CH1"].show_data()
        #data_service.print_infor()
        
        #print(data_service.get_infor("ROI1"))

        


if __name__ == '__main__':
    unittest.main()