# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022

lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from model_package.data_factory import Data3D, Data2D, Data1D

"""
abstract factory
"""
class ControlValFactory:
    @abstractmethod
    def create_control_val(self, val):
        pass
    
"""
abstract product
"""
class ControlValInterface(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self, val):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def print_val(self):
        pass
    
    @abstractmethod
    def reset(self):
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

"""
contrete factory
"""
class RoiFactory:
    def __init__(self):
        self.val = []
        
    def create_control_val(self, val):
        return Roi(val)
        
class TimeWindowFactory:
    def __init__(self):
        self.val = []
        
    def create_control_val(self, val):
        return TimeWindow(val)
    
class FrameShiftFactory:
    def __init__(self):
        self.val = []
        
    def create_control_val(self, val):
        return FrameShift(val)
        
class LineFactory:
    def __init__(self):
        self.val = []
        
    def create_control_val(self, val):
        return Line(val)
        

"""
concrete product
"""
class Roi(ControlValInterface):
    def __init__(self):
        self.__observers = []
        
        self.__x = 40
        self.__y = 40
        self.__x_length = 1
        self.__y_length = 1
        print('Created a ROI.')

    def set_data(self, val):
        self.__x = val[0]
        self.__y = val[1]
        self.__x_length = val[2]
        self.__y_length = val[3]
        
        self.notify_observer()
        print('Set the ROI position ' + str(val) + ', and notified.')

    def get_data(self) -> list:
        return [self.__x,
                self.__y,
                self.__x_length,
                self.__y_length]
    
    def reset(self):
        pass
        
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
            observer_name.update_data(self)
    
    def print_val(self):
        print('set val = ' +
              str(self.__x) + ' ,' +
              str(self.__y) + ' ,' +
              str(self.__x_length) + ' ,' +
              str(self.__y_length) + '\n' +
              'observer = ' +
              str(self.__observers))

    
class TimeWindow(ControlValInterface):
    def __init__(self):
        self.__frame_start = 0
        self.__frame_end = 1
        self.__time_start_width = 10  #(ms)
        self.__time_end_width = 10
        self.__observers = []
        print('Imported a cell image val class.')

    def set_data(self, val):
        self.__frame_start = val[0]
        self.__frame_end = val[1]
        
        self.notify_observer()

    def get_data(self) -> list:
        return [self.__frame_start,
                self.__frame_end]
    
    def reset(self):
        pass
    
    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def delete_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        for observer_name in self.__observers:
            observer_name.update_data(self)

    def print_val(self):
        print('cell image val = ' +
              str(self.__frame_start) + ' ,' +
              str(self.__frame_end))
        
class FrameShift:
    def set_data(self, val):
        pass

    def get_data(self):
        pass

    def print_val(self):
        pass

    def reset(self):
        pass

    def add_observer(self, observer):
        pass

    def delete_observer(self, observer):
        pass

    def notify_observer(self):
        pass


class Line:
    def set_data(self, val):
        pass

    def get_data(self):
        pass

    def print_val(self):
        pass

    def reset(self):
        pass

    def add_observer(self, observer):
        pass

    def delete_observer(self, observer):
        pass

    def notify_observer(self):
        pass