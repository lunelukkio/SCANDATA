# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022

lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from model_package.displayed_data_factory import FullFluoTrace
from model_package.displayed_data_factory import ChFluoTrace
from model_package.displayed_data_factory import ElecTrace
from model_package.displayed_data_factory import CellImage

class ControlVal(metaclass=ABCMeta):
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def delete_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observer(self):
        for observer_name in self.__observers:
            observer_name.update(self)
            
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def set_val(self, val):
        pass
    


class RoiVal():
    def __init__(self):
        self.__observers = [FullFluoTrace()]
        
        self.__x = 40
        self.__y = 40
        self.__x_length = 2
        self.__y_length = 2
        self.__roi_num = 1

    def create_roi(self, x):
        pass

        
    def get_data(self) -> list:
        return [self.__x, self.__y, self.__x_length, self.__y_length, self.__roi_num]
    
    def set_val(self, val):
        self.__x = val[0]
        self.__y = val[1]
        self.__x_length = val[2]
        self.__y_length = val[3]
        self.__roi_num = val[4]
        
        #self.notify_observer()

    def delete_roi(self):
        pass
        

    
class CellImageVal():
    def __init__(self):
    
        self.__dif_base = 50
        self.__dif_base_length = 5
        self.__dif_df = 100
        self.__dif_df_length = 5
        self.__ave_num_cell_image = [0,4]  # [start frame, end frame]
        self.__mod_list = ['mod_list']
        self.__spacial_filter = 8
        
        
    def get_data(self) -> list:
            return self.__ave_num_cell_image
    
    def set_val(self, val):
        self.__ave_num_cell_image = [val[0], val[1]]
