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

    @abstractmethod
    def set_val(self, val):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def print_val(self):
        pass

    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def delete_observer(self, observer):
        pass

    @abstractmethod
    def notify_observer(self):
        pass

class RoiVal(ControlVal):
    def __init__(self):
        self.__observers = []
        
        self.__x = 40
        self.__y = 40
        self.__x_length = 2
        self.__y_length = 2
        self.__roi_num = 1
        print('Imported a roi val class.')

    def set_val(self, val):
        self.__x = val[0]
        self.__y = val[1]
        self.__x_length = val[2]
        self.__y_length = val[3]
        self.__roi_num = val[4]
        
        self.notify_observer()

    def get_data(self) -> list:
        return [self.__x,
                self.__y,
                self.__x_length,
                self.__y_length,
                self.__roi_num]
        
    def create_roi(self, x):
        pass

    def delete_roi(self):
        pass
    
    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def delete_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        for observer_name in self.__observers:
            observer_name.update(self)
            print('')
    
    def print_val(self):
        print('set val = ' +
              str(self.__x) + ' ,' +
              str(self.__x_length) + ' ,' +
              str(self.__y) + ' ,' +
              str(self.__y_length) + ' ,' +
              str(self.__roi_num))

    
class CellImageVal():
    def __init__(self):
        self.__frame_start = 0
        self.__frame_end = 4
        print('Imported a cell image val class.')

    def set_val(self, val):
        self.__frame_start = val[0]
        self.__frame_end = val[1]

    def get_data(self) -> list:
        return [self.__frame_start,
                self.__frame_end]

    def print_val(self):
        print('cell image val = ' +
              str(self.__frame_start) + ' ,' +
              str(self.__frame_end))


class DifImageVal():
    def __init__(self):
        self.__dif_base = 50
        self.__dif_df = 100
        self.__dif_base_length = 5
        self.__dif_df_length = 5
        print('Imported a dif image val class.')
    
    def set_val(self, val):
        self.__dif_base = val[0]
        self.__dif_df = val[1]
        self.__dif_base_length = val[2]
        self.__dif_df_length = val[3]
        
    def get_data(self) -> list:
        return [self.__dif_base, 
                self.__dif_df, 
                self.__dif_base_length, 
                self.__dif_df_length]

    def print_val(self):
        print('dif image val = ' +
              str(self.__dif_base) + ' ,' +
              str(self.__dif_df) + ' ,' +
              str(self.__dif_base_length) + ' ,' +
              str(self.__dif_df_length))
        
    
class ModVal():
    def __init__(self):
        self.__mod_list = ['mod_list']
        print('Imported a mod val class.')
        
    def set_val(self, val):
        pass
        
    def get_data(self) -> list:
        return self.__mod_list
            
    def print_val(self):
        pass


class SpacialAveVal():
    def __init__(self):
        self.__spacial_filter = 8
        print('Imported a spacial ave val class.')
    
    def set_val(self, val):
        pass

    def get_data(self):
        return self.__spacial_filter

    def print_val(self):
        pass

