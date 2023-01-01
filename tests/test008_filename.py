# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 13:24:28 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.value_object import Filename

filename = Filename('..\\220408\\20408B002.tsm')


class TestFilename(unittest.TestCase):
    def test_val(self):
        print('Fullname = ' + str(filename.fullname))
        print('Filename = ' + str(filename.name))
        print('Filepath = ' + str(filename.path))
        print('Absolute path = ' + str(filename.abspath))
        print('Extension = ' + str(filename.extension))



if __name__ == '__main__':
    unittest.main()
    