# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:08:17 2022
concrete classes for data entities
lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import copy


"""
data factory
"""

class DataFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self, data, *args):
        pass


"Frames"
class FullFramesFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data
        return FullFrames(data, *args)


class ChFramesFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data
        return ChFrames(data, *args)


"Image"
class CellImageFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return CellImage(data, *args)


class DifImageFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return DifImage(data, *args)


"Trace"
class FullTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return FullTrace(data, *args)

class ChTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return ChTrace(data, *args)
    
class BGTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return BGTrace(data, *args)
    
class ElecTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = 
        return ElecTrace(data, *args)
    

"""
product
"""
class Data(metaclass=ABCMeta):
    @abstractmethod
    def _read_data(self, data):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def update(self, val):
        pass
    
    @abstractmethod
    def show_data(self):
        pass
    
    @abstractmethod
    def print_infor(self):
        pass



"FluoFrames"
class FluoFrames(Data):  # 3D frames data: full frames, ch image
    def __init__(self, data, interval=0, pixel_size=0, unit=0):  # data = 3D raw data for distingish Chframes
        self.__frames_obj = FramesData()
        self.__interval = copy.deepcopy(interval)  # (ms)
        self.__pixel_size = copy.deepcopy(pixel_size)  # (um)
        self.__unit = copy.deepcopy(unit)  # No unit because of raw camera data.

        self._read_data(data)

    def _read_data(self, data) -> None:
        self.__frames_obj.frames_data = copy.deepcopy(data)  # setter of FramesData
        if len(self.__frames_obj.frames_data) <= 1:  # getter of FramesData
            raise Exception("This object should be 3D data")
    
    def get_data(self) -> object:
        return self.__frames_obj.frames_data, self.__interval, self.__pixel_size, self.__unit

    def update(self):
        pass

    def show_data(self, frame_num=0) -> None:
        image = self.__frames_obj.frames_data
        plt.imshow(image[:, :, frame_num], cmap='gray', interpolation='none')

    def print_infor(self) -> None:
        #np.set_printoptions(threshold=np.inf)  # This is for showing all data values.
        data = self.__frames_obj.frames_data  # getter of FramesData
        print(data)
        print(data.shape)
        print(self.__interval)
        print(self.__pixel_size)
        print(self.__unit)
        #np.set_printoptions(threshold=1000)


class FullFrames(FluoFrames):
    def __init__(self, data, *args):
        super().__init__(data, *args)
        self.object_num = 0  # instance number, It shold be increased by data_set
        print('Made a Fullframes')
        
    def print_name(self):
        print('This is Fullframes' + str(self.object_num))


class ChFrames(FluoFrames):
    def __init__(self, data, *args):
        super().__init__(data, *args)
        self.object_num = 0  # instance number
        print('Made a Chframes')
        
    def print_name(self):
        print('This is Chframes' + str(self.object_num))


"Value Object for frames"
class FramesData():
    def __init__(self):
        self.__frames_data = np.empty((1, 1, 1), dtype=float)
        
    @property
    def frames_data(self):
        return self.__frames_data
    
    @frames_data.setter
    def frames_data(self, val):
        if val.ndim != 3: 
            raise Exception("This object should be numpy 3D data(x, y, t)")
        
        self.__frames_data = val


        
"Fluo Image"
class FluoImage(Data):  # cell image, dif image
    def __init__(self, frames_data, frame_num, pixel_size=0, unit=0):
        self._frames_data = frames_data
        self._image_obj = ImageData()
        self._frame_num = frame_num  # list [start, end]
        self._pixel_size = copy.deepcopy(pixel_size)  # (um)
        self._unit = copy.deepcopy(unit)  # No unit because of raw camera data.

    def _read_data(self, data) -> None:
        pass
    
    def get_data(self) -> object:
        return self._image_obj.image_data, self._pixel_size

    def update(self):
        pass
    
    def show_data(self):
        plt.imshow(self._image_obj.image_data, cmap='gray', interpolation='none')
    
    def print_infor(self):
        #np.set_printoptions(threshold=np.inf)  # This is for showing all data values.
        data = self._image_obj.image_data  # getter of FramesData
        print(data)
        print(data.shape)
        print('The start frame number = ' + str(self._frame_num[0]))
        print('The end frame number = ' + str(self._frame_num[1]))
        print(self._pixel_size)
        print(self._unit)
        #np.set_printoptions(threshold=1000)


