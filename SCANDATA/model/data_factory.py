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
    def create_data(self, data):
        pass


"Frames"
class FullFramesFactory(DataFactory):
    def create_data(self, data):  # data = file_io
        return FullFrame(data)


class ChFramesFactory(DataFactory):
    def create_data(self, data):  # data = file_io
        return ChFrame(data)


"Image"
class CellImageFactory(DataFactory):
    def create_data(self, data):  # data = frame
        return CellImage(data)


class DifImageFactory(DataFactory):
    def create_data(self, data):  # data = frame
        return DifImage(data)


"Trace"
class FullTraceFactory(DataFactory):
    def create_data(self, data):  # data = frame
        return FullTrace(data)

class ChTraceFactory(DataFactory):
    def create_data(self, data):  # data = frame
        return ChTrace(data)
    
class BGTraceFactory(DataFactory):
    def create_data(self, data):  # data = frame
        return BGTrace(data)
    
class ElecTraceFactory(DataFactory):
    def create_data(self, data, interval):  # data = file_io (.tbn)
        return ElecTrace(data)
    

"""
product
"""
class Data(metaclass=ABCMeta):
    @abstractmethod
    def read_data(self, data):
        pass
    
    @abstractmethod
    def update_data(self, val):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def show_data(self):
        pass
    
    @abstractmethod
    def print_infor(self):
        pass



"FluoFrame"
class FluoFrame(Data):  # 3D frame data: full frame, ch image
    def __init__(self, data, interval):
        self.frame_data = FrameData()
        self.interval = 0  # (ms)
        self.pixel = 0  # (um)
        self.unit = 0  # No unit because of raw camera data.

        self.read_data(data, interval)

    def read_data(self, data, interval):
        self.frame_data = copy.deepcopy(data)
        self.interval = copy.deepcopy(interval)
        
        if len(self.frame_data) <= 1:
            print('---------------------')
            print('Can not make Frame data')
            print('---------------------')
            return None
    
    def get_data(self):
        frame = self.frame_data
        interval = self.full_frame_interval
        return frame, interval

    def update(self):
        pass

    def show_frame(self, frame):
        plt.imshow(self.frame_data[:, :, frame], cmap='gray', interpolation='none')

    def print_frame_infor(self):
        #np.set_printoptions(threshold=np.inf)
        print(self.data_type)
        print(self.data.shape)
        print(self.time_data)

        #np.set_printoptions(threshold=1000)


class FullFrame(FluoFrame):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a FullFrame')
        
    def print_name(self):
        print('This is FullFrame' + str(self.num))


class ChFrame(FluoFrame):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a ChFrame')
        
    def print_name(self):
        print('This is ChFrame' + str(self.num))


"Value Object for Frames"
class FrameData():
    def __init__(self):
        self.data = np.empty(1, 1, 1)
        
    def set_val(self, val):
        self.data = val
        
    def check_val(self):
        if self.data.shape != 3:          
            raise Exception("This object should be 3D data")
            
    def add(self,a,b):
        return a+b
        












class Image(metaclass=ABCMeta):  # cell image, dif image
    def __init__(self, data):
        self.image_data = np.array([0, 0])
        
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

"Image"
class CellImage(Image):
    def __init__(self, data):
        super().__init__(data)
        self.object_num = 0  # instance number
        
        self.frame_data = data

    def read_data(self, val):
        start = val[0]
        end = val[1]

        if end - start == 0:
            self.image_data = self.frame_data[:, :, val[0]]
            print('Read a single cell image')
        elif end - start > 0: 
            self.image_data = np.mean(self.frame_data[:, :, start:end], axis = 2)
            print('Read an avarage cell image')
        else:
            self.image_data = np.zeros((2, 2))
            print('-----------------------------------------------------')
            print('The end frame should be higher than the start frame.')
            print('-----------------------------------------------------')
        
    def update(self, val):
        self.read_data(val)
        print('CellImage recieved a notify message.')

    def get_data(self):
        pass
    
    def show_image(self):
            plt.imshow(self.image_data, cmap='gray', interpolation='none')
            
    def print_name(self):
        print('This is CellImage' + str(self.num))
        
class DifImage(Image):
    def __init__(self, data):
        super().__init__(data)
        self.object_num = 0  # instance number

    def read_data(self):
        pass
        
    def update(self):
        pass

    def get_data(self):
        pass
    
    def print_name(self):
        print('This is DifImage' + str(self.num))


"Trace"
class Trace(metaclass=ABCMeta):  # Fluo trae, Elec trace
    def __init__(self):
        self.trace_data = np.array([0,])
        self.time_data = np.array([0,])
        
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

    def plot_trace(self):
        plt.plot(self.time_data, self.trace_data)   

class FluoTrace(Trace):
    def __init__(self, data, interval):
        super().__init__()
        self.frame_data = data
        self.interval = copy.deepcopy(interval)
        # trace_data and time_data are in the super class
        
        self.read_data([40, 40, 1, 1])
        self.create_time_data()

    def read_data(self, roi):  # roi[x, y, x_length, y_length]   
        self.trace_data = self.fluo_trace_creator(self.frame_data, roi)
        
    @staticmethod
    def fluo_trace_creator(frame, roi):
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frame[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data
        print('Undated ROI = ' + str(roi))
    
    def create_time_data(self):
        num_data_point = self.interval * np.shape(self.trace_data)[0]
        self.time_data = np.linspace(self.interval, 
                                     num_data_point, 
                                     np.shape(self.trace_data)[0])
    
    def update(self, roi_obj):
        self.read_data(roi_obj)
        print('FluoTrace recieved a notify message.')
    
    def get_data(self):
        pass
 
class FullTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a FullTrace')
        
    def print_name(self):
        print('This is FullTrace' + str(self.num))
        
class ChTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a ChTrace')
        
    def print_name(self):
        print('This is ChTrace' + str(self.num))
        
class BGTrace(FluoTrace):
    def __init__(self, data, interval):
        super().__init__(data, interval)
        self.object_num = 0  # instance number
        print('Made a BGTrace')
        
    def print_name(self):
        print('This is BGTrace' + str(self.num))

class ElecTrace(Trace):
    def __init__(self, data, interval):
        super().__init__()
        self.object_num = 0  # instance number
        self.read_data(data, interval)
        print('Made a ElecTrace')

    def read_data(self, data, interval):
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
        print('This is ElecTrace' + str(self.num))


if __name__ == '__main__':
    filename = '20408A001.tsm'
    filepath = '..\\220408\\'

    testframe = FrameData()
    testframe.check_val()
