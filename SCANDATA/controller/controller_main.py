# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022

lunelukkio@gmail.com
main for controller
"""

from SCANDATA.model.model_main import DataSet
import os
import math
import glob
import psutil


class MainController:
    def __init__(self):
        self.controller_list = []
        
        
    def get_memory_infor(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        memory_infor = process.memory_info().rss
        maximum_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        return memory_infor, maximum_memory, available_memory

class ImagingController:
    def __init__(self, view, filename_obj):
        self.__filename = filename_obj
        self.view = view
        self.model = None
        self.current_roi_num = None
        self.view_data_repository = None
        
    def create_model(self, filename_obj: object):  
        self.model = DataSet(filename_obj.fullname)  # send filename str
        if self.model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== Suceeded to read data from data files. ============================== (from ImagingController)')
            print('')
        return self.model
    
    def create_filename_obj(self, filename: str):
        filename_obj = WholeFilename(filename)  # Convert from str to value object.
        self.__filename = filename_obj
        return filename_obj

    def set_roi_position(self, event, roi_num=1):
        self.current_roi_num = roi_num
        key = 'Roi' + str(roi_num)
        print(key + ':')
        print(event.button, event.x, event.y, event.xdata, event.ydata)
        roi_val = self.model.get_data(key)
        
        # Set roi center to click poist.
        roi_x = math.floor(event.xdata) - round(roi_val.data[2]/2) + 1
        roi_y = math.floor(event.ydata) - round(roi_val.data[3]/2) + 1
        roi = [roi_x, roi_y]
        self.send_update_message(key, roi)
    
    def change_roi_size(self, roi_num, val): #val = [x,y,x_length,y_length]
        self.current_roi_num = roi_num
        key = 'Roi' + str(roi_num)
        self.model.add_data(key, val)
        
    def set_frame_window_position(self, event):
        pass
        
    def send_update_message(self, key, val):
        self.model.set_data(key, val)
        
    def bind_keys(self, controller_key, data_key):
        self.model.bind_data(controller_key, data_key)
        self.model.update_data(controller_key)
    
    def add_mod(self, data_key: str, mod_key: str):
        self.model.add_mod(data_key, mod_key)
        if self.current_roi_num is None:
            return
        key = 'Roi' + str(self.current_roi_num)
        self.send_update_message(key, [])
        
    def remove_mod(self, data_key: str, mod_key: str):
        self.model.remove_mod(data_key, mod_key)
        if self.current_roi_num is None:
            return
        key = 'Roi' + str(self.current_roi_num)
        self.send_update_message(key, [])
    
    def count_data(self, filename, key):
        return self.model.count_data(filename, key)
    
    def update_data(self, key):
        self.model.update_data(key)
        
        
"Value object"





        
