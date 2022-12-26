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
        self.__roi_obj = RoiVal(40, 40, 1, 1)
        self.object_num = 0  # instance number
        self.__observers = []
        print('Created a new ROI.')
        
    def check_val(self) -> None:
        if self.__x < 0 or self.__y < 0 or self.__x_length < 0 or self.__y_length < 0:
            raise ValueError('ROI value shold be more than 1')

    def set_data(self, x: int, y: int, x_width=0, y_width=0) -> None:
        self.__roi_obj = RoiVal(x, y, x_width, y_width)
        self.notify_observer()
        print('Set the ROI{} and notified',format(self.object_num))
        self.print_val()
      
    def add_data(self, x: int, y: int, x_width=0, y_width=0) -> None:
        add_roi_obj = RoiVal(x, y, x_width, y_width)
        new_roi_obj = self.__roi_obj + add_roi_obj
        self.__roi_obj = new_roi_obj
        self.notify_observer()
        print('Added to the ROI and notified')
        self.print_val()

    def get_data(self) -> object:
        return self.__roi_obj.roi_val
    
    def reset(self) -> None:
        self.__roi_obj = RoiVal(40, 40, 1, 1)
        self.notify_observer()
        print('Reset the ROI and notified')
        self.print_val()

    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def remove_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        val = self.get_data()
        for observer_name in self.__observers:
            observer_name.update(val)
    
    
    def print_val(self) -> None:
        print('ROI = ' + str(self.get_data()) + 
              ', observer = ' + str(self.__observers))
        
            
"Value object for Roi value"
class RoiVal():
    def __init__(self, x: int, y: int, x_width: int, y_width: int):         

        if x < 0 or y < 0 or x_width < 0 or y_width < 0:
            raise Exception("ROI values should be 0 or more")
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__x = x
        self.__y = y
        self.__x_width = x_width
        self.__y_width = y_width
        self.__data_type = called_class.__class__.__name__
        print(self.__data_type + ' made a RoiVal' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        print('Deleted a RoiVal object.' + '  myId={}'.format(id(self)))
        
    #override for "+"
    def __add__(self, other: object) -> object:
        if self.__data_type != other.data_type:
            raise Exception("Wrong FrameWindowVal data")
        self.__x += other.roi_val[0]
        self.__y += other.roi_val[1]
        self.__x_width += other.roi_val[2]
        self.__y_width += other.roi_val[3]
        return self
        
    @property
    def roi_val(self) -> list:
        return [self.__x,
                self.__y,
                self.__x_width,
                self.__y_width]
    
    @roi_val.setter
    def roi_val(self, x, y, x_width=1, y_width=1):  
        raise Exception("RoiVal is a value object (Immutable).")
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    
class FrameWindow(ModelController):
    def __init__(self):
        self.__frame_window_obj = FrameWindowVal(0, 0, 1, 1)
        self.__observers = []
        self.object_num = 0
        print('Create a new FrameWindow.')

    def set_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        self.__frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.notify_observer()
        print('Set the frame_window_val and notified')
        self.print_val()
        
    def add_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        add_frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        new_frame_window_obj = self.__frame_window_obj + add_frame_window_obj
        self.__frame_window_obj = new_frame_window_obj
        self.notify_observer()
        print('Added to the frame_window_val and notified')
        self.print_val()

    def get_data(self) -> object:
        return self.__frame_window_obj.frame_window_val
    
    def reset(self) -> None:
        self.__frame_window_obj = FrameWindowVal(0, 0, 0, 0)
        self.notify_observer()
        print('Reset the frame_window_val and notified')
        self.print_val()
    
    def add_observer(self, observer: object) -> None:
        self.__observers.append(observer)
        
    def remove_observer(self, observer: object) -> None:
        self.__observers.remove(observer)
    
    def notify_observer(self) -> None:
        for observer_name in self.__observers:
            observer_name.update(self.get_data())

    def print_val(self) -> None:
        print('frame_window_val = ' + str(self.get_data()) + 
              ', observer = ' + str(self.__observers))


"Value object for FrameWindow value"
class FrameWindowVal():
    def __init__(self, start: int, end: int, start_width: int, end_width: int):
        if start > end: 
            raise Exception("FrameWindow the end values should be the same or larger than the start value")
            

        if start_width < 0 or end_width < 0:
            raise Exception("FrameWindow width values should be 0 or more")
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__frame_start = start  # (frame)
        self.__frame_end = end  # (frame)
        self.__frame_start_width = start_width
        self.__frame_end_width = end_width
        self.__data_type = called_class.__class__.__name__
        print(self.__data_type + ' made a FrameWindowVal' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        print('.')
        #print('Deleted a FrameWindowVal object.' + '  myId={}'.format(id(self)))
        
    #override for "+"
    def __add__(self, other: object) -> object:
        if self.__data_type != other.data_type:
            raise Exception("Wrong FrameWindowVal data")
        self.__frame_start += other.frame_window_val[0]
        self.__frame_end += other.frame_window_val[1]
        self.__frame_start_width += other.frame_window_val[2]
        self.__frame_end_width += other.frame_window_val[3]
        return self
        
    @property
    def frame_window_val(self) -> list:
        return [self.__frame_start,
                self.__frame_end,
                self.__frame_start_width,
                self.__frame_end_width]
    
    @frame_window_val.setter
    def frame_window_val(self, start, end, start_width=1, end_width=1):  
        raise Exception("FrameWindowVal is a value object (Immutable).")
    
    @property
    def data_type(self) -> str:
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