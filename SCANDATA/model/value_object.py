# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 10:04:06 2023

@author: lulul
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import inspect



"""
Value object factory
"""
"""

class ValueObjectFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_value_object(self, val):
        raise NotImplementedError()


class FilenameFactory(ValueObjectFactory):
    def create_value_object(self, val):
        return Filename(val)
        
class Value_object(metaclass=ABCMeta):
    @abstractmethod
    def show_data(self, val):
        raise NotImplementedError()
"""
        
"""
Value object
"""
class Filename:
    def __init__(self, fullname: str):
        self.__fullname = os.path.join(fullname)   # replace separater for each OS
        self.__filename = os.path.basename(self.__fullname)
        self.__filepath = os.path.dirname(self.__fullname) + os.sep
        self.__abspath = os.path.abspath(self.__fullname)# absolute path
        self.__extension = os.path.splitext(self.__fullname)[1]  # get only extension

    def __del__(self):
        #print('.')
        #print('Deleted a ImageData object.' + '  myId= {}'.format(id(self)))
        pass
        
    @property
    def fullname(self) -> str:
        return self.__fullname
    
    @property
    def name(self) -> str:
        return self.__filename
    
    @property
    def path(self) -> str:
        return self.__filepath
    
    @property
    def abspath(self) -> str:
        return self.__abspath
    
    @property
    def extension(self) -> str:
        return self.__extension
"""
"Value object for Data
"""
class FramesData:
    def __init__(self, val: np.ndarray):
        if val.ndim != 3: 
            raise Exception('The argument of FrameData should be numpy 3D data(x, y, t)')
        size = val.shape
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = val
        self.__frames_size = size
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a FramesData' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        #print('.')
        #print('Deleted a FramesData object.' + '  myId= {}'.format(id(self)))
        pass
    
    # This is for background substruction
    def __sub__(self):
        raise NotImplementedError()
    
    @property
    def data(self) -> np.ndarray:
        return self.__data
    
    @data.setter
    def data(self, val):
        raise Exception('FrameData is a value object (Immutable).')
        
    @property
    def frame_size(self) -> int:
        return self.__frame_size
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    def show_data(self, frame_num=0, plt=plt) -> object:  # plt shold be an axis in a view class object = AxisImage
        return plt.imshow(self.__data[:, :, frame_num], cmap='gray', interpolation='none')
    
    
class ImageData:
    def __init__(self, val: np.ndarray):
        if val.ndim != 2: 
            raise Exception('The argument of ImageData should be numpy 2D data(x, y)')
        size = val.shape
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = val
        self.__image_size = size
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a ImageData' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        #print('.')
        #print('Deleted a ImageData object.' + '  myId= {}'.format(id(self)))
        pass
        
    # This is for difference image
    def __sub__(self):
        raise NotImplementedError()
        
    @property
    def data(self) -> np.ndarray:
        return self.__data
    
    @data.setter
    def data(self, val):
        raise Exception('ImageData is a value object (Immutable).')
        
    @property
    def image_size(self) -> int:
        return self.__image_size
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    def show_data(self, plt=plt) -> object:    # plt shold be an axis in a view class object = AxisImage
        return plt.imshow(self.__data, cmap='gray', interpolation='none')
    
    
