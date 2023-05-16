# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 17:33:00 2023

@author: lunelukkio
"""

from abc import ABCMeta, abstractmethod
import copy
from SCANDATA.model.repository import Repository
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import CellImageFactory
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.data_factory import ChElecFactory
from SCANDATA.model.controller_factory import RoiFactory, FrameWindowFactory, ElecControllerFactory
from SCANDATA.model.value_object import FramesData, TraceData


"""
Builder
"""
class Builder(metaclass=ABCMeta):
    @abstractmethod
    def read_file(self, filename) -> None:
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


class ImagingBuilder(Builder):
    def __init__(self, filename):
        self.__filename = filename
        self.__data+repository = Repository()
        self.reset()                                                                                                           
        
    def reset(self) -> tuple:
        #self.__file_io = WeakValueDictionary()  # weak referece dictionary
        #self.__data = WeakValueDictionary()  # weak referece dictionary
        #self.__controller = WeakValueDictionary()  # weak referece dictionary
        
        self.__file_io = {}
        self.__data = {}
        self.__controller = {}
        
        self.__file_io_counter = {}  # dict
        self.__data_counter = {}  # dict
        self.__controller_counter = {}  # dict
        
        return self.__file_io, self.__data, self.__controller
        
    # make a full frames and channel frames from data files.
    def initialize(self):  # for making Frames data without traces and images.
        # make file_io
        tsm = self.create_file_io(TsmFileIOFactory(), self.__filename)
        tbn = self.create_file_io(TbnFileIOFactory(), self.__filename, tsm)
        
        # get raw frames data and interval
        tsm_raw_data_tuple = copy.deepcopy(tsm.get_data())  # made indipendent from the file
        interval = copy.deepcopy(tsm.get_infor())  # made indipendent from the file
        full_interval = interval[0]
        ch_interval = interval[1]
        
        # make full frames
        full_frames = FramesData(tsm_raw_data_tuple[0])  # Value object from raw data.
        self.create_data(FullFramesFactory(), full_frames, full_interval)
        
        # make ch frames
        for i in range(0, tsm_raw_data_tuple[1].shape[3]):
            ch_frames = FramesData(tsm_raw_data_tuple[1][:, :, :, i])
            self.create_data(ChFramesFactory(), ch_frames, ch_interval)
        
class FileIOBuilder(Builder):
    def __int__(self, filename):
        self.file_io = Translator.file_type_checker(filename)
    
    def create_data(self, factory_type, filename, *args) -> object:  # factory_type
        product = factory_type.create_file_io(filename, *args)
        object_name = product.__class__.__name__  # str
        
        last_num = self.__file_io_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        
        self.__file_io_counter[object_name] = new_num  # Add key and object_num to counter dict.
        self.__file_io[object_name + str(product.object_num)] = product
        return product
    
class FluoTraceBuilder(Builder):
    # for making a single trace    
    def create_data(self, factory_type, data, *args) -> object:
        product = factory_type.create_data(data, *args)
        object_name = product.__class__.__name__  # str
        
        last_num = self.__data_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        product.name = object_name + str(new_num)
        
        self.__data_counter[object_name] = new_num  # Add key and object_num to a counter dict.
        self.__data[object_name + str(product.object_num)] = product
        return product
    
class Controller_builder(Builder):
    def create_controller(self, factory_type) -> object:
        product = factory_type.create_controller()
        object_name = product.__class__.__name__  # str
        
        last_num = self.__controller_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        
        self.__controller_counter[object_name] = new_num  # Add key and object_num to counter dict.
        self.__controller[object_name + str(product.object_num)] = product
        return product 
    
class ImageBuilder(Builder):
    def build_image_set(self, data_set) -> None:
        entity_name_list = []  # for FrameWindowView
        frame_window = self.create_controller(FrameWindowFactory())
        # Make an image from full trace
        full_image = self.create_data(CellImageFactory(), data_set['FullFrames1'].frames_obj)
        frame_window.add_observer(full_image)
        entity_name_list.append(full_image.name)
        
        # make images from ch traces
        num_ch_frames = KeyCounter.count_key(data_set, 'ChFrames')
        ch_frames_list = []
        for i in range(0, num_ch_frames):
            ch_frames_list.append(data_set['ChFrames' + str(i+1)])
        for i in ch_frames_list:
            image = self.create_data(CellImageFactory(), i.frames_obj)
            frame_window.add_observer(image)
            entity_name_list.append(image.name)
        return entity_name_list
    
class TraceBuilder(Builder):
    # for making trace data set
    def build_trace_set(self, data_set) -> None:
        entity_name_list = []  # for RoiView
        # Make a controller
        roi = self.create_controller(RoiFactory())
        # Make traces
        full_trace = self.create_data(FullTraceFactory(), 
                                      data_set['FullFrames1'].frames_obj, 
                                      data_set['FullFrames1'].interval)
        roi.add_observer(full_trace)
        entity_name_list.append(full_trace.name)

        num_ch_frames = KeyCounter.count_key(data_set, 'ChFrames')
        ch_frames_list = []
        for i in range(0, num_ch_frames):
            ch_frames_list.append(data_set['ChFrames' + str(i+1)])
        for i in ch_frames_list:
            trace = self.create_data(ChTraceFactory(), i.frames_obj, i.interval)
            roi.add_observer(trace)
            entity_name_list.append(trace.name)
        return entity_name_list
            
class ElecDataBuilder(Builder):
    def build_elec_data_set(self, raw_data):
        entity_name_list = []  # for ElecView
        # Make a controller
        elec_controller = self.create_controller(ElecControllerFactory())
        # Make elec traces
        raw_elec_data = copy.deepcopy(raw_data['TbnFileIO1'].get_data())  # made indipendent from the file
        elec_interval = copy.deepcopy(raw_data['TbnFileIO1'].get_infor())    # made indipendent from the file
        num_elec_ch = raw_elec_data.shape[1]

        for i in range(0, num_elec_ch):
            # Convert from raw data to a value object
            elec_trace_obj = TraceData(raw_elec_data[:,i], elec_interval)
            # make channel electric data
            trace = self.create_data(ChElecFactory(), elec_trace_obj, elec_interval)
            elec_controller.add_observer(trace)
            entity_name_list.append(trace.name)
        return entity_name_list
        
xx    def count_data(self):
        #num = 2  # This should be got from cunting ChFrames.
        #ch_frames_list = []
        #for i in range(0, num):
        #    ch_frames_list.append(data_set['ChFrames' + str(i+1)])
        pass

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
        

class KeyCounter:
    @staticmethod
    def count_key(key_dict, key):
        num = 0
        key_list = key_dict.keys()
        for i in key_list:
            if key in i:
                num += 1
        return num    

