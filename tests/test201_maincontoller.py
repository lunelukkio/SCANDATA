# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:55:52 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.view.view_main import View
from SCANDATA.controller.controller_main import Controller

fullname = '..\\220408\\20408B002.tsm'

class TestController(unittest.TestCase):
    def test_controller(self):
        
        controller = Controller()
        filename_obj = controller.create_filename_obj(fullname)
        filename_obj.print_infor()
        
        
if __name__ == '__main__':
    unittest.main()