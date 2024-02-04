# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
classes for User controllers
user controllers always have only one experiments, but several chs.
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import TraceData, ImageData
from SCANDATA.model.value_object import RoiVal, TimeWindowVal
from SCANDATA.model.mod.mod_main import ModService
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
    def create_controller(self):
        return Roi()
        
class ImageControllerFactory(UserControllerFactory):
    def create_controller(self):
        return ImageController()
    
class TraceControllerFactory(UserControllerFactory):
    def create_controller(self):
        return TraceController() 
        

"""
abstract product
"""
class UserController(metaclass=ABCMeta):
    def __init__(self):
        self.observer = ControllerObserver()
        self.__mod_service = ModService()
        self._val_obj = None
        self.__mod_switch = False  # This is for test.
        
    def __del__(self):  #make a message when this object is deleted.
        print('.')
        #print('----- Deleted a Roi object.' + '  myId={}'.format(id(self)))
        #pass
        
    @abstractmethod
    def set_controller_val(self, val_list:list):  # e.g. roi value
        raise NotImplementedError()
        
    @abstractmethod
    def _get_val(self, experiments_obj, ch_key):
        raise NotImplementedError()
    
    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError()
        
    # it can receive list or str as ch_key. But usualy it should be a list, becase every data shold be produced by the same controller.
    def set_controller_data(self, experiments_obj, data_key_list):   # get controller values from experiments
        data_dict = {}
        if isinstance(data_key_list, str):
            data = self._get_val(experiments_obj, data_key_list)
            if data is None:
                pass
            else:
                data_dict[data_key_list] = data
        elif isinstance(data_key_list, list):
            for data_key in data_key_list:
                data = self._get_val(experiments_obj, data_key)
                if data is None:
                    pass
                else:
                    data_dict[data_key] = data
        print("Mod service should be here???????????")
        if self.__mod_switch is True:
            # apply mod 
            data_dict = self.__mod_service.apply_mod(data_dict)
        return data_dict

    def set_observer(self, observer):
        self.observer.set_observer(observer)

    def set_mod_key(self, mod_key):
        if self.__mod_switch is True:
            self.__mod_service.set_mod_key(mod_key)
        else:
            pass
        
    def set_mod_val(self, mod_key, val):
        if self.__mod_switch is True:
            self.__mod_service.set_mod_val(mod_key, val)
        else:
            pass
    
    @abstractmethod
    def reset(self):
        raise NotImplementedError()
    
    @property
    def val_obj(self):
        return self._val_obj


"""
concrete product
"""
class Roi(UserController):
    def __init__(self):
        super().__init__()
        self._val_obj = RoiVal(40, 40, 1, 1)
        
    # make a new Roi value object
    def set_controller_val(self, roi_val: list):
        if None not in roi_val:
            pass
        else:
            for i in range(2):  # for x and y
                if roi_val[i] == None:
                    roi_val[i] = self._val_obj.data[i]
            for i in range(2, 4):
                if roi_val[i] == None:
                    roi_val[i] = self._val_obj.data[i]# for width and hight
                else:
                    roi_val[i] = self._val_obj.data[i] + roi_val[i]
        self._val_obj = RoiVal(*roi_val[:4])  # replace the roi
        print(f"set ROI: {self._val_obj.data}")

    # calculate a trace from a single frames data with a roi value object
    def _get_val(self, experiments_obj, ch_key):
        if "CH" not in ch_key:
            pass
        else:
            frames_obj = experiments_obj.frames_dict[ch_key]
            if frames_obj is None:
                raise Exception(f'The controller can not find the key:{ch_key} in experiments entity {experiments_obj}.')
            roi_obj = self._val_obj
            # check value is correct
            self.__check_val(frames_obj, roi_obj)
            # make raw trace data       
            x, y, x_width, y_width = roi_obj.data[:4]
        
            mean_data = np.mean(frames_obj.data[x:x+x_width, y:y+y_width, :], axis = (0, 1)) #slice end doesn't include to slice
            # make a trace value object
            print(f"{ch_key}: ROI trace with {roi_obj.data}: Succeeded")
            return TraceData(mean_data, frames_obj.interval)
        
    def __check_val(self, frames_obj, roi_obj) -> bool:
        # convert to raw values
        roi = roi_obj.data
        # check the value is correct. See RoiVal class.
        frames_size = frames_obj.shape
        if roi[0] + roi[2]-1 > frames_size[0] or roi[1] + roi[3] -1> frames_size[1]:  #width is always 1 or more.
            raise Exception("The roi size should be the same as the image size or less")
        if roi[0] < 0 or roi[1] < 0: 
            raise Exception("The roi should be the same as 0 or more")
        if roi[2] < 1 or roi[3] < 1: 
            raise Exception("The roi width should be the same as 1 or more")
        else:
            return True
    
    def reset(self) -> None:
        self.set_controller_val([40, 40, 1, 1])
        
