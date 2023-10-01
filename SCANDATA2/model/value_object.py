# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 10:04:06 2023

@author: lunelukkio@gmail.com
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import inspect
import glob

        
"""
Value object
"""
class WholeFilename:  # Use it only in a view and controller
    def __init__(self, fullname: str):
        self.__fullname = os.path.join(fullname)  # replace separater for each OS
        self.__filename = os.path.basename(self.__fullname)
        self.__filepath = os.path.dirname(self.__fullname) + os.sep
        self.__abspath = os.path.abspath(fullname)# absolute path
        split_filename = os.path.splitext(self.__filename)
        self.__file_name_no_ext = split_filename[0]
        self.__extension =  split_filename[1]  # get only extension
        
        self.__filename_list = self.__make_filename_list()
        
    
    # List need A000-Z999 in the last of filenames
    def __make_filename_list(self) -> list:
        find = '*' + str(self.__extension)
        fullname_list = glob.glob(find)
        filename_list = []
        for i in range(len(fullname_list)):
            filename_list.append(os.path.basename(fullname_list[i]))
        return  filename_list
    

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
    def file_name_no_ext(self) -> str:
        return self.__file_name_no_ext
    
    @property
    def extension(self) -> str:
        return self.__extension
    
    @property
    def filename_list(self) -> list:
        return self.__filename_list
    
    def print_infor(self) -> None:
        print('THe absolute path = ' + self.__abspath)
        print('The full path = ' + self.__fullname)
        print('The file name = ' + self.__filename)
        print('The file path = ' + self.__filepath)
        print('The file name without extension = ' + self.__file_name_no_ext)
        print('The file extension = ' + self.__extension)
        print('The file name list in the same folder = ' + str(self.__filename_list))
        
        
"""
"Value object for Data
"""
class FramesData:
    def __init__(self, val: np.ndarray, interval = 0, pixel_size = [0, 0]):  # need *args, **kwargs for constracting
        if val.ndim != 3: 
            raise Exception('The argument of FrameData should be numpy 3D data(x, y, t)')
        self.__data = val
        self.__shape = val.shape  # the number of pixels and frames [pixel, pixel, frame]
        self.__interval = interval  # frame interval (ms)
        self.__pixel_size = pixel_size  #actual length (um)
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
    def interval(self):
        return self.__interval
        
    @property
    def shape(self) -> int:
        return self.__shape
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    def show_data(self, frame_num=0, plt=plt) -> object:  # plt shold be an axis in a view class object = AxisImage
        return plt.imshow(self.__data[:, :, frame_num], cmap='gray', interpolation='none')
    
    
class ImageData:
    def __init__(self, val: np.ndarray, pixel_size = [0, 0]):  # need *args, **kwargs for constracting
        if val.ndim != 2: 
            raise Exception('The argument of ImageData should be numpy 2D data(x, y)')
        self.__data = val
        self.__shape = val.shape  # the number of pixels
        self.__pixel_size = pixel_size
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
    def shape(self) -> int:
        return self.__shape
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    def show_data(self, plt=plt) -> object:    # plt shold be an axis in a view class object = AxisImage
        return plt.imshow(self.__data, cmap='gray', interpolation='none')
    
    
