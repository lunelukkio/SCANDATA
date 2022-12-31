# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022

lunelukkio@gmail.com
main for controller
"""

from SCANDATA.model.model_main import ExperimentsInterface
from SCANDATA.view.view_main import View
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import glob


class Controller:
    def __init__(self):
        print('Imported controller')
        
        self.view = None
        self.model = None
        
        self.filename = []
        self.filepath = []
        
    def create_filename_obj(self, fullname: str) -> object:
        filename_obj = WholeFilename(fullname)
        return filename_obj

    def create_model(self, filename, filepath):  
        self.model.create_data_objects(filename, filepath)
        self.filename.append(filename)
        self.filepath.append(filepath)
        
    def roi_controller(self):
        print('ROI controller')
        
    def get_data(self, filename, data_type) -> object:  # value object
        return self.model.get_data(filename.name, data_type)
    
    def set_roi(self, filename, event, roi_num=1, roi_length=[1, 1]):
        print(event.button, event.x, event.y, event.xdata, event.ydata)
        roi_x = math.floor(event.xdata)
        roi_y = math.floor(event.ydata)
        roi = [roi_x, roi_y] + roi_length
        self.model.set_data(filename.name, 'Roi' + str(roi_num), roi)
        return roi   # for ROI Box
    
    def large_roi(self, filename, roi_num):
        old_roi = self.model.get_data(filename.name, 'Roi' + str(roi_num))
        new_roi = old_roi.data + np.array[0, 0, 1, 1]
        self.model.set_data(filename.name, 'Roi' + str(roi_num), new_roi)
        return new_roi
        
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
