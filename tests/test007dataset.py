# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:06:03 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataSet


class TestDataSet(unittest.TestCase):
    def test_data_set(self):
        filename = '20408B002.tsm'
        filepath = '..\\220408\\'
        dataset = DataSet(filename, filepath)
        
        print(dataset.data['ChTrace1'].print_infor())
        #print(dataset.model_controller['Roi1'].get_data())

        print('TraceDataにTimeDataを移植。初期値を消す。これで5以下はなくなる')

if __name__ == '__main__':
    unittest.main()