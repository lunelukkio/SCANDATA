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
    def set_controller(self, x, y, x_width, y_width):
        raise NotImplementedError()
    
    @abstractmethod
    def add_experiments(self, filename_str):
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
        
    def __del__(self):  #make a message when this object is deleted.
        #print('.')
        print('----- Deleted a Roi object.' + '  myId={}'.format(id(self)))
        #pass
        
        # make a new Roi value object
    def set_controller(self, roi_value_list):
        x = roi_value_list[0]
        y = roi_value_list[1]
        x_width = roi_value_list[2]
        y_width = roi_value_list[3]
        self.__roi_obj = RoiVal(x, y, x_width, y_width)  # replace the roi
        
        
    def set_data(self):
        # repeat the number of experiments
        for filename_key in list(self.__data_dict.keys()):
            # get Experiments obj Data using a method in DataService
            experiments_entity = self.get_experiments(filename_key)
            # make a traces data dict
            new_dict = {}
            for key in experiments_entity.frames_dict.keys():  # key = "Full", "Ch1", "Ch2"
                dict_val = self.__trace_culc(experiments_entity.frames_dict[key], self.__roi_obj)
                new_dict[key] = dict_val
            self.__data_dict[filename_key] = new_dict
        print(f"set ROI: {self.__roi_obj.data}")
            
    def add_experiments(self, filename_str):
        self.__data_dict[filename_str] = None
        self.set_data()
        self.print_infor()
            
    # calculate a trace from a single frames data with a roi value object
    def __trace_culc(self, frames_obj, roi_obj):
        # check value is correct
        self.__check_val(frames_obj, roi_obj)
        # make raw trace data
        x = roi_obj.data[0]
        y = roi_obj.data[1]
        x_length = roi_obj.data[2]
        y_length = roi_obj.data[3]
        mean_data = np.mean(frames_obj.data[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        # make a trace value object
        trace_obj = TraceData(mean_data, frames_obj.interval)
        return trace_obj
        
    def __check_val(self, frames_obj, roi_obj) -> None:
        # convert to raw values
        roi = roi_obj.data
        # check the value is correct. See RoiVal class.
        frames_size = frames_obj.shape
        if roi[0] + roi[2] > frames_size[0] or roi[1] + roi[3] > frames_size[1]: 
            raise Exception("The roi size should be the same as the image size or less")
        if roi[0] < 0 or roi[1] < 0: 
            raise Exception("The roi should be the same as 0 or more")
        if roi[2] < 0 or roi[3] < 0: 
            raise Exception("The roi length should be the same as 0 or more")
        else:
            return True
    
    def print_infor(self) -> None:
        if not self.__data_dict:
            print("Data_dict is empty")
            return
        dict_key = list(self.__data_dict.keys())
        if self.__data_dict[dict_key[0]] is None:
            print("No data in the ROI")
            return
        print("ROI information ===================")
        print(f"ROI = {self.__roi_obj.data}")
        print("-- data_dict LIST -- ")
        for experiments in dict_key:
            key_list = list(self.__data_dict[experiments].keys())
            print(f"{experiments} = {key_list}")
        print("=============== ROI information END")
            
    @property
    def data_dict(self):
        return self.__data_dict





    def add_data(self, x: int, y: int, x_width=0, y_width=0) -> None:
        check_bool = self.__check_val(self.__roi_obj.data[0] + x,
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
    
