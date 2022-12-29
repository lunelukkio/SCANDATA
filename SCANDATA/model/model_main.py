# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

"""

from abc import ABCMeta, abstractmethod
from weakref import WeakValueDictionary
import pprint
import copy
from SCANDATA.model.io_factory import TsmFileIOFactory, TbnFileIOFactory
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import CellImageFactory
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.data_factory import ChElecTraceFactory
from SCANDATA.model.controller_factory import RoiFactory, FrameWindowFactory
from SCANDATA.model.data_factory import ValueObjConverter


class Experiments:
    pass


class DataSet:
    def __init__(self, filename, filepath):
        self.__filename = filename
        self.__filepath = filepath
        builder_type = self.file_type_checker(filename)
        
        self.__director = Director()  # Director makes the cartain default set of the experiments. 
        self.__builder = builder_type
        self.__director.builder = self.__builder  # Set a builder throuh the setter of Director.

        #initial deta set
        self.__director.build_initial_data_set(filename, filepath)
        
        # get dict from the builder
        objects = self.__builder.get_result()
        self.__file_io = objects[0]
        self.__data = objects[1]
        self.__controller = objects[2]
        
        self.print_infor()
        
    @property
    def data(self):
        return self.__data
    
    @property
    def controller(self):
        return self.__controller

    def get_data(self, data_type):
        return self.__data[data_type].get_data()

    @staticmethod
    def file_type_checker(filename):
        if filename.find('.tsm') > 0:
            print('Found a .tsm file')
            return TsmFileBuilder()
        elif filename.find('.abf') > 0:
            print('Found an .abf file')
            return AbfFileBuilder()
        elif filename.find('.wcp') > 0:
            print('Found a .wcp file')
            return WcpFileBuilder()
        else:
            print('--------------------------------------')
            print('Can not find any builder for this file')
            print('--------------------------------------')
            raise Exception("The file is incorrect!!!")
                
    def build_image(self ,data, *args):
        self.__director.build_images_data_set(data, *args)

    
    def build_trace(self, data, *args):
        self.__director.build_traces_data_set(data, *args)
        
    def print_infor(self):
        pprint.pprint('IO Keys = ' + str(self.__file_io.keys()))
        pprint.pprint('Data Keys = ' + str(self.__data.keys()))
        pprint.pprint('Controller Keys = ' + str(self.__controller.keys()))

    
class Builder(metaclass=ABCMeta):
    @abstractmethod
    def create_file_io(self, factory_type, filename, filepath, *args) -> None:
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
    def __init__(self):
        self.reset()
        
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
        
    def create_file_io(self, factory_type, filename, filepath, *args) -> object:  # factory_type from director???
        product = factory_type.create_file_io(filename, filepath, *args)
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
        
        self.__data_counter[object_name] = new_num  # Add key and object_num to counter dict.
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
    def __init__(self) -> None:
        self.__builder = None  # This decide which file_type will it use. (e.g. .tsm)
        self.converter = ValueObjConverter()

    @property
    def builder(self) -> Builder:
        return self.__builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self.__builder = builder
        
    def build_initial_data_set(self, filename, filepath) -> None:
        # make file_io
        tsm = self.builder.create_file_io(TsmFileIOFactory(), filename, filepath)
        tbn = self.builder.create_file_io(TbnFileIOFactory(), filename, filepath, tsm)
        
        # get raw frames data and interval
        tsm_raw_data_tuple = copy.deepcopy(tsm.get_data())  # made indipendent from the file
        interval = copy.deepcopy(tsm.get_infor())  # made indipendent from the file

        # Convert from raw data to a value object
        full_frames = self.converter.frames_converter(tsm_raw_data_tuple[0])
        #for i in range(0, tsm_raw_data_tuple[1].shape(3)):
        ch1_frames = self.converter.frames_converter(tsm_raw_data_tuple[1][:, :, :, 0])
        ch2_frames = self.converter.frames_converter(tsm_raw_data_tuple[1][:, :, :, 1])
        
        # make frames
        full_interval = interval[0]
        ch_interval = interval[1]
        self.builder.create_data(FullFramesFactory(), full_frames, full_interval)
        self.builder.create_data(ChFramesFactory(), ch1_frames, ch_interval)
        self.builder.create_data(ChFramesFactory(), ch2_frames, ch_interval)

        # make images
        ch1_image = self.builder.create_data(CellImageFactory(), ch1_frames)
        ch2_image = self.builder.create_data(CellImageFactory(), ch2_frames)

        # make fluo traces
        full_trace = self.builder.create_data(FullTraceFactory(), full_frames, full_interval)
        ch1_trace = self.builder.create_data(ChTraceFactory(), ch1_frames, ch_interval)
        ch2_trace = self.builder.create_data(ChTraceFactory(), ch2_frames, ch_interval)
        
        #make elec traes
        elec_data = copy.deepcopy(tbn.get_data())  # made indipendent from the file
        elec_interval = copy.deepcopy(tbn.get_infor())    # made indipendent from the file
        num_elec_ch = elec_data.shape[1]

        for i in range(0, num_elec_ch):
            # Convert from raw data to a value object
            elec_trace_obj = self.converter.elec_trace_converter(elec_data[:,i], elec_interval)
            # make ElecTrace
            self.builder.create_data(ChElecTraceFactory(), elec_trace_obj, elec_interval)

        # make model controller
        roi = self.builder.create_controller(RoiFactory())
        frame_window = self.builder.create_controller(FrameWindowFactory())
        
        #bind controller to data
        roi.add_observer(full_trace)
        roi.add_observer(ch1_trace)
        roi.add_observer(ch2_trace)
        frame_window.add_observer(ch1_image)
        frame_window.add_observer(ch2_image)
        
    def build_images_data_set(self, full_frame, *args) -> None:
        frame_window = self.builder.create_controller(FrameWindowFactory())
        for i in (args):
            image = self.builder.create_data(CellImageFactory(), i.frames_obj)
            frame_window.add_observer(image)

    def build_traces_data_set(self, full_frames, *args) -> None:
        roi = self.builder.create_controller(RoiFactory())
        full_trace = self.builder.create_data(FullTraceFactory(), full_frames.frames_obj, full_frames.interval)
        roi.add_observer(full_trace)
        for i in (args):
            trace = self.builder.create_data(ChTraceFactory(), i.frames_obj, i.interval)
            roi.add_observer(trace)
        
    
if __name__ == '__main__':
    pass
    


    
    

