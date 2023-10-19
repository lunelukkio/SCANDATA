# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
concrete classes for User controllers
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA2.model.value_object import TraceData, ImageData
from SCANDATA2.model.value_object import RoiVal, TimeWindowVal
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
    def create_controller(self, get_experiments_method):
        return Roi(get_experiments_method)
        
class ImageControllerFactory(UserControllerFactory):
    def create_controller(self, get_experiments_method):
        return ImageController(get_experiments_method)
    
class TraceControllerFactory(UserControllerFactory):
    def create_controller(self, get_experiments_method):
        return TraceController(get_experiments_method) 
    
class FrameShiftFactory(UserControllerFactory):
    def create_controller(self):
        return FrameShift()
        
class LineFactory(UserControllerFactory):
    def create_controller(self):
        return Line()
        

    


"""
abstract product
"""
class UserController(metaclass=ABCMeta):
    @abstractmethod
    def set_controller(self, val_list:list):
        raise NotImplementedError()
    
    @abstractmethod
    def add_experiments(self, filename_key):
        raise NotImplementedError()

    @abstractmethod
    def add_data(self, filename_key, data_key):
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
        self.__data_dict = {}  # data dict = {filename:frame_type{full:TraceData_value obj,ch1:TraceData,ch2:TraceData}}
        self.__mod_list = []
        
    def __del__(self):  #make a message when this object is deleted.
        #print('.')
        print('----- Deleted a Roi object.' + '  myId={}'.format(id(self)))
        #pass
        
        # make a new Roi value object
    def set_controller(self, roi_value_list: list):
        for i in range(4):
            if roi_value_list[i] == None:
                roi_value_list[i] = self.__roi_obj.data[i]
        x = roi_value_list[0]
        y = roi_value_list[1]
        x_width = roi_value_list[2]
        y_width = roi_value_list[3]
        self.__roi_obj = RoiVal(x, y, x_width, y_width)  # replace the roi
        self.set_data()

    def set_data(self):
        # repeat the number of experiments
        for filename_key in list(self.__data_dict.keys()):
            # get Experiments obj Data using a method in DataService
            experiments_entity = self.get_experiments(filename_key)
            # make a traces data dict
            filtered_keys = [key for key in experiments_entity.frames_dict.keys() if key in self.__data_dict[filename_key].keys()]
            for key in filtered_keys:  # key = "Full", "Ch1", "Ch2"
                dict_val = self.__trace_culc(experiments_entity.frames_dict[key], self.__roi_obj)
                self.__data_dict[filename_key][key] = dict_val
        print(f"set ROI: {self.__roi_obj.data}")
            
    def get_data(self):
        return self.__data_dict
        
    def add_experiments(self, filename_key):
        if filename_key in self.__data_dict.keys():
            del self.__data_dict[filename_key]  
        else:
            self.__data_dict[filename_key] = {}
            experiments_entity = self.get_experiments(filename_key)
            original_data_list = experiments_entity.frames_dict.keys()
            for data_key in original_data_list:
                self.__data_dict[filename_key][data_key] = None
        self.set_data()
        self.print_infor()
        
    def add_data(self, filename_key, data_key):
        if filename_key in self.__data_dict.keys():
            if data_key in self.__data_dict[filename_key].keys():
                del self.__data_dict[filename_key][data_key]
            else:
                self.__data_dict[filename_key][data_key] = None
        else:
            print(f"No {filename_key} in this ROI")
        self.set_data()
        self.print_infor()
            
    # calculate a trace from a single frames data with a roi value object
    def __trace_culc(self, frames_obj, roi_obj):
        # check value is correct
        #self.__check_val(frames_obj, roi_obj)
        # make raw trace data
        x = roi_obj.data[0]
        y = roi_obj.data[1]
        x_width = roi_obj.data[2]
        y_width = roi_obj.data[3]
        
        mean_data = np.mean(frames_obj.data[x:x+x_width, y:y+y_width, :], axis = 0) #slice end doesn't include to slice
        mean_data = np.mean(mean_data, axis = 0)
        # make a trace value object
        return TraceData(mean_data, frames_obj.interval)
        
    def __check_val(self, frames_obj, roi_obj) -> bool:
        # convert to raw values
        roi = roi_obj.data
        # check the value is correct. See RoiVal class.
        frames_size = frames_obj.shape
        print("t      tttttttttttttttttttttttttttttttttt ROI.__check_val")
        print(roi[0])
        print(roi[2])
        if roi[0] + roi[2]-1 > frames_size[0] or roi[1] + roi[3] -1> frames_size[1]:  #width is always 1 or more.
            raise Exception("The roi size should be the same as the image size or less")
        if roi[0] < 0 or roi[1] < 0: 
            raise Exception("The roi should be the same as 0 or more")
        if roi[2] < 1 or roi[3] < 1: 
            raise Exception("The roi width should be the same as 1 or more")
        else:
            return True
    
    def reset(self) -> None:
        self.set_controller([40, 40, 2, 2])
    
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
    
    @property
    def roi_obj(self):
        return self.__roi_obj
        
        

