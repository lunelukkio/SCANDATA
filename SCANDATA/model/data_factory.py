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
import inspect


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
    
class BGFullTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return BGFullTrace(data, *args)
    
class BGChTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = frames object
        return BGChTrace(data, *args)
    
class CameraSyncElecTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = 
        return CameraSyncElecTrace(data, *args)
    

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
        val = np.empty((1, 1, 1), dtype=float)
        self.__frames_obj = FramesData(val)  # Initialised
        self.__interval = copy.deepcopy(interval)  # (ms)
        self.__pixel_size = copy.deepcopy(pixel_size)  # (um)
        self.__unit = copy.deepcopy(unit)  # No unit because of raw camera data.

        self._read_data(data)

    def _read_data(self, data) -> None:
        if len(data) <= 1:  # getter of FramesData
            raise Exception("This x or y size is too small for FluoFrames")
            
        if len(data.shape) == 3:
            self.__frames_obj = FramesData(copy.deepcopy(data))
        elif len(data.shape) == 4:
            raise Exception("It might have more than 1 ch in the data. Use [:,:,:,ch]")
        else:
            raise Exception("The data for FluoFrames is not 3D data")

    def update(self):
        pass
    
    def get_data(self) -> object:
        return self.__frames_obj.frames_data, self.__interval, self.__pixel_size, self.__unit

    def show_data(self, frame_num=0) -> None:
        image = self.__frames_obj.frames_data
        plt.imshow(image[:, :, frame_num], cmap='gray', interpolation='none')

    def print_infor(self):
        pass
    
    def print_additional_infor(self):
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
        
    def print_infor(self) -> None:
        print('This is Fullframes' + str(self.object_num))
        super().print_additional_infor()



class ChFrames(FluoFrames):
    def __init__(self, data, *args):
        super().__init__(data, *args)
        self.object_num = 0  # instance number
        
    def print_infor(self) -> None:
        print('This is Chframes' + str(self.object_num))
        #np.set_printoptions(threshold=np.inf)  # This is for showing all data values.
        super().print_additional_infor()


