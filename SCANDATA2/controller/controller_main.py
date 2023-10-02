# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022

lunelukkio@gmail.com
main for controller
"""

from SCANDATA2.model.model_main import DataService
from SCANDATA2.common_class import WholeFilename
import tkinter as tk
from tkinter import ttk
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
    

class ViewController:
    def __init__(self, view=None):
        self.model = DataService()
        self.view = view
        self.file_service = FileService()
        self.__filename_obj_list = []  # list of filename keys
        
        
        self.current_roi = None
        self.current_image_time_window = None
        self.current_trace_time_window = None
        
    def create_model(self, filename_obj: object):  
        self.model.create_model(filename_obj.fullname)
        if self.model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== Controller: Suceeded to read data from data files.')
            print('')
        return self.model
    
    def create_controller(self, controller_key:str):
        self.model.create_user_controller(controller_key)
        
    def bind_filename2controller(self, filename_key, controller_key):
        self.model.bind_filename2controller(filename_key, controller_key)
        
    def set_controller(self, controller_key: str, val: list):
        self.model.set_controller(controller_key, val)
        
    def get_data(self, controller_key):
        return self.model.get_user_controller(controller_key)









    def file_open(self):
        filename_obj = self.file_service.file_open()
        self.__filename_obj_list.append(filename_obj.name)
        self.view.reset()        
        self.create_model(filename_obj)
        
        default_controller = self.model.get_experiments(filename_obj.name).get_default()
        print(default_controller)
        for controller_key in default_controller.keys():
            print(controller_key)
            for num in range(default_controller[controller_key]):
                print(default_controller[controller_key])
                self.model.create_user_controller(controller_key)
        
        
        
        
        
        


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
        

class FileService:
    def file_open(self, *filename):  # it can catch variable num of filenames.
        if filename == ():
            fullname = self.get_fullname()  # This is str filename
            if fullname == None:
                print("There is no such a filename.")
                return
            return WholeFilename(fullname)
    
    
    @staticmethod
    def get_fullname(event=None):
        # open file dialog
        fullname = tk.filedialog.askopenfilename(
            initialdir = os.getcwd(), # current dir
            filetypes=(('Tsm files', '*.tsm'),
                       ('Da files', '*.da'), 
                       ('Axon files', '*.abf'),
                       ('WinCP files', '*.wcp'),
                       ('All files', '*.*'))
                      )
        return fullname
    



        
