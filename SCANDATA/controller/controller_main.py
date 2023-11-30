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
        self.__operating_controller_list = []
        
    def __del__(self):
        print('Deleted a ViewController.' + '  myId= {}'.format(id(self)))

    def open_file(self, filename_obj=None) -> dict:
        # get filename object
        if filename_obj is None:
            filename_obj = self.__file_service.open_file()
        # make experiments data
        self.create_experiments(filename_obj) 
        self.print_model_infor()
        print(f"   !!! Open {filename_obj.name}: suceeded!!!")
        print("")
        return filename_obj   
    
    def create_experiments(self, filename_obj: object):  
        controller_dict_keys = self.__model.create_experiments(filename_obj.fullname)
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== ViewController: Suceeded to read data from data files.')
            print('')
            return controller_dict_keys
            
    def create_user_controller(self, controller_key):
        new_key = self.__model.create_user_controller(controller_key)
        return new_key
        
    def get_data(self, controller_key):
        data_dict = self.__model.get_controller_data(controller_key)
        if data_dict is None:
            print(f"Can't find data_dict in {controller_key}")
        else:
            return data_dict

    # put data to user controller data dict.
    def set_data(self, controller_key:str, data_key: str):
        for filename_key in self.filename_key_list:
            self.__model.set_data(controller_key, self.filename_key, data_key)
        
    def set_controller_val(self, controller_key: str, val: list):
        self.__model.set_controller_val(controller_key, val)
        
    def set_observer(self, controller_key, ax:object):
        self.__model.set_observer(controller_key, ax)
        
    def set_mod_key(self, controller_key, mod_key):
        self.__model.set_mod_key(controller_key, mod_key)
        
    def set_mod_val(self, controller_key, mod_key, val):
        self.__model.set_mod_val(controller_key, mod_key, val)

    def get_controller_infor(self, controller_key=None) -> dict:
        if controller_key is None:
            data_infor = self.__model.get_infor()
        else:
            data_infor = self.__model.get_infor(controller_key)
        return data_infor

    def set_position_image_ax(self, event):
        #print(event.button, event.x, event.y, event.xdata, event.ydata, event.dblclick, event.inaxes)
        for controller_key in self.__operating_controller_list:
            print(f"{self.__operating_controller_list}: ", end='')
            # Cursor adjustment. the center of the pixel is 0. So it need 0.5 shift. 
            roi_x = round(event.xdata)
            roi_y = round(event.ydata)
            roi = [roi_x, roi_y, None, None]
            self.__model.set_controller_val(controller_key, roi)



    def change_roi_size(self, val): #val = [x,y,x_length,y_length]
        for roi in self.__operating_controller_list:        
            roi_val = self.__model.get_controller_val(roi).data
            new_roi_val = roi_val + val 
            if new_roi_val[2] < 1 or new_roi_val[3] < 1:
                print("Cant't be smaller ROI size than 1")
                return None
            else:
                self.__model.set_controller_val(roi, new_roi_val)
                return new_roi_val
      
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
        
    def get_operating_controller_list(self):
        return self.__operating_controller_list
    
    def set_operating_controller_list(self, controller_key):
        if controller_key in self.__operating_controller_list:
            self.__operating_controller_list.remove(controller_key)
        else:
            self.__operating_controller_list.append(controller_key)
        
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
            filetypes=(('All files', '*.*'), 
                       ('Tsm files', '*.tsm'),
                       ('Da files', '*.da'), 
                       ('Axon files', '*.abf'),
                       ('WinCP files', '*.wcp')
                      ))
        return fullname
    



        