class ImageController(UserController):
    def __init__(self, get_experiments_method):
        self.get_experiments = get_experiments_method
        self.__time_window_obj = TimeWindowVal(0, 1)
        self.__data_dict = {}  # data dict = {filename:frame_type{full:ImageData,ch1:ImageData,ch2:ImageData}}
        self.__mod_list = []
        
    def __del__(self):  #make a message when this object is deleted.
        #print('.')
        print('----- Deleted a ImageCOntroller object.' + '  myId={}'.format(id(self)))
        #pass

        # make a new Roi value object
    def set_controller(self, window_value_list: list):  #value_list = [start, width]
        start = window_value_list[0]
        width = window_value_list[1]

        self.__time_window_obj = TimeWindowVal(start, width)  # replace the roi
        self.set_data()

    def set_data(self):
        # repeat the number of experiments
        for filename_key in list(self.__data_dict.keys()):
            # get Experiments obj Data using a method in DataService
            experiments_entity = self.get_experiments(filename_key)
            # make a image data dict
            new_dict = {}
            for key in experiments_entity.frames_dict.keys():  # key = "ELEC1", "ELEC2", "ELEC3"
                dict_val = self.__image_culc(experiments_entity.frames_dict[key], self.__time_window_obj)
                new_dict[key] = dict_val
            self.__data_dict[filename_key] = new_dict
        print(f"set TraceController: {self.__time_window_obj.data}")

    def add_experiments(self, filename_str):
        self.__data_dict[filename_str] = None
        self.set_data()
        self.print_infor()
        
    def add_data(self, filename_key, data_key):
        pass
        
    def show_data(self, filename_key, data_key, axis=None):  # axis = MatplotLib axis
        if axis is None:
            self.__data_dict[filename_key][data_key.upper()].show_data()
        else:
            self.__data_dict[filename_key][data_key.upper()].show_data(axis)
            
    # calculate a image from a single frames data with a time window value object
    def __image_culc(self, frames_obj, time_window_obj):
        # check value is correct
        self.__check_val(frames_obj, time_window_obj)
        # make raw trace data
        start = time_window_obj.data[0]
        width = time_window_obj.data[1]
        
        val = np.mean(frames_obj.data[:, :, start:start+width], axis = 2) # slice end is end+1
        print(f'Cell image from an avaraged frame# {start} to {start+width-1}: Succeeded')
        return ImageData(val)

    def __check_val(self, frames_obj, time_window_obj) -> bool:
        # convert to raw values
        time_window = time_window_obj.data
        # check the value is correct. See TimeWindowVal class.
        frame_length = frames_obj.data.shape[2]
        # check the start and end values
        if time_window[0] < 0:
            raise Exception('The start frame should be 0 or more.')
        if time_window[1] < 1:
            raise Exception('The width should be 1 or more.')
        # compare the val to frame lentgh
        if time_window[0] + time_window[1] > frame_length:
            raise Exception(f"The total frame should be less than {frame_length-1}.")
        else:
            return True

    def reset(self) -> None:
        self.set_controller([0, 1])

    def print_infor(self) -> None:
        if not self.__data_dict:
            print("Data_dict is empty")
            return
        dict_key = list(self.__data_dict.keys())
        if self.__data_dict[dict_key[0]] is None:
            print("No data in the ImageController")
            return
        print("ImageController information ===================")
        print(f"ImageController = {self.__time_window_obj.data}")
        print("-- data_dict LIST -- ")
        for experiments in dict_key:
            key_list = list(self.__data_dict[experiments].keys())
            print(f"{experiments} = {key_list}")
        print("=============== ImageController information END")
            
    @property
    def data_dict(self):
        return self.__data_dict

