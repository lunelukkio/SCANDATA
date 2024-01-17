# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.controller.controller_axis import ViewData

class Test(unittest.TestCase):
    def test(self):

        view_data = ViewData()
        view_data.set_view_data("CONTROLLER", "ROI1")
        print(view_data.view_dict)
        view_data.set_view_data_val("ROI1", False)  
        print(view_data.view_dict["CONTROLLER"])
        view_data.set_view_data_val("ROI1")  
        print(view_data.view_dict["CONTROLLER"])
        view_data.set_view_data("CONTROLLER", "ROI1")
        print(view_data.view_dict)


if __name__ == '__main__':
    unittest.main()