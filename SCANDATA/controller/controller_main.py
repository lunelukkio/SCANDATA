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
import math


class Controller:
    def __init__(self):
        print('Imported controller')
        
        self.view = None
        self.model = None
        
        self.filename = []
        self.filepath = []
        

    def create_model(self, filename, filepath):  
        self.model.create_data_objects(filename, filepath)
        self.filename.append(filename)
        self.filepath.append(filepath)
        
    def roi_controller(self):
        print('ROI controller')
        
    def get_data(self, filename, data_type):
        return self.model.get_data(filename, data_type)
    
    def set_roi(self, event, roi_num=1, roi_length=[1, 1]):
        print(event.button, event.x, event.y, event.xdata, event.ydata)
        roi_x = math.floor(event.xdata)
        roi_y = math.floor(event.ydata)
        roi = [roi_x, roi_y] + roi_length
        self.model.set_data('ROI' + str(roi_num), roi)
        return roi
    
    def large_roi(self, roi_num):
        self.model.get_infor
        self.model.set_data('ROI' + str(roi_num), roi)
        