class ImageController(UserController):
    def __init__(self):
        super().__init__()
        self._val_obj = TimeWindowVal(0, 1)
        
    def __del__(self):  #make a message when this object is deleted.
        print('.')
        #print('----- Deleted a ImageCOntroller object.' + '  myId={}'.format(id(self)))
        #pass

        # make a new Roi value object
    def set_controller_val(self, window_value_list: list):  #value_list = [start, width]
        start = window_value_list[0]
        width = window_value_list[1]
        self._val_obj = TimeWindowVal(start, width)  # replace the roi
        print(f"set ImageController: {self._val_obj.data}")

    # calculate a image from a single frames data with a timewindow value object
    def _get_val(self, experiments_obj, ch_key):
        if "CH" not in ch_key:
            pass
        else:
            frames_obj = experiments_obj.frames_dict[ch_key]
            time_window_obj = self._val_obj
            # check value is correct
            self.__check_val(frames_obj, time_window_obj)
            # make raw trace data
            start = time_window_obj.data[0]
            width = time_window_obj.data[1]
        
            val = np.mean(frames_obj.data[:, :, start:start+width], axis = 2) # slice end is end+1
            print(f"{ch_key}: An avarage Cell image from frame# {start} to {start+width-1}: Succeeded")
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
        self.set_controller_val([0, 1])


class TraceController(UserController):
    def __init__(self):
        super().__init__()
        self._val_obj = TimeWindowVal(0, 100)
        self.__inf_mode = True  # This is for no limit trace (whole trace)
        
    def __del__(self):  #make a message when this object is deleted.
        print('.')
        #print('----- Deleted a TraceController object.' + '  myId={}'.format(id(self)))
        #pass

        # make a new Roi value object
    def set_controller_val(self, window_value_list: list):  #value_list = [start, width]
        start = window_value_list[0]
        width = window_value_list[1]
        self._val_obj = TimeWindowVal(start, width)  # replace the roi
        print(f"set TimeController: {self._val_obj.data}")

    # calculate a trace from a single trace data in experiments dict with a time window value object
    def _get_val(self, experiments_obj, ch_key):
        if "ELEC" not in ch_key:
            pass
        else:
            trace_obj = experiments_obj.trace_dict[ch_key]
            time_window_obj = self._val_obj
            start = time_window_obj.data[0]
            width = time_window_obj.data[1]
            if self.__inf_mode is True:
                return trace_obj
            else:
                # check value is correct
                self.__check_val(trace_obj, time_window_obj)
                # make raw trace data
                val = trace_obj.data[start:start+width]
                print(f"Made a new trace from {start} to {start+width-1}: Succeeded")
                interval = trace_obj.interval
                return TraceData(val, interval)

    def __check_val(self, trace_obj, time_window_obj) -> bool:
        # convert to raw values
        time_window = time_window_obj.data
        # check the value is correct. See TimeWindowVal class.
        trace_length = trace_obj.data.shape[0]
        # check the start and end values
        if time_window[0] < 0:
            raise Exception('The start trace should be 0 or more.')
        if time_window[1] < 1:
            raise Exception('The width should be 1 or more.')
        # compare the val to trace lentgh
        if time_window[0] + time_window[1] > trace_length:
            raise Exception(f"The total data point should be less than {trace_length-1}.")
        else:
            return True

    def reset(self) -> None:
        self.set_controller_val([0, 1])
    
        
class ControllerObserver:
    def __init__(self):
        self._observers = []
        
    def set_observer(self, observer):
        for check_observer in self._observers:
            if check_observer == observer:
                self._observers.remove(observer)
                print(f"Observer removed {observer.__class__.__name__}")
                return
        self._observers.append(observer)   
        print(f"Observer added {observer.__class__.__name__} to a user controller")
            
    def notify_observer(self):
        for observer_name in self._observers:
            observer_name.update()
        #print("Update Notification from Roi")

    @property
    def observers(self) -> list:
        return self._observers