class TraceController(UserController):
    def __init__(self, get_experiments_method):
        self.get_experiments = get_experiments_method
        self.__time_window_obj = TimeWindowVal(0, 100)
        self.__data_dict = {}  # data dict = {filename:frame_type{ELEC1:ElecData,ELEC2:ElecData,ELEC3:ElecData}}
        self.__mod_list = []
        self.__inf_mode = True  # This is for no limit trace (whole trace)
        
    def __del__(self):  #make a message when this object is deleted.
        #print('.')
        print('----- Deleted a TraceController object.' + '  myId={}'.format(id(self)))
        #pass

        # make a new Roi value object
    def set_controller(self, window_value_list: list):  #value_list = [start, width]
        start = window_value_list[0]
        width = window_value_list[1]

        self.__time_window_obj = TimeWindowVal(start, width)  # replace the roi
        self.set_data()

    def set_data(self):
        # repeat the number of experiments
        for filename_key in list(self.__data_dict.keys()):
            # get Experiments obj Data using a method in DataService
            experiments_entity = self.get_experiments(filename_key)
            # make a image data dict
            new_dict = {}
            for key in experiments_entity.trace_dict.keys():  # key = "ELEC1", "ELEC2", "ELEC3"
                dict_val = self.__trace_culc(experiments_entity.trace_dict[key], self.__time_window_obj)
                new_dict[key] = dict_val
            self.__data_dict[filename_key] = new_dict
        print(f"set TimeController: {self.__time_window_obj.data}")

    def add_experiments(self, filename_str):
        self.__data_dict[filename_str] = None
        self.set_data()
        self.print_infor()
        
    def add_data(self, filename_key, data_key):
        pass
        
    def show_data(self, filename_key, data_key, axis=None):  # axis = MatplotLib axis
        if axis is None:
            self.__data_dict[filename_key][data_key.upper()].show_data()
        else:
            self.__data_dict[filename_key][data_key.upper()].show_data(axis)
            
    # calculate a image from a single frames data with a time window value object
    def __trace_culc(self, trace_obj, time_window_obj):

        start = time_window_obj.data[0]
        width = time_window_obj.data[1]
        if self.__inf_mode is True:
            return trace_obj
        else:
            # check value is correct
            self.__check_val(trace_obj, time_window_obj)
            # make raw trace data
            val = np.mean(trace_obj.data[:, :, start:start+width])
            print(f'Cell image from an avaraged frame# {start} to {start+width-1}: Succeeded')
            return TraceData(val)

    def __check_val(self, trace_obj, time_window_obj) -> bool:
        # convert to raw values
        time_window = time_window_obj.data
        # check the value is correct. See TimeWindowVal class.
        trace_length = trace_obj.data.shape[0]
        # check the start and end values
        if time_window[0] < 0:
            raise Exception('The start frame should be 0 or more.')
        if time_window[1] < 1:
            raise Exception('The width should be 1 or more.')
        # compare the val to frame lentgh
        if time_window[0] + time_window[1] > trace_length:
            raise Exception(f"The total data point should be less than {trace_length-1}.")
        else:
            return True

    def reset(self) -> None:
        self.set_controller([0, 1])

    def print_infor(self) -> None:
        if not self.__data_dict:
            print("Data_dict is empty")
            return
        dict_key = list(self.__data_dict.keys())
        if self.__data_dict[dict_key[0]] is None:
            print("No data in the TraceController")
            return
        print("TraceController information ===================")
        print(f"TraceController = {self.__time_window_obj.data}")
        print("-- data_dict LIST -- ")
        for experiments in dict_key:
            key_list = list(self.__data_dict[experiments].keys())
            print(f"{experiments} = {key_list}")
        print("=============== TraceController information END")
            
    @property
    def data_dict(self):
        return self.__data_dict

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
    
