# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:55:52 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.controller.controller_main import ViewController
from SCANDATA.common_class import WholeFilename

filename_obj = WholeFilename('..\\220408\\20408B002.tsm')

class TestController(unittest.TestCase):
    def test_controller(self):
        
        controller = ViewController()
        controller.create_model(filename_obj)
        controller.create_controller("ROI")
        controller.bind_filename2controller("20408B002.tsm", "Roi1")
        controller.model.help()
        roi1 = controller.get_data("ROI1")
        
        roi1.show_data("20408B002.tsm", "Ch1")
        controller.set_controller("ROI1", [7,0,40,40])
        roi1.show_data("20408B002.tsm", "Ch1")

        
if __name__ == '__main__':
    unittest.main()