class TraceData:
    def __init__(self, val: np.ndarray, interval) -> None:  #  needs 2 variables
        if val.ndim != 1: 
            raise Exception('The argument of TraceData should be numpy 1D data(x)')
        if  val.shape[0] < 5: 
            print('------------------------------------------------------------------------')
            print('This data length is ' + str(val))
            print('Warning!!! The number of the data points of TraceData is less than 5 !!!')
            print('It makes a bug during dF over calculation !!!')
            print('------------------------------------------------------------------------')

        self.__data = val
        self.__time = self.__create_time_data(val, interval)
        self.__length = val.shape[0]  # the number of data points
        self.__interval = interval  # data interval
        #print(self.__data_type + ' made a TraceData' + '  myId= {}'.format(id(self)))

    def __del__(self):
        #print('.')
        #print('Deleted a TraceData object.' + '  myId= {}'.format(id(self)))
        pass
    
    def __add__(self, sum_val) -> object:
        if type(sum_val) == float or \
           type(sum_val) == int or \
           type(sum_val) == np.int64 or \
           type(sum_val) == np.float64:
            sub_trace = self.__data + sum_val
        elif self.__data_type == sum_val.data_type:
            if len(self.__data) != len(sum_val.data):
                print('!!! Caution! The length of these data is not matched!')
            sub_trace = np.sum(self.__data, sum_val.data)
        else:
            raise Exception('Wrong value. This value object should be dvided by int or float or other value object')
        return TraceData(sub_trace, self.__interval)
        
    def __sub__(self, sub_val) -> object:
        if type(sub_val) == float or \
           type(sub_val) == int or \
           type(sub_val) == np.int64 or \
           type(sub_val) == np.float64:
            sub_trace = self.__data - sub_val
        elif self.__data_type == sub_val.data_type:
            if len(self.__data) != len(sub_val.data):
                print('!!! Caution! The length of these data is not matched!')
            sub_trace = np.subtract(self.__data, sub_val.data)
        else:
            raise Exception('Wrong value. This value object should be dvided by int or float or other value object')
            
        return TraceData(sub_trace, self.__interval)
        
    def __truediv__(self, div_val) -> object:
        if type(div_val) != float and \
           type(div_val) != int and \
           type(div_val) != np.int64 and \
           type(div_val) != np.float64:
            raise Exception('Wrong value. This value object should be dvided by int or float')
        div_trace = self.__data/div_val
        return TraceData(div_trace, self.__interval)
    
    def __mul__(self, mul_val) -> object:
        if type(mul_val) != float and \
           type(mul_val) != int and \
           type(mul_val) != np.int64 and \
           type(mul_val) != np.float64:
            raise Exception('Wrong value. This value object should be dvided by int or float')
        mul_trace = self.__data * mul_val
        return TraceData(mul_trace, self.__interval)
        
        
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
        return plt.plot(self.__time, self.__data ,linewidth=0.7) 

    

"""
Value object for controller
"""
class RoiVal:  # Shold be called by the same class for __add__ and __sub__
    def __init__(self, x: int, y: int, x_width: int, y_width: int):         
        if x < 0 or y < 0 :  # np.mean slice doesn't inculed end value. so width shold be 1 or more than 1
            raise Exception('ROI x and y values should be 0 or more')
        if x_width < 1 or y_width < 1:
            raise Exception('ROI width values should be 1 or more')
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = np.array([x, y, x_width, y_width])  # self.__data should be np.array data.
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
        new_val = self.__data + other.data
        new_obj = RoiVal(*new_val)
        new_obj.data_type = self.__data_type
        return new_obj
    
    def __sub__(self, other: object)  -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong data! Only RoiVal can be added!')
        new_val = self.__data - other.data
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
    
    

class TimeWindowVal:  # Shold be called by the same class for __add__ and __sub__
    # be careful about end_width. np.mean slice a value not include end.
    def __init__(self, start: int, width=1):
        if start < 0:
            raise Exception('TimeWindow start values should be 0 or more')
        if width < 1:
            raise Exception('FrameWindow width values should be 1 or more')
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__data = np.array([start, width])
        self.__data_type = called_class.__class__.__name__
        #print(self.__data_type + ' made a TimeWindowVal' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        #print('.')
        #print('Deleted a TimeWindowVal object.' + '  myId={}'.format(id(self)))
        pass
        
    #override for "+"
    def __add__(self, other: object) -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong data! Only TimeWindowVal can be added!')
        self.__data += other.data
        return self
    
    def __sub__(self, other: object)  -> object:
        if self.__data_type != other.data_type:
            raise Exception('Wrong data! Only TimeWindowVal can be subtructed!')
        new_val = self.__data - other.data
        new_obj = TimeWindowVal(new_val)
        new_obj.data_type = self.__data_type
        return new_obj
        
    @property
    def data(self) -> list:
        return self.__data
    
    @data.setter
    def data(self, start, width=1):  
        raise Exception('TimeWindowVal is a value object (Immutable).')
    
    @property
    def data_type(self) -> str:
        return self.__data_type
