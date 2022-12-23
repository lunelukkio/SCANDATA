# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
concrete classes for model controllers
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from model.data_factory import FullFrame, ChFrame
from model.data_factory import CellImage, DifImage
from model.data_factory import FluoTrace, ElecTrace

"""
abstract factory
"""
class ModelControllerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_model_controller(self, val):
        pass


"""
contrete factory
"""
class RoiFactory:
    def create_model_controller(self):
        return Roi()
        
class TimeWindowFactory:
    def create_model_controller(self):
        return TimeWindow()
    
class FrameShiftFactory:
    def create_model_controller(self):
        return FrameShift()
        
class LineFactory:
    def create_model_controller(self):
        return Line()


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
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observer(self):
        pass


"""
concrete product
"""
class Roi(ModelController):
    def __init__(self):
        self.__x = 40
        self.__y = 40
        self.__x_length = 1
        self.__y_length = 1
        
        self.num = 0  # instance number
        self.__observers = []
        print('Created a new ROI.')
        
    def check_val(self) -> None:
        if self.__x < 0 or self.__y < 0 or self.__x_length < 0 or self.__y_length < 0:
            raise ValueError('ROI value shold be more than 1')

    def set_data(self, val) -> None:
        self.__x = val[0]
        self.__y = val[1]
        self.__x_length = val[2]
        self.__y_length = val[3]
        
        self.check_val()
        
        self.notify_observer()
        print('Set the ROI position and notified')
        self.print_val()


    def get_data(self) -> list:
        return [self.__x,
                self.__y,
                self.__x_length,
                self.__y_length]
    
    def reset(self):
        self.__x = 40
        self.__y = 40
        self.__x_length = 1
        self.__y_length = 1
        
        self.__observers = []
        print('Reset ROI' + str(self.num))
    
    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def remove_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        val = self.get_data()
        for observer_name in self.__observers:
            observer_name.update(val)
    
    def print_val(self):
        print('ROI' + str(self.num) + ' = ' +
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
        
    def remove_observer(self, observer):
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
    num_instance = 0  # Class member to count the number of instance
    
    def __init__(self):
        FrameShift.num_instance += 1
    
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

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass


class Line(ModelController):
    num_instance = 0  # Class member to count the number of instance
    
    def __init__(self):
        Line.num_instance += 1
    
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

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass