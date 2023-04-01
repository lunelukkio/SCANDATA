# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 18:06:03 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import DataSet
from SCANDATA.model.value_object import Filename
import matplotlib.pyplot as plt
import numpy as np

class TestDataSet(unittest.TestCase):
    def test_data_set(self):
        filename = ('..\\220408\\20408B002.tsm')
        dataset = DataSet(filename)
        dataset.create_data('Trace')
        dataset.create_data('CellImage')
        dataset.update_data('Roi1')
        dataset.data['CellImage1'].update([0,0])  # update separately

        
        tracefig = plt.figure()
        dataset.data['ChTrace1'].show_data()
        dataset.controller['Roi1'].set_data(5,5)
        dataset.data['ChTrace1'].show_data()
        dataset.data['FullTrace1'].show_data()
        
        dataset.create_data('Trace')
        dataset.update_data('Roi2')
        
        dataset.print_infor()    
        dataset.set_data('Roi1', (5,5,5,5))
        dataset.data['ChTrace3'].show_data()
        dataset.data['ChTrace4'].show_data()
        
        imagefig = plt.figure()
        dataset.create_data('CellImage')
        dataset.data['CellImage3'].update(np.array([0,0]))
        dataset.print_infor()
        dataset.data['CellImage3'].show_data()
        
if __name__ == '__main__':
    unittest.main()