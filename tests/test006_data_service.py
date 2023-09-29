# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 08:38:14 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA2.model.model_main import DataService

class Test(unittest.TestCase):
    def test(self):

        data_service = DataService()      
        data_service.create_model('..\\220408\\20408B002.tsm')
        data_service.create_model('..\\220408\\20408B001.tsm')
        
        expdata = data_service.get_experiments('20408B002.tsm')
        expdata.trace_dict["Elec_ch1"].show_data()
        expdata = data_service.get_experiments('20408B001.tsm')
        expdata.trace_dict["Elec_ch2"].show_data()
        
        #make controller
        data_service.create_user_controller("Roi")
        data_service.print_infor()
        data_service.create_user_controller("Roi")
        data_service.print_infor()
        data_service.create_user_controller("Roi")
        data_service.print_infor()
        
        #get ROI
        roi = data_service.get_user_controller("ROI1")
        roi.print_infor()
        
        #delete ROI
        data_service.delete_user_controller("Roi2")
        data_service.delete_user_controller("Roi3")
        
        #make ROI again
        data_service.create_user_controller("Roi")
        data_service.print_infor()
        
        #add filename to ROI1
        data_service.resister_filename2controller("Roi1", "20408B002.tsm")
        roi.print_infor()
        



if __name__ == '__main__':
    unittest.main()
