# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
concrete classes for model controllers
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import RoiVal, FrameWindowVal

"""
abstract factory
"""
class ModelControllerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_controller(self, val):
        raise NotImplementedError()


"""
contrete factory
"""
class RoiFactory(ModelControllerFactory):
    def create_controller(self):
        return Roi()
        
class FrameWindowFactory(ModelControllerFactory):
    def create_controller(self):
        return FrameWindow()
    
class FrameShiftFactory(ModelControllerFactory):
    def create_controller(self):
        return FrameShift()
        
class LineFactory(ModelControllerFactory):
    def create_controller(self):
        return Line()


"""
abstract product
"""
class ModelController(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
        raise NotImplementedError()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()

    @abstractmethod
    def print_val(self):
        raise NotImplementedError()
    
    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def add_observer(self, observer):
        raise NotImplementedError()

    @abstractmethod
    def remove_observer(self, observer):
        raise NotImplementedError()

    @abstractmethod
    def notify_observer(self):
        raise NotImplementedError()


"""
concrete product
"""
class Roi(ModelController):
    def __init__(self):
        self.__roi_obj = RoiVal(40, 40, 1, 1)
        self.object_num = 0  # instance number
        self.__observers = []
        #print('Created ROI-{}.'.format(self.object_num))
        
    def check_val(self) -> None:
        if self.__x < 0 or self.__y < 0 or self.__x_length < 0 or self.__y_length < 0:
            raise ValueError('ROI value shold be more than 1')

    def set_data(self, x: int, y: int, x_width=1, y_width=1) -> None:
        self.__roi_obj = RoiVal(x, y, x_width, y_width)
        self.notify_observer()
        print('Set ROI-{} and notified'.format(self.object_num))
        self.print_val()
      
    def add_data(self, x: int, y: int, x_width=0, y_width=0) -> None:
        add_roi_obj = RoiVal(x, y, x_width, y_width)
        self.__roi_obj += add_roi_obj
        self.notify_observer()
        print('Add to ROI-{} and notified'.format(self.object_num))
        self.print_val()

    def get_data(self) -> object:
        return self.__roi_obj
    
    def reset(self) -> None:
        self.__roi_obj = RoiVal(40, 40, 1, 1)
        self.notify_observer()
        print('Reset ROI-{} and notified'.format(self.object_num))
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
        print('ROI-{} = '.format(self.object_num) + str(self.get_data().data) + 
              ', observer = ' + str(self.__observers))
        
    
    
class FrameWindow(ModelController):
    def __init__(self):
        self.__frame_window_obj = FrameWindowVal(0, 0, 1, 1)
        self.__observers = []
        self.object_num = 0
        #print('Create FrameWindow-{}.'.format(self.object_num))

    def set_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        self.__frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.notify_observer()
        print('Set FrameWindow-{} and notified'.format(self.object_num))
        self.print_val()
        
    def add_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        add_frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.__frame_window_obj += add_frame_window_obj
        self.notify_observer()
        print('Add to FrameWindow-{} and notified'.format(self.object_num))
        self.print_val()

    def get_data(self) -> object:
        return self.__frame_window_obj
    
    def reset(self) -> None:
        self.__frame_window_obj = FrameWindowVal(0, 0, 0, 0)
        self.notify_observer()
        print('Reset FrameWindow-{} and notified'.format(self.object_num))
        self.print_val()
    
    def add_observer(self, observer: object) -> None:
        self.__observers.append(observer)
        
    def remove_observer(self, observer: object) -> None:
        self.__observers.remove(observer)
    
    def notify_observer(self) -> None:
        for observer_name in self.__observers:
            observer_name.update(self.get_data())

    def print_val(self) -> None:
        print('FrameWindow-{} = '.format(self.object_num) + str(self.get_data()) + 
              ', observer = ' + str(self.__observers))


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