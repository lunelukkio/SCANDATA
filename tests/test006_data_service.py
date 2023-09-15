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
        
        expdata = data_service.repository["ExperimentsRepository"].find_by_name('20408B002.tsm')
        data_dict = expdata.get_trace_list()
        print(data_dict)
        expdata.trace_dict["Elec_ch2"].show_data()
        
        data_service.find_by_key('20408B002.tsm')

if __name__ == '__main__':
    unittest.main()
