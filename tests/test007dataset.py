# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:06:03 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataSet
import matplotlib.pyplot as plt

class TestDataSet(unittest.TestCase):
    def test_data_set(self):
        filename = '20408B002.tsm'
        filepath = '..\\220408\\'
        dataset = DataSet(filename, filepath)
        
        tracefig = plt.figure()
        dataset.data['ChTrace1'].show_data()
        dataset.controller['Roi1'].set_data(5,5,1,1)
        dataset.data['ChTrace1'].show_data()
        dataset.data['FullTrace1'].show_data()
        
        dataset.build_trace(dataset.data['FullFrames1'], dataset.data['ChFrames1'], dataset.data['ChFrames2'])
        dataset.print_infor()
        dataset.controller['Roi2'].set_data(50,50,10,10)
        dataset.data['ChTrace3'].show_data()
        dataset.data['ChTrace4'].show_data()
        
        imagefig = plt.figure()
        dataset.build_image(dataset.data['FullFrames1'], dataset.data['ChFrames1'], dataset.data['ChFrames2'])
        dataset.print_infor()
        dataset.data['CellImage3'].show_data()
        
if __name__ == '__main__':
    unittest.main()