"Value Object for frames"       
class FramesData():
    def __init__(self, val: np.ndarray):
        if val.ndim != 3: 
            raise Exception("The argument of FrameData should be numpy 3D data(x, y, t)")
        size = val.shape
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__frames_data = val
        self.__frames_size = size
        self.__data_type = called_class.__class__.__name__
        print(self.__data_type + ' made a FramesData' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        print('.')
        #print('Deleted a FramesData object.' + '  myId= {}'.format(id(self)))
    
    @property
    def frames_data(self) -> np.ndarray:
        return self.__frames_data
    
    @frames_data.setter
    def frames_data(self, val):
        raise Exception("FrameData is a value object (Immutable).")
        
    @property
    def frame_size(self) -> int:
        return self.__frame_size
    
    @property
    def data_type(self) -> str:
        return self.__data_type


        
"Fluo Image"
class FluoImage(Data):  # cell image, dif image
    def __init__(self, frames_data, frame_num, pixel_size=0, unit=0):
        val = np.empty((1, 1), dtype=float)
        self._image_obj = ImageData(val)
        self._frames_data = frames_data
        self._frame_num = frame_num  # list [start, end]
        self._pixel_size = copy.deepcopy(pixel_size)  # (um)
        self._unit = copy.deepcopy(unit)  # No unit because of raw camera data.

    def _read_data(self, data) -> None:
        pass

    def update(self):
        pass
    
    def get_data(self) -> object:
        return self._image_obj.image_data, self._pixel_size
    
    def show_data(self) -> None:
        plt.imshow(self._image_obj.image_data, cmap='gray', interpolation='none')
    
    def print_infor(self) -> None:
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

    def _read_data(self, frame_num) -> None:
        frame_length = self._frames_data.shape[2]
        if frame_num[0] > frame_length-1 or frame_num[1] > frame_length-1: 
            raise Exception('The end frame should be the same as the frames length or less.')
            
        start = frame_num[0]
        end = frame_num[1]

        if end - start == 0:
            val = self._frames_data[:, :, frame_num[0]]
            self._image_obj = ImageData(val)
            #print('Read a single cell image')
        elif end - start > 0: 
            val = np.mean(self._frames_data[:, :, start:end], axis = 2)
            self._image_obj = ImageData(val)
            #print('Read an avarage cell image')
        else:
            self._image_data = np.zeros((2, 2))
            raise Exception('The end frame should be higher than the start frame.')
        
    def update(self, frame_num) -> None:  # frame_num = [start, end, start_width, end_width]
        self._read_data(frame_num)
        print('CellImage-{} recieved a notify message.'.format(self.object_num))
            
    def print_name(self) -> None:
        print('This is CellImage-{}'.format(self.object_num))
        
        
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
        print('This is DifImage-{}'.format(self.object_num))


"Value Object for images"
class ImageData():
    def __init__(self, val: np.ndarray):
        if val.ndim != 2: 
            raise Exception("The argument of ImageData should be numpy 2D data(x, y)")
        size = val.shape
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__image_data = val
        self.__image_size = size
        self.__data_type = called_class.__class__.__name__
        print(self.__data_type + ' made a ImageData' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        print('.')
        #print('Deleted a ImageData object.' + '  myId= {}'.format(id(self)))
        
    @property
    def image_data(self) -> np.ndarray:
        return self.__image_data
    
    @image_data.setter
    def image_data(self, val):
        raise Exception("ImageData is a value object (Immutable).")
        
    @property
    def image_size(self) -> int:
        return self.__image_size
    
    @property
    def data_type(self) -> str:
        return self.__data_type
            


"Fluo Trace"
class FluoTrace(Data):  # Fluo trae, Elec trace
    def __init__(self, data, interval):
        val = np.empty((1), dtype=float)
        self.__trace_obj = TraceData(val)
        self.__time_obj = TimeData(val)
        self.__frames_data = data
        self.__interval = copy.deepcopy(interval)

    def _read_data(self, roi: list) -> None:  # roi[x, y, x_length, y_length]
        x_size = self.__frames_data.shape[0]
        y_size = self.__frames_data.shape[1]

        if roi[0] + roi[2] > x_size - 1 or roi[1] + roi[3] > y_size - 1: 
            raise Exception("The roi size should be the same as the image size or less")
            
        if roi[0] < 0 or roi[1] < 0: 
            raise Exception("The roi should be the same as 0 or more")

        trace_val = self.__create_fluo_trace(self.__frames_data, roi)
        self.__trace_obj = TraceData(trace_val)
        time_val = self.__create_time_data(trace_val, self.__interval)
        self.__time_obj = TimeData(time_val)
        
        if self.__trace_obj.check_length(self.__time_obj) == False:
            raise Exception("The trace and time is not the same length")
    
    def update(self, roi_obj) -> None:
        pass
    
    def get_data(self) -> tuple:
        return self.__trace_obj.trace_data, self.__interval
    
    @staticmethod
    def __create_fluo_trace(frames_data, roi) -> np.ndarray:
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frames_data[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data
        print('Updated ROI = ' + str(roi))
        
    def __create_time_data(self, trace, interval) -> np.ndarray:
        num_data_point = interval * np.shape(trace)[0]
        time_val = np.linspace(interval, num_data_point, np.shape(trace)[0])
        return time_val
    
    def show_data(self) -> None:
        plt.plot(self.__time_obj.time_data, self.__trace_obj.trace_data)  
    
    def print_infor(self):
        pass

 
class FullTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number

    def update(self, roi_obj) -> None:
        super()._read_data(roi_obj)
        print('FullTrace-{} recieved a notify message.'.format(self.object_num))
        
    def print_infor(self) -> None:
        print('This is FullTrace-{}'.format(self.object_num))


class ChTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        
    def update(self, roi_obj) -> None:
        super()._read_data(roi_obj)
        print('ChTrace-{} recieved a notify message.'.format(self.object_num))
        
    def print_infor(self) -> None:
        print('This is ChTrace-{}'.format(self.object_num))


class BGFullTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        
    def print_name(self) -> None:
        print('This is BGTrace-{}'.format(self.object_num))
        
        
class BGChTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        
    def print_name(self) -> None:
        print('This is BGTrace-{}'.format(self.object_num))


"Elec trace"
class ElecTrace(Data):  # Fluo trae, Elec trace
    def __init__(self, interval):
        val = np.empty((1), dtype=float)
        self._trace_obj = TraceData(val)
        self._time_obj = TimeData(val)
        self._interval = copy.deepcopy(interval)
        
    def _read_data(self):
        pass
    
    def update(self, roi_obj) -> None:
        pass
    
    def get_data(self) -> tuple:
        return self._trace_obj.trace_data, self._interval
    
    def show_data(self) -> None:
        plt.plot(self._time_obj.time_data, self._trace_obj.trace_data)  
    
    def print_infor(self):
        pass
        
class CameraSyncElecTrace(ElecTrace):
    def __init__(self, data, interval):
        super().__init__(interval)
        self.object_num = 0  # instance number
        self._read_data(data)

    def _read_data(self, data: np.ndarray) -> None:
        self._trace_obj = TraceData(copy.deepcopy(data))

        num_data_point = self._interval * np.shape(data)[0]
        time_val = np.linspace(self._interval, 
                                     num_data_point, 
                                     np.shape(data)[0])
        self._time_obj = TimeData(time_val)
        
        if len(self._trace_obj.trace_data) <= 1:
            print('---------------------')
            print('Can not make Elec data')
            print('---------------------')
            return None
        else:
            print('Read a ElecTrace')
    
    def print_infor(self):
        print('This is ElecTrace' + str(self.object_num))
        
class LongElecTrace(ElecTrace):
    pass


"Value Object for traces"
class TraceData():
    def __init__(self, val: np.ndarray):
        if val.ndim != 1: 
            raise Exception("The argument of TraceData should be numpy 1D data(x)")
        length = val.shape[0]
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__trace_data = val
        self.__length = length
        self.__data_type = called_class.__class__.__name__
        print(self.__data_type + ' made a TraceData' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        print('.')
        #print('Deleted a TraceData object.' + '  myId= {}'.format(id(self)))
        
    @property
    def trace_data(self) -> np.ndarray:
        return self.__trace_data
    
    @trace_data.setter
    def trace_data(self, val):
        raise Exception("TraceData is a value object (Immutable).")
            
    @property
    def length(self) -> int:
        return self.__length
    
    @property
    def data_type(self) -> str:
        return self.__data_type
    
    def check_length(self, data: object) -> bool:
        return bool(self.__length == data.length)
    
        
class TimeData():
    def __init__(self, val: np.ndarray):
        if val.ndim != 1: 
            raise Exception("The argument of TImeData should be numpy 1D data(x)")
        length = val.shape[0]
        called_class = inspect.stack()[1].frame.f_locals['self']
        self.__time_data = val
        self.__length = length
        self.__data_type = called_class.__class__.__name__
        print(self.__data_type + ' made a TimeData' + '  myId= {}'.format(id(self)))
        
    def __del__(self):
        print('.')
        #print('Deleted a TimeData object.' + '  myId= {}'.format(id(self)))
        
    @property
    def time_data(self) -> np.ndarray:
        return self.__time_data
    
    @time_data.setter
    def time_data(self, val):
        raise Exception("TimeData is a value object (Immutable).")
        
    @property
    def length(self) -> int:
        return self.__length
        
    @property
    def data_type(self) -> str:
        return self.__data_type
            
    def check_length(self, data: object) -> bool:
        return bool(self.__length == object.length)


if __name__ == '__main__':
    pass

