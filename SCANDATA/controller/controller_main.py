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


class MainController:
    def __init__(self):
        self.controller_list = []
        
    def create_filename_obj(self, fullname: str) -> object:
        pass
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_imaging_controller(self,filename):
        pass
        self.controller_list.append(ImagingController(filename))

class ImagingController:
    def __init__(self, view, filename_obj):
        self.__filename = filename_obj
        self.view = view
        self.model = None
        
    def create_model(self, filename_obj: object):  
        self.model = DataSet(filename_obj.fullname)  # send filename str
        if self.model == None:
            raise Exception('Failed to create a model.')
        else:
            print('Suceeded to make a model.')
        return self.model

    def initialize_data_window(self):
        self.show_data_repository()
        
    def create_view_data(self, factory_type):
        return self.view_data_repository          .create_view_data(factory_type)
        
    def show_data_repository(self):
        self.view_data_repository            .show_data()

    def set_roi_position(self, event, roi_num=1):
        key = 'Roi' + str(roi_num)
        print(key + ':')
        print(event.button, event.x, event.y, event.xdata, event.ydata)
        roi_x = math.floor(event.xdata)
        roi_y = math.floor(event.ydata)
        roi = [roi_x, roi_y]
        self.model.set_data(key, roi)
    
    def change_roi_size(self, roi_num, val):
        self.model.add_data('Roi' + str(roi_num), val)
        
        
        
        
    def get_controller(self, filename: str, key:str) -> object:
        return self.model.get_data(filename, key)
    
    def count_data(self, filename, key):
        return self.model.count_data(filename, key)
        
    
    


        
"Value object"
class WholeFilename:  # Use it only in a view and controller
    def __init__(self, fullname: str):
        self.__fullname = os.path.join(fullname)  # replace separater for each OS
        self.__filename = os.path.basename(self.__fullname)
        self.__filepath = os.path.dirname(self.__fullname) + os.sep
        self.__abspath = os.path.abspath(fullname)# absolute path
        split_filename = os.path.splitext(self.__filename)
        self.__file_name_no_ext = split_filename[0]
        self.__extension =  split_filename[1]  # get only extension
        
        self.__filename_list = self.__make_filename_list()

    # List need A000-Z999 in the last of filenames
    def __make_filename_list(self) -> list:
        find =  self.__filepath + self.__file_name_no_ext[0:-3] + '*' + str(self.__extension)
        fullname_list = glob.glob(find)
        filename_list = []
        for i in range(len(fullname_list)):
            filename_list.append(os.path.basename(fullname_list[i]))
        return  filename_list

    def __del__(self):
        #print('.')
        #print('Deleted a ImageData object.' + '  myId= {}'.format(id(self)))
        pass
        
    @property
    def fullname(self) -> str:
        return self.__fullname
    
    @property
    def name(self) -> str:
        return self.__filename
    
    @property
    def path(self) -> str:
        return self.__filepath
    
    @property
    def abspath(self) -> str:
        return self.__abspath
    
    @property
    def file_name_no_ext(self) -> str:
        return self.__file_name_no_ext
    
    @property
    def extension(self) -> str:
        return self.__extension
    
    @property
    def filename_list(self) -> list:
        return self.__filename_list
    
    def print_infor(self) -> None:
        print('THe absolute path = ' + self.__abspath)
        print('The full path = ' + self.__fullname)
        print('The file name = ' + self.__filename)
        print('The file path = ' + self.__filepath)
        print('The file name without extension = ' + self.__file_name_no_ext)
        print('The file extension = ' + self.__extension)
        print('The file name list in the same folder = ' + str(self.__filename_list))
        
        




        
