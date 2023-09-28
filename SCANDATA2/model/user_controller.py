# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
concrete classes for User controllers
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA2.model.value_object import TraceData, RoiVal, FrameWindowVal, TimeWindowVal
import numpy as np

"""
abstract factory
"""
class UserControllerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_controller(self, val):
        raise NotImplementedError()


"""
contrete factory
"""
class RoiFactory(UserControllerFactory):
    def create_controller(self, data_service):
        return Roi(data_service)
        
class FrameWindowFactory(UserControllerFactory):
    def create_controller(self):
        return FrameWindow()
    
class FrameShiftFactory(UserControllerFactory):
    def create_controller(self):
        return FrameShift()
        
class LineFactory(UserControllerFactory):
    def create_controller(self):
        return Line()
        
class ElecControllerFactory(UserControllerFactory):
    def create_controller(self):
        return ElecController() 
    


"""
abstract product
"""
class UserController(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
        raise NotImplementedError()
        
    @abstractmethod
    def get_infor(self):
        raise NotImplementedError()

    @abstractmethod
    def print_infor(self):
        raise NotImplementedError()
    
    @abstractmethod
    def reset(self):
        raise NotImplementedError()

        

"""
concrete product
"""
class Roi(UserController):
    def __init__(self, get_experiments_method):
        self.get_experiments = get_experiments_method
        self.__roi_obj = RoiVal(40, 40, 2, 2)
        self.__data_dict = {}  # data dict = {filename:frame_type{full:TraceData,ch1:TraceData,ch2:TraceData}}
        self.__mod_list = []
        
        self.__experiments_list = []
        
        self.print_infor()
        
    def __del__(self):  #make a message when this object is deleted.
        #print('.')
        print('----- Deleted a Roi object.' + '  myId={}'.format(id(self)))
        #pass
        
    def set_data(self, x = None, y = None, x_width = None, y_width = None) -> None:
        check_bool = self.check_val(x, y, x_width, y_width)
        if check_bool is True:
            # make a new Roi value object
            self.__roi_obj = RoiVal(x, y, x_width, y_width)  # replace the roi
            for key in self.__experiments_list:
                # get Experiments obj Data using a method in DataService
                frames_dict = self.get_experiments(key).frames_dict
                # make a traces data dict
                for key in frames_dict:  # key = "Full", "Ch1", "Ch2"
                    self.__data_dict[key] = self.trace_culc(frames_dict[key], self.__roi_obj)
            self.print_infor()
        elif check_bool is False:
            print('Failed to make a new ROI value')
            
    # calculation from a frame data
    def trace_culc(self, frames, roi_val):
        roi = roi_val.data
        if roi[0] + roi[2] > self.x_size - 1 or roi[1] + roi[3] > self.y_size - 1: 
            raise Exception("The roi size should be the same as the image size or less")
        if roi[0] < 0 or roi[1] < 0: 
            raise Exception("The roi should be the same as 0 or more")
        if roi[2] < 1 or roi[3] < 1: 
           print("Warning!!!!!! The roi length is 0 or less")

        trace_val = self.__create_fluo_trace(self.__frames_obj, roi)
        self.__trace_obj = TraceData(trace_val, self.__interval)
        
    def __create_fluo_trace(frames_obj, roi) -> np.ndarray:
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frames_obj.data[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data
            
    def __create_time_data(self, trace, interval) -> np.ndarray:
        num_data_point = interval * np.shape(trace)[0]
        time_val = np.linspace(interval, num_data_point, np.shape(trace)[0])
        return time_val
        
    def check_val(self, x = None, y = None, x_width = None, y_width = None) -> None:
        # check the val for existance
        if x is None:
            x = self.__roi_obj.data[0]
        if y is None:
            y = self.__roi_obj.data[1]
        if x_width is None:
            x_width = self.__roi_obj.data[2]
        if y_width is None:
            y_width = self.__roi_obj.data[3]
            
        # check the val as the same or not
        if x == self.__roi_obj.data[0] and \
           y == self.__roi_obj.data[1] and \
           x_width == self.__roi_obj.data[2] and \
           y_width == self.__roi_obj.data[3]:
               print('----- The new ROI value is the same as previous.')
               return False
        # check the val for limit
        else:
            if x < 0 or \
               y < 0 or \
               x_width < 1 or \
               y_width < 1:
                print('ROI value shold be more than 1')
                return False
            else:
                return True

    def add_data(self, x: int, y: int, x_width=0, y_width=0) -> None:
        check_bool = self.check_val(self.__roi_obj.data[0] + x,
                                    self.__roi_obj.data[1] + y,
                                    self.__roi_obj.data[2] + x_width,
                                    self.__roi_obj.data[3] + y_width)
        if check_bool is True:
            add_roi_obj = RoiVal(x, y, x_width, y_width)  # make new additional RoiVal
            self.__roi_obj += add_roi_obj  # override of + in type:RoiVal
            self.print_infor()
            self.notify_observer()
        elif check_bool is False:
            pass
    
    def reset(self) -> None:
        self.__roi_obj = RoiVal(40, 40, 2, 2)
        self.print_infor()
        print('----- Reset ROI and notified')

    @property   
    def get_infor(self):  # get names from observers
        name_list = self.__observer.get_infor()
        return name_list
    
    def print_infor(self) -> None:
        dict_key = list(self.__data_dict.keys())
        print("")
        print(f"ROI = {self.__roi_obj.data}, data_dict_key = {dict_key}")


class FrameWindow(UserController):
    def __init__(self):
        self.__frame_window_obj = FrameWindowVal(0, 0, 1, 1)
        self.__observer = ControllerObserver()
        self.object_num = 0
        #print('Create FrameWindow{}.'.format(self.object_num))

    def set_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        # check data
        print('Tip: Didnt test this check program.')
        if start == self.__frame_window_obj.data[0] and \
           end == self.__frame_window_obj.data[1] and \
           start_width == self.__frame_window_obj.data[2] and \
           end_width == self.__frame_window_obj.data[3]:
               print('----- The new FrameWindow value is the same as previous.')
               return
        self.__frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.print_infor()
        self.notify_observer()
        #print('Set FrameWindow-{} and notified'.format(self.object_num))

        
    def add_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        add_frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.__frame_window_obj += add_frame_window_obj
        self.print_infor()
        self.notify_observer()
        #print('Add to FrameWindow{} and notified'.format(self.object_num))

    def get_data(self) -> object:
        return self.__frame_window_obj
    
    def reset(self) -> None:
        self.__frame_window_obj = FrameWindowVal(0, 0, 0, 0)
        self.print_infor()
        self.notify_observer()
        #print('Reset FrameWindow{} and notified'.format(self.object_num))

    def add_observer(self, observer: object) -> None:
        self.__observer.add_observer(observer)
        #self.notify_observer()  # this message come from a controller
    
    def notify_observer(self) -> None:
        self.__observer.notify_observer(self.__frame_window_obj)
            
    @property
    def observers(self) -> list:
        return self.__observer.observers
    
    def get_infor(self):  # get names from observers
        name_list = self.__observer.get_infor()
        return name_list

    def print_infor(self) -> None:
        name_list = []
        num = len(self.__observer.observers)
        for i in range(num):
            name_list.append(self.__observer.observers[i].name)
        print(f'FrameWindow{self.object_num} observer list = {str(name_list)}, ROI = {self.get_data().data}')


class FrameShift(UserController): 
    def __init__(self):
        self.__observers = []
    
    def set_data(self, val):
        pass

    def get_data(self):
        pass

    def print_infor(self):
        pass

    def reset(self):
        pass

    def add_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass
    
    @property
    def observers(self) -> list:
        return self.__observers
    
    def get_infor(self):
        name_list = []
        for i in range(len(self.__observers)):
            name_list.append(self.__observers[i].name)
        return name_list


class Line(UserController): 
    def __init__(self):
        self.__observers = []
    
    def set_data(self, val):
        pass

    def get_data(self):
        pass

    def print_infor(self):
        pass

    def reset(self):
        pass

    def add_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass
    
    @property
    def observers(self) -> list:
        return self.__observers
    
    def get_infor(self):
        name_list = []
        for i in range(len(self.__observers)):
            name_list.append(self.__observers[i].name)
        return name_list
    
    
class ElecController(UserController):
    def __init__(self):
        self.__time_window_obj = TimeWindowVal(0, 100)
        self.__observer = ControllerObserver()
        self.object_num = 0
        #print('Create TimeController{}.'.format(self.object_num))

    def set_data(self, start: int, end: int) -> None:
        self.__time_window_obj = TimeWindowVal(start, end)
        self.print_infor()
        self.notify_observer()
        #print('Set TimeWindow{} and notified'.format(self.object_num))

    def add_data(self, start: int, end: int) -> None:
        add_time_window_obj = TimeWindowVal(start, end)
        self.__time_window_obj += add_time_window_obj
        self.print_infor()
        self.notify_observer()
        #print('Add to TimeWindow{} and notified'.format(self.object_num))

    def get_data(self) -> object:
        return self.__time_window_obj
    
    def reset(self) -> None:
        self.__time_window_obj = FrameWindowVal(0, 100)
        self.print_infor()
        self.notify_observer()
        #print('Reset FrameWindow{} and notified'.format(self.object_num))
    
    def add_observer(self, observer: object) -> None:
        self.__observer.add_observer(observer)
        #self.notify_observer()  # this message come from a controller
    
    def notify_observer(self) -> None:
        self.__observer.notify_observer(self.__time_window_obj)
            
    @property
    def observers(self) -> list:
        return self.__observer.observers
    
    def get_infor(self):  # get names from observers
        name_list = self.__observer.get_infor()
        return name_list

    def print_infor(self) -> None:
        name_list = []
        num = len(self.__observer.observers)
        for i in range(num):
            name_list.append(self.__observer.observers[i].name)
        print(f'ElecController{self.object_num} observer list = {str(name_list)}, ROI = {self.get_data().data}')
        
class ControllerObserver:
    def __init__(self):
        self.__observers = []
        
    def add_observer(self, observer):
        for check_observer in self.__observers:
            if check_observer == observer:
                self.remove_observer(observer)
                return
        self.__observers.append(observer)
        self.__observers = sorted(self.__observers, key=lambda x: str(x.sort_num)+x.name)

    def remove_observer(self, observer):
        self.__observers.remove(observer)
        name_list = []
        for i in self.__observers:
            name_list.append(i.name)
            
    def notify_observer(self, controller_obj):
        name_list = []
        for observer in self.__observers:
            name_list.append(observer.name)
        print('----- Notify to observers: ' + str(name_list))
        """ The order of ViewDatas should be after Data entiries """
        for observer_name in self.__observers:
            observer_name.update(controller_obj.data)
            
    def get_infor(self):
        name_list = []
        for observer in self.__observers:
            name_list.append(observer.name)
        return name_list

    @property
    def observers(self) -> list:
        return self.__observers
    