# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:05:53 2022

lunelukkio@gmail.com
"""

import unittest
from SCANDATA.model.model_main import Filename
from SCANDATA.model.model_main import Experiments
import matplotlib.pyplot as plt

filename1 = Filename('..\\220408\\20408B002.tsm')
filename2 = Filename('..\\220408\\20408A001new.tsm')

class TestExperiments(unittest.TestCase):
    def test_experiments(self):
        exp1 = Experiments()
        exp1.help()
        #make dataset
        exp1.create_data_set(filename1)
        exp1.create_data_set(filename2)
        
        # show traces
        a = plt.figure()
        exp1.data_set['20408B002.tsm'].data['ChTrace1'].show_data()
        b = plt.figure()
        exp1.data_set['20408A001new.tsm'].data['ChTrace1'].show_data()
        
        #add new trace
        exp1.create_data(filename1, 'CellImage')
        c = plt.figure()
        exp1.data_set['20408B002.tsm'].data['CellImage3'].show_data()

        # test create data and bind data and reset data
        exp1.create_data(filename1, 'FluoTrace')
        d = plt.figure()
        exp1.set_data('20408B002.tsm', 'Roi1', (5,5,50,50))
        trace3 = exp1.get_data('20408B002.tsm', 'ChTrace1')
        trace3.plot()
        
        exp1.bind_data('Roi1', 'ChTrace1', '20408A001new.tsm', '20408B002.tsm')
        exp1.reset_data('20408A001new.tsm', 'Roi1')
        trace3 = exp1.get_data('20408B002.tsm', 'ChTrace1')
        trace3.plot()
        

if __name__ == '__main__':
    unittest.main()
    