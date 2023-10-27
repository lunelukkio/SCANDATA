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


class ViewController:
    def __init__(self, view=None):
        self.__model = DataService()
        self.__view = view
        self.__file_service = FileService()
        self.operating_controller_list = []
        
    def __del__(self):
        print('Deleted a ViewController.' + '  myId= {}'.format(id(self)))

    def open_file(self, filename_obj=None) -> dict:
        # get filename object
        if filename_obj is None:
            filename_obj = self.__file_service.open_file()
        # make experiments data
        self.create_experiments(filename_obj) 
        return filename_obj   
    
    def create_experiments(self, filename_obj: object):  
        controller_dict_keys = self.__model.create_experiments(filename_obj.fullname)
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== ViewController: Suceeded to read data from data files.')
            print('')
            return controller_dict_keys
            
    def set_user_controller(self, controller_key):
        new_key = self.__model.set_user_controller(controller_key)
        return new_key
        
    def set_experiments(self, controller_key:str, filename_key:str):
        self.__model.set_experiments(controller_key, filename_key)

    def set_data(self, controller_key:str, data_key: str):
        for filename_key in self.filename_key_list:
            self.__model.set_data(controller_key, self.filename_key, data_key)

    def bind_filename2controller(self, filename_key, controller_key):
        self.__model.bind_filename2controller(filename_key, controller_key)
        
    def set_controller_val(self, controller_key: str, val: list):
        self.__model.set_controller_val(controller_key, val)
        
    def set_observer(self, controller_key, ax:object):
        self.__model.set_observer(controller_key, ax)

    def get_data(self, controller_key):
        data_dict = self.__model.get_controller_data(controller_key)
        if data_dict is None:
            print(f"Can't find data_dict in {controller_key}")
        else:
            return data_dict
        
    def get_controller_infor(self):
        return self.__model.get_infor()

    def set_position_image_ax(self, event):
        #print(event.button, event.x, event.y, event.xdata, event.ydata, event.dblclick, event.inaxes)
        for controller_key in self.operating_controller_list:
            print(f"{self.operating_controller_list}: ", end='')
            user_controller = self.__model.get_user_controller(controller_key)
            # Cursor adjustment. the center of the pixel is 0. So it need 0.5 shift. 
            roi_x = round(event.xdata)
            roi_y = round(event.ydata)
            roi = [roi_x, roi_y, None, None]
            user_controller.set_controller_val(roi)

    def change_roi_size(self, roi_num, val): #val = [x,y,x_length,y_length]
        self.current_roi_num = roi_num
        key = 'Roi' + str(roi_num)
        self.__model.add_data(key, val)
      
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
    
    def get_memory_infor(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        memory_infor = process.memory_info().rss
        maximum_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        return memory_infor, maximum_memory, available_memory

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
    



        
