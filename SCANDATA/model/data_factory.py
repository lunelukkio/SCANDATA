# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:08:17 2022
concrete classes for data entities
lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import ImageData, TraceData
import numpy as np


"""
data factory
"""

class DataFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self, data, *args):
        raise NotImplementedError()


"Frames"
class FullFramesFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data. *args is for interval, pixel_size, unit
        return FullFrames(data, *args)


class ChFramesFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data. *args is for interval, pixel_size, unit
        return ChFrames(data, *args)


"Image"
class CellImageFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data, frame = [list]
        return CellImage(data, *args)


class DifImageFactory(DataFactory):
    def create_data(self, data, *args):  
        return DifImage(data, *args)


"Trace"
class FullTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data, interval
        return FullTrace(data, *args)


class ChTraceFactory(DataFactory):
    def create_data(self, data, *args):  # data = 3D raw data, interval
        return ChTrace(data, *args)
    
    
class ChElecTraceFactory(DataFactory):  # data = 3D raw data, interval
    def create_data(self, data, *args):  # data = 
        return ChElecTrace(data, *args)
    

"""
product
"""
class Data(metaclass=ABCMeta):
    @abstractmethod
    def _read_data(self, data):
        raise NotImplementedError()
    
    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
    
    @abstractmethod
    def get_infor(self):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, val):
        raise NotImplementedError()
    
    @abstractmethod
    def show_data(self):
        raise NotImplementedError()
    
    @abstractmethod
    def print_infor(self):
        pass



"FluoFrames"
class FluoFrames(Data):  # 3D frames data: full frames, ch image
    def __init__(self, frames_obj, interval=0, pixel_size=0, unit=0):  # frames_obj = value object
        #self.__frames_obj  # create in _read_data
        self.__interval = interval  # (ms)
        self.__pixel_size = pixel_size  # (um)
        self.__unit = unit  # No unit because of raw camera data.

        self._read_data(frames_obj)

    def _read_data(self, frames_obj) -> None:
        if len(frames_obj.data) <= 1:  # getter of FramesData
            raise Exception("This x or y size is too small for FluoFrames")
        if len(frames_obj.data.shape) == 3:
            self.__frames_obj = frames_obj
        elif len(frames_obj.data.shape) == 4:
            raise Exception("It might have more than 1 ch in the data. Use [:,:,:,ch]")
        else:
            raise Exception("The data for FluoFrames is not 3D data")

    def update(self):
        pass
    
    def get_data(self) -> object:  # -> vaqlue object
        return self.frames_obj
    
    def get_infor(self) -> tuple:
        return self.__interval, self.__pixel_size, self.__unit
  
    @property
    def frames_obj(self):
        return self.__frames_obj
  
    @property
    def interval(self):
        return self.__interval

    def show_data(self, frame_num=0) -> None:
        self.__frames_obj.show_data(frame_num)

    def print_infor(self):
        pass
    
    def print_additional_infor(self):
        #np.set_printoptions(threshold=np.inf)  # This is for showing all data values.
        print(self.__frames_obj.data)
        print(self.__frames_obj.data.shape)
        print(self.__interval)
        #print(self.__pixel_size)
        #print(self.__unit)
        #np.set_printoptions(threshold=1000)


class FullFrames(FluoFrames):
    def __init__(self, frames_obj, *args):
        super().__init__(frames_obj, *args)
        self.object_num = 0  # instance number, It shold be increased by data_set
        
    def print_infor(self) -> None:
        print('This is Fullframes' + str(self.object_num))
        super().print_additional_infor()



class ChFrames(FluoFrames):
    def __init__(self, frames_obj, *args):
        super().__init__(frames_obj, *args)
        self.object_num = 0  # instance number
        
    def print_infor(self) -> None:
        print('This is Chframes' + str(self.object_num))
        super().print_additional_infor()

        
