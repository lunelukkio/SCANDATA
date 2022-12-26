# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
concrete classes for model controllers
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA.model.data_factory import FullFrames, ChFrames
from SCANDATA.model.data_factory import CellImage, DifImage
from SCANDATA.model.data_factory import FluoTrace, ElecTrace
import inspect

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
class RoiFactory(ModelControllerFactory):
    def create_model_controller(self):
        return Roi()
        
class FrameWindowFactory(ModelControllerFactory):
    def create_model_controller(self):
        return FrameWindow()
    
class FrameShiftFactory(ModelControllerFactory):
    def create_model_controller(self):
        return FrameShift()
        
class LineFactory(ModelControllerFactory):
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
            
    
class FrameWindow(ModelController):
    def __init__(self):
        self.__frame_window_obj = FrameWindowVal(0, 0, 1, 1)
        self.__observers = []
        self.object_num = 0
        print('Create a new time window.')

    def set_data(self, start, end, start_width=1, end_width=1):
        self.__frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.notify_observer()
        print('Set the time window and notified')
        self.print_val()
        
    def add_data(self, start, end, start_width=0, end_width=0):
        add_frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        new_frame_window_obj = self.__frame_window_obj + add_frame_window_obj
        self.__frame_window_obj = new_frame_window_obj
        self.notify_observer()
        print('Set the time window and notified')
        self.print_val()

    def get_data(self):
        return self.__frame_window_obj.frame_window_val
    
    def reset(self):
        self.__frame_window_obj = FrameWindowVal(40, 40, 1, 1)
        self.notify_observer()
        print('Reset the time window and notified')
        self.print_val()
    
    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def remove_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        for observer_name in self.__observers:
            observer_name.update(self.get_data())

    def print_val(self):
        print('Time window = ' + str(self.get_data()) + 
              ', observer = ' + str(self.__observers))





"Value object for FrameWindow value"
class FrameWindowVal():
    def __init__(self, start, end, start_width, end_width):
        if start > end: 
            raise Exception("Time Window the end values should be the same or larger than the start value")
            

        if start_width < 0 or end_width < 0:
            raise Exception("Time Window width values should be 0 or more")
        self.__frame_start = start  # (frame)
        self.__frame_end = end  # (frame)
        self.__time_start_width = start_width
        self.__time_end_width = end_width
        
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data_type = called_class.__class__.__name__
        
    def __del__(self):
        print('Deleted a FrameWindowVal object.' + '  myId={}'.format(id(self)))
        
    #override for "+"
    def __add__(self, other):
        if self.__data_type != other.data_type:
            raise Exception("Wrong FrameWindowVal data")
        print(self.__data_type)
        self.__frame_start += other.frame_window_val[0]
        self.__frame_end += other.frame_window_val[1]
        self.__time_start_width += other.frame_window_val[2]
        self.__time_end_width += other.frame_window_val[3]
        return self
        
    @property
    def frame_window_val(self):
        return [self.__frame_start,
                self.__frame_end,
                self.__time_start_width,
                self.__time_end_width]
    
    @frame_window_val.setter
    def frame_window_val(self, start, end, start_width=1, end_width=1):  
        raise Exception("This is a value object (Immutable).")
    
    @property
    def data_type(self):
        return self.__data_type
        


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