class CellImage(FluoImage):
    def __init__(self, frames_data, frame_num=[0,1], *args):  # data = 3D raw data, frame = [list]
        super().__init__(frames_data, frame_num, *args)
        self.object_num = 0  # instance number
        self._read_data(frame_num)
        
    def _read_data(self, frame_num):
        frame_length = self._frames_data.shape[2]
        
        if frame_num[1] > frame_length-1: 
            raise Exception("The end frame should be the same as image size or less.")
            
        start = frame_num[0]
        end = frame_num[1]

        if end - start == 0:
            self._image_obj.image_data = self._frames_data[:, :, frame_num[0]]
            print('Read a single cell image')
        elif end - start > 0: 
            self._image_obj.image_data = np.mean(self._frames_data[:, :, start:end], axis = 2)
            print('Read an avarage cell image')
        else:
            self._image_data = np.zeros((2, 2))
            print('-----------------------------------------------------')
            print('The end frame should be higher than the start frame.')
            print('-----------------------------------------------------')
        
    def update(self, frame_num):  # frame_num = [start, end, start_width, end_width]
        self._read_data(frame_num)
        print('CellImage recieved a notify message.')
            
    def print_name(self):
        print('This is CellImage' + str(self.object_num))
        
        
class DifImage(FluoImage):
    def __init__(self, data):
        super().__init__(data)
        self.object_num = 0  # instance number

    def _read_data(self):
        pass
        
    def update(self):
        pass

    def get_data(self):
        pass
    
    def print_name(self):
        print('This is DifImage' + str(self.object_num))


"Value Object for images"
class ImageData():
    def __init__(self):
        self.__image_data = np.empty((1, 1), dtype=float)
        
    @property
    def image_data(self):
        return self.__image_data
    
    @image_data.setter
    def image_data(self, val):
        if val.ndim != 2: 
            raise Exception("This object should be numpy 2D data(x, y)")
            
        self.__image_data = val




"Fluo Trace"
class FluoTrace(Data):  # Fluo trae, Elec trace
    def __init__(self, data, interval):
        self.__trace_obj = TraceData()
        self.__time_obj = TimeData()
        self.__frames_data = data
        self.__interval = copy.deepcopy(interval)

    def _read_data(self, roi):  # roi[x, y, x_length, y_length]   
        self.__trace_obj.trace_data = self.__fluo_trace_creator(self.__frames_data, roi)
    
    def update(self, roi_obj):
        self._read_data(roi_obj)
        print('FluoTrace recieved a notify message.')
    
    def get_data(self):
        return self.__trace_obj.trace_data, self.__interval
    
    @staticmethod
    def __fluo_trace_creator(frames_data, roi):
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frames_data[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data
        print('Undated ROI = ' + str(roi))
        
    def create_time_data(self):
        num_data_point = self.__interval * np.shape(self.__trace_obj.trace_data)[0]
        self.__time_obj.time_data = np.linspace(self.__interval, 
                                     num_data_point, 
                                     np.shape(self.__trace_obj.trace_data)[0])
    
    def show_data(self):
        plt.plot(self.__time_obj.time_data, self.__trace_obj.trace_data)  
    
    def print_infor(self):
        pass

 
class FullTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a FullTrace')

    def print_name(self):
        print('This is FullTrace' + str(self.object_num))


class ChTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a ChTrace')
        
    def print_name(self):
        print('This is ChTrace' + str(self.object_num))


class BGTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a BGTrace')
        
    def print_name(self):
        print('This is BGTrace' + str(self.object_num))





class ElecTrace(Data):
    def __init__(self, data, interval):
        super().__init__()
        self.object_num = 0  # instance number
        self.__read_data(data, interval)
        print('Made a ElecTrace')

    def _read_data(self, data, interval):
        self.trace_data = copy.deepcopy(data)
        self.interval = copy.deepcopy(interval)
        num_data_point = self.interval * np.shape(self.trace_data)[0]
        self.time_data = np.linspace(self.interval, 
                                     num_data_point, 
                                     np.shape(self.trace_data)[0])
        
        if len(self.trace_data) <= 1:
            print('---------------------')
            print('Can not make Elec data')
            print('---------------------')
            return None
        else:
            print('Read a ElecTrace')

    
    def update(self):
        pass

    def get_data(self):
        pass
    
    def print_name(self):
        print('This is ElecTrace' + str(self.object_num))


"Value Object for traces"
class TraceData():
    def __init__(self):
        self.__trace_data = np.empty((1), dtype=float)
        
    @property
    def trace_data(self):
        return self.__trace_data
    
    @trace_data.setter
    def trace_data(self, val):
        if val.ndim != 1: 
            raise Exception("This object should be numpy 1D data(x)")
            
        self.__trace_data = val
        
class TimeData():
    def __init__(self):
        self.__time_data = np.empty((1), dtype=float)
        
    @property
    def time_data(self):
        return self.__time_data
    
    @time_data.setter
    def time_data(self, val):
        if val.ndim != 1: 
            raise Exception("This object should be numpy 1D data(x)")
            
        self.__time_data = val

if __name__ == '__main__':
    filename = '20408A001.tsm'
    filepath = '..\\220408\\'