"Fluo Image"
class FluoImage(Data):  # cell image, dif image
    def __init__(self, frames_obj: object, pixel_size=0, unit=0):  # 3D raw data from IO
        #self._image_obj  # create in _read_data
        self._frames_obj = frames_obj
        self._frame_window = [0,0]  # default [start, end] 
        self._pixel_size = pixel_size  # (um)
        self._unit = unit  # No unit because of raw camera data.
        
        self.__observer = DataObserver()  # obserbers for View

    def _read_data(self, data) -> None:
        pass

    def update(self):
        pass
    
    def get_data(self) -> object:  # -> value object
        return self._image_obj
    
    def get_infor(self) -> float:
        return self._pixel_size
    
    @property
    def image_obj(self):
        return self._image_obj
  
    @property
    def frame_window(self):
        return self._frame_window
    
    def show_data(self) -> None:
        self._image_obj.show_data()
    
    def print_infor(self):
        pass
    
    def print_add_infor(self) -> None:
        #np.set_printoptions(threshold=np.inf)  # This is for showing all data values.
        print(self._image_obj.data)
        print(self._image_obj.data.shape)
        print('The start frame number = ' + str(self._frame_window[0]))
        print('The end frame number = ' + str(self._frame_window[1]))
        #print(self._pixel_size)
        #print(self._unit)
        #np.set_printoptions(threshold=1000)


class CellImage(FluoImage):
    def __init__(self, frames_obj, *args):
        super().__init__(frames_obj, *args)
        self.object_num = 0  # instance number
        
        self._read_data(self._frame_window)

    def _read_data(self, frame_window) -> None:
        frame_length = self._frames_obj.data.shape[2]
        if frame_window[0] > frame_length-1 or frame_window[1] > frame_length-1: 
            raise Exception('The end frame should be the same as the frames length or less.')
        start = frame_window[0]
        end = frame_window[1]
        if end - start == 0:
            val = self._frames_obj.data[:, :, frame_window[0]]
            self._image_obj = ImageData(val)
            #print('Read a single cell image')
        elif end - start > 0: 
            val = np.mean(self._frames_obj.data[:, :, start:end], axis = 2)
            self._image_obj = ImageData(val)
            print(self._image_obj.data)
            #print('Read an avarage cell image')
        else:
            self._data = np.zeros((2, 2))
            raise Exception('The end frame should be higher than the start frame.')
        
    def update(self, frame_window_obj) -> None:  # value object
        self._frame_window = frame_window_obj.data  # frame_window = [start, end, start_width, end_width]
        self._read_data(self._frame_window)
        print('CellImage-{} recieved a notify message.'.format(self.object_num) + str(self._frame_window))
            
        
    def print_infor(self) -> None:
        print('This is CellImage-{}'.format(self.object_num))
        super().print_add_infor()
        
        
class DifImage(FluoImage):
    def __init__(self, frames_obj):
        super().__init__(frames_obj)
        self.object_num = 0  # instance number

    def _read_data(self):
        pass
        
    def update(self):
        pass

    def get_data(self):
        pass
    
    def get_infor(self):
        pass
    
    def print_infor(self):
        print('This is DifImage-{}'.format(self.object_num))
        super().print_add_infor()

            

