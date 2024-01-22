# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 17:04:36 2023

@author: lunelukkio@gmail.com
"""

import unittest
from SCANDATA.common_class import SingletonKeyDict
class Test(unittest.TestCase):
    def test(self):
        dict_original = {"ROI1": ["CH0", "CH1"], "ROI2":["CH2", "CH3"]}
        dict1 = SingletonKeyDict()
        dict1.copy_dict(dict_original)
        print(dict1._dict)
        dict1.set_key("ROI1")
        print(dict1._dict)
        dict1.set_key("ROI3")
        print(dict1._dict)
        dict1.set_key("ROI2", "CH0")
        print(dict1._dict)
        dict1.set_key("ROI2", "CH0")
        print(dict1.get_key("ROI2"))



if __name__ == '__main__':
    unittest.main()

    
