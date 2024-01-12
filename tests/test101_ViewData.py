# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import WholeFilename
from SCANDATA.controller.controller_axis import ViewData
import


filename_obj = WholeFilename('..\\220408\\20408B002.tsm')  # this is a value object

class Test(unittest.TestCase):
    def test(self):

        view_data_list = ViewData(filename_obj)
        


if __name__ == '__main__':
    unittest.main()




if __name__ == '__main__':
    unittest.main()