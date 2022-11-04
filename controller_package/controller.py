# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022

lunelukkio@gmail.com
main for controller
"""

from model_package.model import Model
from view_package.view import View
import os
import numpy as np
import matplotlib.pyplot as plt


class Controller:
    def __init__(self):
        print('Imported controller')
        
        self.view = None
        self.model = None
        
        self.filename = 'no file'
        self.filepath = 'no file'
        
    def menu_open_click(self, fullname):
        self.filename = os.path.basename(fullname)
        filepath = os.path.dirname(fullname)
        self.filepath = os.path.join(filepath) +os.sep
        
        self.model = self.create_model()

    def create_model(self):  
        self.model = Model(self.filename, self.filepath)     #test code

        print(self.filename)
        self.model.data_container.fileinfor.print_fileinfor()
        
    def fluo_trace(self):
        displayed_trace = self.model.request_data('ch_fluo_trace')

        plt.plot(displayed_trace)
        return displayed_trace
        
    def roi_controller(self):
        print('ROI controller')