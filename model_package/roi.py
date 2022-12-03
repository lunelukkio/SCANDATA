# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022

lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from model_package.data_factory import FullFrame, ChFrame
from model_package.data_factory import CellImage, DifImage
from model_package.data_factory import FluoTrace, ElecTrace

"""
abstract factory
"""
class ModelControllerFactory:
    @abstractmethod
    def create_control_val(self, val):
        pass
    
"""
abstract product
"""
class ModelController(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
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
class Roi(ModelController):
    num_instance = 0  # Class member to count the number of instance
    
    def __init__(self):
        Roi.num_instance += 1
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
        print('Set the ROI position and notified')
        self.print_val()


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
        val = self.get_data()
        for observer_name in self.__observers:
            observer_name.update(val)
    
    def print_val(self):
        print('ROI = ' +
              str(self.__x) + ' ,' +
              str(self.__y) + ' ,' +
              str(self.__x_length) + ' ,' +
              str(self.__y_length) + '\n' +
              'observer = ' +
              str(self.__observers))

    
class TimeWindow(ModelController):
    num_instance = 0  # Class member to count the number of instance

    def __init__(self):
        TimeWindow.num_instance += 1
        
        self.__frame_start = 5
        self.__frame_end = 10
        self.__time_start_width = 1  #(ms)
        self.__time_end_width = 1
        self.__observers = []
        print('Imported a cell image val class.')

    def set_data(self, val):
        self.__frame_start = val[0]
        self.__frame_end = val[1]
        self.__time_start_width = val[2]
        self.__time_end_width = val[3]
        
        self.notify_observer()
        
        print('Set the time window and notified')
        self.print_val()

    def get_data(self):
        return [self.__frame_start,
                self.__frame_end,
                self.__time_start_width,
                self.__time_end_width]
    
    def reset(self):
        pass
    
    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def delete_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        val = self.get_data()
        for observer_name in self.__observers:
            observer_name.update(val)

    def print_val(self):
        print('Time window = ' +
              str(self.__frame_start) + ' ,' +
              str(self.__frame_end) + ' ,' +
              str(self.__time_start_width) + ' ,' +
              str(self.__time_end_width) + '\n' +
              'observer = ' +
              str(self.__observers))


class FrameShift(ModelController):
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


class Line(ModelController):
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