"Fluo Trace"
class FluoTrace(Data):  # Fluo trae, Elec trace
    def __init__(self, frames_obj, interval):
        #self.__trace_obj  # create in _read_data
        self.__frames_obj = frames_obj
        self.__interval = interval
        self._roi = [40,40,1,1]  #default
        
        self._read_data(self._roi)
        
        self.__observer = DataObserver()  # obserbers for View

    def _read_data(self, roi: list) -> None:  # roi[x, y, x_length, y_length]
        x_size = self.__frames_obj.data.shape[0]
        y_size = self.__frames_obj.data.shape[1]

        if roi[0] + roi[2] > x_size - 1 or roi[1] + roi[3] > y_size - 1: 
            raise Exception("The roi size should be the same as the image size or less")
        if roi[0] < 0 or roi[1] < 0: 
            raise Exception("The roi should be the same as 0 or more")

        trace_val = self.__create_fluo_trace(self.__frames_obj, roi)
        self.__trace_obj = TraceData(trace_val, self.__interval)
    
    def update(self, roi_obj) -> None:
        pass
    
    def get_data(self) -> object:  # -> value object
        return self.__trace_obj
    
    def get_infor(self) -> float:
        return self.__interval
    
    @property
    def trace_obj(self):
        return self.__trace_obj
  
    @property
    def interval(self):
        return self.__interval
    
    @property
    def roi(self):
        return self._roi
    
    @staticmethod
    def __create_fluo_trace(frames_obj, roi) -> np.ndarray:
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frames_obj.data[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data
        print('Updated ROI = ' + str(roi))
        
    def __create_time_data(self, trace, interval) -> np.ndarray:
        num_data_point = interval * np.shape(trace)[0]
        time_val = np.linspace(interval, num_data_point, np.shape(trace)[0])
        return time_val
    
    def show_data(self) -> None:
        self.trace_obj.show_data()
        
    def print_infor(self):
        pass
    
    def print_add_infor(self) -> None:
        #np.set_printoptions(threshold=np.inf)  # This is for showing all data values.
        print(self.__trace_obj.data)
        print(self.__trace_obj.data.shape)
        print(self.__interval)
        #np.set_printoptions(threshold=1000)

 
class FullTrace(FluoTrace):
    def __init__(self, frames_obj, interval):
        super().__init__(frames_obj, interval)
        self.object_num = 0  # instance number
        self.__name = None

    def update(self, roi_obj: object) -> None:  # value object
        self._roi = roi_obj.data
        super()._read_data(self._roi)
        self.__name = str('FullTrace-' + str(self.object_num))
        print('FullTrace-{} recieved a notify message.'.format(self.object_num))
        
    def print_infor(self) -> None:
        print('This is ' + self.__name)
        super().print_add_infor()
        
    @property
    def name(self):
        return self.__name
        

class ChTrace(FluoTrace):
    def __init__(self, frames_obj, interval):
        super().__init__(frames_obj, interval)
        self.object_num = 0  # instance number
        self.__name = None
        
    def update(self, roi_obj: list) -> None:  # value object
        self._roi = roi_obj.data
        super()._read_data(self._roi)
        self.__name = str('ChTrace-' + str(self.object_num))
        print('ChTrace-{} recieved a notify message.'.format(self.object_num))
        
    def print_infor(self) -> None:
        print('This is ChTrace-{}'.format(self.object_num))
        super().print_add_infor()
        
    @property
    def name(self):
        return self.__name


"Elec trace"
class ElecTrace(Data):  # Fluo trae, Elec trace
    def __init__(self, interval):
        #self._trace_obj  # create in _read_data of sub classes
        self._interval = interval
        
        self.__observer = DataObserver()  # obserbers for View
        
    def _read_data(self):
        pass
    
    def update(self, roi_obj) -> None:
        pass
    
    def get_data(self) -> object:  # -> value object
        return self._trace_obj
    
    def get_infor(self) -> float:
        return self._interval
    
    @property
    def trace_obj(self):
        return self._trace_obj
  
    @property
    def interval(self):
        return self._interval
    
    def show_data(self) -> None:
        self._trace_obj.show_data()  
    
    def print_infor(self):
        pass
        
class ChElecTrace(ElecTrace):
    def __init__(self, trace_data_obj, interval):
        super().__init__(interval)
        self.object_num = 0  # instance number
        self._read_data(trace_data_obj)

    def _read_data(self, trace_data_obj: np.ndarray) -> None:
        self._trace_obj = trace_data_obj
        
        if len(self._trace_obj.data) <= 1:
            print('---------------------')
            print('Can not make Elec data')
            print('---------------------')
            return None
    
    def print_infor(self):
        print('This is ElecTrace' + str(self.object_num))
        print(self._trace_obj.data)
        
class LongElecTrace(ElecTrace):
    pass
        

class DataObserver:
    def __init__(self):
        self.__observers = []  # for view
        
    def add_observer(self, observer):
        self.__observers.append(observer)
        
    def remove_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        for observer_name in self.__observers:
            observer_name.update()

if __name__ == '__main__':
    pass

