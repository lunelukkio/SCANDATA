# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 17:33:00 2023

@author: lulul
"""

from abc import ABCMeta, abstractmethod
from weakref import WeakValueDictionary
import copy
from SCANDATA.model.io_factory import TsmFileIOFactory, TbnFileIOFactory
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import CellImageFactory
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.data_factory import ChElecTraceFactory
from SCANDATA.model.controller_factory import RoiFactory, FrameWindowFactory
from SCANDATA.model.value_object import FramesData, TraceData

"""
Builder
"""
class Builder(metaclass=ABCMeta):
    @abstractmethod
    def create_file_io(self, factory_type, filename, *args) -> None:
        raise NotImplementedError()

    @abstractmethod
    def create_data(self, factory_type, data, *args) -> None:
        raise NotImplementedError()

    @abstractmethod
    def create_controller(self, factory_type) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_result(self) -> None:
        raise NotImplementedError()


class TsmFileBuilder(Builder):
    def __init__(self, filename):
        self.__filename = filename
        self.reset()
        self.initialize()
        
    def reset(self) -> None:
        #self.__file_io = WeakValueDictionary()  # weak referece dictionary
        #self.__data = WeakValueDictionary()  # weak referece dictionary
        #self.__controller = WeakValueDictionary()  # weak referece dictionary
        
        self.__file_io = {}
        self.__data = {}
        self.__controller = {}
        
        self.__file_io_counter = {}  # dict
        self.__data_counter = {}  # dict
        self.__controller_counter = {}  # dict
        
    def initialize(self):
        # make file_io
        tsm = self.create_file_io(TsmFileIOFactory(), self.__filename)
        tbn = self.create_file_io(TbnFileIOFactory(), self.__filename, tsm)
        
        # get raw frames data and interval
        tsm_raw_data_tuple = copy.deepcopy(tsm.get_data())  # made indipendent from the file
        interval = copy.deepcopy(tsm.get_infor())  # made indipendent from the file
        full_interval = interval[0]
        ch_interval = interval[1]
        
        # make full frames and ch frames from full frames
        full_frames = FramesData(tsm_raw_data_tuple[0])  # Value object from raw data.
        self.create_data(FullFramesFactory(), full_frames, full_interval)
        
        # make trace data
        self.build_traces_set(data_set)
        
    def create_file_io(self, factory_type, filename, *args) -> object:  # factory_type from director???
        product = factory_type.create_file_io(filename, *args)
        object_name = product.__class__.__name__  # str
        
        last_num = self.__file_io_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        
        self.__file_io_counter[object_name] = new_num  # Add key and object_num to counter dict.
        self.__file_io[object_name + str(product.object_num)] = product
        return product
        
    def create_data(self, factory_type, data, *args) -> object:
        product = factory_type.create_data(data, *args)
        object_name = product.__class__.__name__  # str
        
        last_num = self.__data_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        
        self.__data_counter[object_name] = new_num  # Add key and object_num to a counter dict.
        self.__data[object_name + str(product.object_num)] = product
        return product
    
    def create_controller(self, factory_type) -> object:
        product = factory_type.create_controller()
        object_name = product.__class__.__name__  # str
        
        last_num = self.__controller_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        
        self.__controller_counter[object_name] = new_num  # Add key and object_num to counter dict.
        self.__controller[object_name + str(product.object_num)] = product
        return product
    
    def build_images_set(self, data_set) -> None:
        frame_window = self.builder.create_controller(FrameWindowFactory())
        for i in (data_set['ChFrames1'], data_set['ChFrames2']):
            image = self.builder.create_data(CellImageFactory(), i.frames_obj)
            frame_window.add_observer(image)
    
    def build_traces_set(self, data_set) -> None:
        roi = self.create_controller(RoiFactory())
        full_trace = self.create_data(FullTraceFactory(), 
                                      data_set['FullFrames1'].frames_obj, 
                                      data_set['FullFrames1'].interval)
        roi.add_observer(full_trace)
        print('Tip count ChFrames')
        for i in (data_set['ChFrames1'], data_set['ChFrames2']):
            trace = self.create_data(ChTraceFactory(), i.frames_obj, i.interval)
            roi.add_observer(trace)

    @property
    def file_io(self) -> dict:
        return self.__file_io
    
    @property
    def data(self) -> dict:
        return self.__data
    
    @property
    def controller(self) -> dict:
        return self.__controller
        
    def get_result(self) -> tuple:
        return self.__file_io, self.__data, self.__controller


class AbfFileBuilder(Builder):

    def create_file_io(self, factory_type) -> None:
        raise NotImplementedError()

    def create_data(self, factory_type) -> None:
        raise NotImplementedError()

    def create_controller(self, factory_type) -> None:
        raise NotImplementedError()
    
    def get_result(self) -> None:
        raise NotImplementedError()
        

class WcpFileBuilder(Builder):

    def create_file_io(self, factory_type) -> None:
        raise NotImplementedError()

    def create_data(self, factory_type) -> None:
        raise NotImplementedError()

    def create_controller(self, factory_type) -> None:
        raise NotImplementedError()
    
    def get_result(self) -> None:
        raise NotImplementedError()
    

class Director:
    #def __init__(self) -> None:
    #    self.__builder = None  # This decide which file_type will it use. (e.g. .tsm)

    #@property
    #def builder(self) -> Builder:
    #    return self.__builder

    #@builder.setter
    #def builder(self, builder: Builder) -> None:
    #    self.__builder = builder
        
    def build_initial_data_set(self, filename) -> None:
        # make file_io
        #tsm = self.builder.create_file_io(TsmFileIOFactory(), filename)
        #tbn = self.builder.create_file_io(TbnFileIOFactory(), filename, tsm)
        
        # get raw frames data and interval
        #tsm_raw_data_tuple = copy.deepcopy(tsm.get_data())  # made indipendent from the file
        #interval = copy.deepcopy(tsm.get_infor())  # made indipendent from the file
        #full_interval = interval[0]
        #ch_interval = interval[1]

        # make frames
        #full_frames = FramesData(tsm_raw_data_tuple[0])
        #self.builder.create_data(FullFramesFactory(), full_frames, full_interval)
        
        # make trace data
        #self.build_traces_data_set(data_set)

        
        # make ch data set
        for i in range(0, tsm_raw_data_tuple[1].shape[3]):
            ch_frames = FramesData(tsm_raw_data_tuple[1][:, :, :, i])
            self.builder.create_data(ChFramesFactory(), ch_frames, ch_interval)
            image = self.builder.create_data(CellImageFactory(), ch_frames)
            trace = self.builder.create_data(ChTraceFactory(), ch_frames, ch_interval)
            # bind controller to data
            frame_window.add_observer(image)
            roi.add_observer(trace)
            
            # Make ch backgrand traces
            bg_trace = self.builder.create_data(ChTraceFactory(), ch_frames, ch_interval)
            # bind controller to data
            bg_roi.add_observer(bg_trace)

        # make elec traes
        elec_data = copy.deepcopy(tbn.get_data())  # made indipendent from the file
        elec_interval = copy.deepcopy(tbn.get_infor())    # made indipendent from the file
        num_elec_ch = elec_data.shape[1]

        for i in range(0, num_elec_ch):
            # Convert from raw data to a value object
            elec_trace_obj = TraceData(elec_data[:,i], elec_interval)
            # make ElecTrace
            self.builder.create_data(ChElecTraceFactory(), elec_trace_obj, elec_interval)
        
    def build_images_data_set(self, data_set) -> None:
        frame_window = self.builder.create_controller(FrameWindowFactory())
        for i in (data_set['ChFrames'], data_set['ChFrames']):
            image = self.builder.create_data(CellImageFactory(), i.frames_obj)
            frame_window.add_observer(image)

    #def build_traces_data_set(self, data_set) -> None:
    #    roi = self.builder.create_controller(RoiFactory())
    #    full_trace = self.builder.create_data(FullTraceFactory(), data_set['FullFrames1'].frames_obj, data_set['FullFrames1'].interval)
    #    roi.add_observer(full_trace)
    #    for i in (data_set['ChFrames1'], data_set['ChFrames2']):
    #        trace = self.builder.create_data(ChTraceFactory(), i.frames_obj, i.interval)
    #        roi.add_observer(trace)