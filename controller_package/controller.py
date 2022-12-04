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
        
        self.filename = []
        self.filepath = []
        
    def menu_open_click(self, fullname):
        filename = os.path.basename(fullname)
        pre_filepath = os.path.dirname(fullname)
        filepath = os.path.join(pre_filepath) + os.sep
        self.filename.append(filename)
        self.filepath.append(filepath)
        self.create_model(filename, filepath)

    def create_model(self, filename, filepath):  
        self.model.create_data_objects(filename, filepath)
        print('222222222222222222222222222222')
        
    def fluo_trace(self):
        displayed_trace = self.model.request_data('ch_fluo_trace')

        plt.plot(displayed_trace)
        return displayed_trace
        
    def roi_controller(self):
        print('ROI controller')