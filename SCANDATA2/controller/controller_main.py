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
import psutil  # for memory check
import re   # Regular expression


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
        self.__model = DataService()
        self.__view = view
        self.__file_service = FileService()
        
        self.__controller_list = []  # "ROI1" "ROI2" "IMGAE_CONTROLLER1" "ELEC_CONTROLLER1"
        self.__filename_list = []  # "20408B001.tsm" "20408B002.tsm"
        self.__data_list = []  # "Full" "CH1" "CH2"
        

        
        # filename []    roi []    data[]    20408B002.tsm ROI1 CH1
        # for filename in self.current_filename:
        #    for roi in current_controller:
        #        for data in current_data:
        #            send to view
                
        
    def __del__(self):
        print('Deleted a ViewController.' + '  myId= {}'.format(id(self)))

    def open_file(self):
        filename_obj = self.__file_service.open_file()
        self.__filename_list.append(filename_obj.name)       
        self.create_model(filename_obj)
        
        default_controller_key, default_data_key = self.__model.get_experiments(filename_obj.name).get_default()
        self.__data_list = default_data_key
        # make default controllers. "ROI1" "ROI2" "IMAGE_CONTROLLER1"
        if not self.__controller_list:
            for controller_key in default_controller_key:
                new_key = self.__model.create_user_controller(controller_key) # new_key is str
                self.__model.bind_filename2controller(filename_obj.name, new_key)
                self.__controller_list.append(new_key)
        # need refactoring
        # This is for the second opening file.
        else:
            i = 0
            for controller_key in default_controller_key:
                if controller_key == re.sub(r'\d+', '', self.__controller_list[i]):
                    self.__model.bind_filename2controller(filename_obj.name, self.__controller_list[i])
                    i += 1

        self.__view.draw_ax(3)  # 3 = draw whole ax
        

    def create_model(self, filename_obj: object):  
        self.__model.create_model(filename_obj.fullname)
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== Controller: Suceeded to read data from data files.')
            print('')
    
    def create_user_controller(self, controller_key:str):
        self.__model.create_user_controller(controller_key)
        
    def bind_filename2controller(self, filename_key, controller_key):
        self.__model.bind_filename2controller(filename_key, controller_key)
        
    def set_controller(self, controller_key: str, val: list):
        self.__model.set_controller(controller_key, val)
        
    def get_data(self, filename_key, controller_key, data_key):
        user_controller_obj = self.get_user_controller(controller_key)
        return user_controller_obj.data_dict[filename_key][data_key]
        
    def get_user_controller(self, controller_key):
        return self.__model.get_user_controller(controller_key.upper())
    
    def get_view_list(self):
        return self.__controller_list, self.__filename_list, self.__data_list


        





    def set_roi_position(self, event, roi_num=1):
        self.current_roi_num = roi_num
        key = 'Roi' + str(roi_num)
        print(key + ':')
        print(event.button, event.x, event.y, event.xdata, event.ydata)
        roi_val = self.__model.get_data(key)
        
        # Set roi center to click poist.
        roi_x = math.floor(event.xdata) - round(roi_val.data[2]/2) + 1
        roi_y = math.floor(event.ydata) - round(roi_val.data[3]/2) + 1
        roi = [roi_x, roi_y]
        self.send_update_message(key, roi)
    
    def change_roi_size(self, roi_num, val): #val = [x,y,x_length,y_length]
        self.current_roi_num = roi_num
        key = 'Roi' + str(roi_num)
        self.__model.add_data(key, val)
        
    def set_frame_window_position(self, event):
        pass
        
    def send_update_message(self, key, val):
        self.__model.set_data(key, val)
        
    def bind_keys(self, controller_key, data_key):
        self.__model.bind_data(controller_key, data_key)
        self.__model.update_data(controller_key)
    
    def add_mod(self, data_key: str, mod_key: str):
        self.__model.add_mod(data_key, mod_key)
        if self.current_roi_num is None:
            return
        key = 'Roi' + str(self.current_roi_num)
        self.send_update_message(key, [])
        
    def remove_mod(self, data_key: str, mod_key: str):
        self.__model.remove_mod(data_key, mod_key)
        if self.current_roi_num is None:
            return
        key = 'Roi' + str(self.current_roi_num)
        self.send_update_message(key, [])
    
    def count_data(self, filename, key):
        return self.__model.count_data(filename, key)
    
    def update_data(self, key):
        self.__model.update_data(key)
        

class FileService:
    def open_file(self, *filename):  # it can catch variable num of filenames.
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
    



        
