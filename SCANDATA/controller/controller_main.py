# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022

lunelukkio@gmail.com
main for controller
"""

from SCANDATA.model.model_main import DataService
from SCANDATA.common_class import WholeFilename
import tkinter as tk
import os
import psutil  # for memory check


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

    def __del__(self):
        print('Deleted a ViewController.' + '  myId= {}'.format(id(self)))

    def open_file(self, filename_obj=None) -> str:
        if filename_obj is None:
            filename_obj = self.__file_service.open_file()
        self.create_model(filename_obj) 
        default_controller_list, default_data_list = self.__model.get_experiments(filename_obj.name).get_default()
        
        controller_list = []
        data_list = default_data_list
        for controller_key in default_controller_list:
            new_key = self.set_user_controller(controller_key)
            controller_list.append(new_key)
            self.__model.bind_filename2controller(filename_obj.name, new_key)
        return filename_obj.name, controller_list, data_list    
    
    def create_model(self, filename_obj: object):  
        self.__model.create_model(filename_obj.fullname)
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== ViewController: Suceeded to read data from data files.')
            print('')
            
    def set_user_controller(self, controller_key):
        new_key = self.__model.set_user_controller(controller_key)
        return new_key

    def bind_filename2controller(self, filename_key, controller_key):
        self.__model.bind_filename2controller(filename_key, controller_key)
        
    def set_controller_val(self, controller_key: str, val: list):
        self.__model.set_controller_val(controller_key, val)
        
    def get_data(self, controller_key):
        data_dict = self.__model.get_controller_data(controller_key)
        if data_dict is None:
            print(f"Can't find data_dict in {controller_key}")
        else:
            return data_dict

    # overlap with set_controller_val???
    def set_position(self, controller_key, val):
        self.__model.set_controller_val(controller_key, val)
    
    def change_roi_size(self, roi_num, val): #val = [x,y,x_length,y_length]
        self.current_roi_num = roi_num
        key = 'Roi' + str(roi_num)
        self.__model.add_data(key, val)
        
    def set_frame_window_position(self, event):
        pass
        
    # no use?
    def send_update_message(self, key, val):
        self.__model.set_data(key, val)
        
    def bind_keys(self, controller_key, data_key):
        self.__model.bind_data(controller_key, data_key)
        self.__model.update_data(controller_key)
        
    def set_experiments(self, controller_key:str, filename_key:str):
        self.__model.set_experiments(controller_key, filename_key)

    def set_data(self, controller_key:str, data_key: str):
        self.__model.set_data(controller_key, data_key)
    
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
        
    def print_model_infor(self):
        self.__model.print_infor()
    
        

class FileService:
    def open_file(self, *filename):  # it can catch variable num of filenames.
        if filename == ():
            fullname = self.get_fullname()  # This is str filename
            if fullname == None:
                print("There is no such a filename.")
                return
            new_full_filename = fullname
        else:
            new_full_filename = filename
        return WholeFilename(new_full_filename)
    
    
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
    



        