class TraceData:
    def __init__(self, val: np.ndarray, interval) -> None:
        if val.ndim != 1: 
            raise Exception('The argument of TraceData should be numpy 1D data(x)')
        if  val.shape[0] < 5: 
            print('------------------------------------------------------------------------')
            print('This data length is ' + str(val))
            print('Warning!!! The number of the data points of TraceData is less than 5 !!!')
            print('It makes a bug during dF over calculation !!!')
            print('------------------------------------------------------------------------')

        length = val.shape[0]
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = val
        self.__time = self.__create_time_data(val, interval)
        self.__interval = interval
        self.__length = length
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a TraceData' + '  myId= {}'.format(id(self)))

    def __del__(self):
        #print('.')
        #print('Deleted a TraceData object.' + '  myId= {}'.format(id(self)))
        pass
        
    # This is for background substruction
    def __sub__(self, other: object) -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong trace data')
        F = self.__data[0: 5]
        mean_F = np.mean(F, axis = 0)
        delta_F_trace = self.__data - other.data
        bg_comp_trace = delta_F_trace + mean_F
        return TraceData(bg_comp_trace, self.__interval)

        
        
        
    def __create_time_data(self, trace, interval) -> np.ndarray:
        num_data_point = interval * np.shape(trace)[0]
        time_val = np.linspace(interval, num_data_point, np.shape(trace)[0])
        return time_val
        
    @property
    def data(self) -> np.ndarray:
        return self.__data
    
    @data.setter
    def data(self, val):
        raise Exception('TraceData is a value object (Immutable).')
        
    @property
    def time(self) -> np.ndarray:
        return self.__time
    
    @time.setter
    def time(self, val):
        raise Exception('TimeData is a value object (Immutable).')
            
    @property
    def length(self) -> int:
        return self.__length
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    @property
    def interval(self) -> float:
        return self.__interval
    
    def check_length(self, data: object) -> bool:
        return bool(self.__length == data.length)
    
    def show_data(self, plt=plt) -> list:  # plt shold be an axis in a view class object = [matplotlib.lines.Line2D]
        return plt.plot(self.__time, self.__data) 

    
"""
Value object for controller
"""
class RoiVal:
    def __init__(self, x: int, y: int, x_width: int, y_width: int):         

        if x < 0 or y < 0 or x_width < -1 or y_width < -1:  # width -1 is for small ROI subtraction
            raise Exception('ROI values should be 0 or more')
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = np.array([x, y, x_width, y_width])
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a RoiVal' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        #print('.')
        #print('Deleted a RoiVal object.' + '  myId={}'.format(id(self)))
        pass
        
    #override for "+"
    def __add__(self, other: object)  -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong data! Only RoiVal can be added!')
        "Tip Need refactroing. This should be new roi value object."
        new_val = self.__data + other.data
        new_obj = RoiVal(*new_val)
        new_obj.data_type = self.__data_type
        return new_obj
        
    @property
    def data(self) -> list:
        return self.__data
    
    @data.setter
    def data(self, x, y, x_width=1, y_width=1):  
        raise Exception('RoiVal is a value object (Immutable).')
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    @data_type.setter
    def data_type(self, data_type) -> None:  
        self.__data_type = data_type
    
    

class FrameWindowVal:
    def __init__(self, start: int, end: int, start_width: int, end_width: int):
        if start > end: 
            raise Exception('FrameWindow the end values should be the same or larger than the start value')

        if start_width < 0 or end_width < 0:
            raise Exception('FrameWindow width values should be 0 or more')
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = np.array([start, end, start_width, end_width])  # frame number ex.[10, 50, 5, 5]
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a FrameWindowVal' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        #print('.')
        #print('Deleted a FrameWindowVal object.' + '  myId={}'.format(id(self)))
        pass
        
    #override for "+"
    def __add__(self, other: object) -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong FrameWindowVal data')
        self.__data += other.data
        return self
        
    @property
    def data(self) -> list:
        return self.__data
    
    @data.setter
    def data(self, start, end, start_width=1, end_width=1):  
        raise Exception('FrameWindowVal is a value object (Immutable).')
    
    @property
    def data_type(self) -> str:
        return self.__data_type


class TimeWindowVal:
    def __init__(self, start: float = 0, end: float = 100):
        if start > end: 
            raise Exception('TimeWindow the end values should be the same or larger than the start value')

        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = np.array([start, end])  # time (ms)  ex.[0, 100]
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a TimeWindowVal' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        #print('.')
        #print('Deleted a FrameWindowVal object.' + '  myId={}'.format(id(self)))
        pass
        
    #override for "+"
    def __add__(self, other: object) -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong TimeWindowVal data')
        self.__data += other.data
        return self
        
    @property
    def data(self) -> list:
        return self.__data
    
    @data.setter
    def data(self, start, end, start_width=1, end_width=1):  
        raise Exception('TimeWindowVal is a value object (Immutable).')
    
    @property
    def data_type(self) -> str:
        return self.__data_type