# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

"""

from abc import ABCMeta, abstractmethod
from weakref import WeakValueDictionary
import pprint
from SCANDATA.model.io_factory import TsmFileIOFactory, TbnFileIOFactory
from SCANDATA.model.data_factory import FullFramesFactory, ChFramesFactory
from SCANDATA.model.data_factory import CellImageFactory
from SCANDATA.model.data_factory import FullTraceFactory, ChTraceFactory
from SCANDATA.model.data_factory import CameraSyncElecTraceFactory
from SCANDATA.model.controller_factory import RoiFactory, FrameWindowFactory

class Experiments():
    pass

class DataSet():
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
        self.__model_controller = objects[2]
        
        pprint.pprint(self.__file_io.keys())
        pprint.pprint(self.__data.keys())
        pprint.pprint(self.__model_controller.keys())
        
        
    """
    waht is best
    """    
    @property
    def data(self):
        return self.__data
    
    @property
    def model_controller(self):
        return self.__model_controller

    def get_data(self, data_type):
        self.__data[data_type].get_data()
    """
    ???
    """


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
            
        # This is for additional trace or roi etc. eg def add_trace()
        def make_trace(self):
            full_frames = self.data['FullFrames1']
            ch1_frames = self.data['ChFrames1']
            ch2_frames = self.data['ChFrames2']
            self.__director.build_traces(self.__filename, self.__filepath, full_frames, ch1_frames, ch2_frames)

    
class Builder(metaclass=ABCMeta):
    @abstractmethod
    def create_file_io(self, factory_type, filename, filepath, *args) -> None:
        pass

    @abstractmethod
    def create_data(self, factory_type, data, *args) -> None:
        pass

    @abstractmethod
    def create_model_controller(self, factory_type) -> None:
        pass
    
    @abstractmethod
    def get_result(self) -> None:
        pass


class TsmFileBuilder(Builder):
    def __init__(self):
        self.reset()
        
    def reset(self) -> None:
        #self.__file_io = WeakValueDictionary()  # weak referece dictionary
        #self.__data = WeakValueDictionary()  # weak referece dictionary
        #self.__model_controller = WeakValueDictionary()  # weak referece dictionary
        
        self.__file_io = {}
        self.__data = {}
        self.__model_controller = {}
        
        self.__file_io_counter = {}  # dict
        self.__data_counter = {}  # dict
        self.__model_controller_counter = {}  # dict
        
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
    
    def create_model_controller(self, factory_type) -> object:
        product = factory_type.create_model_controller()
        object_name = product.__class__.__name__  # str
        
        last_num = self.__model_controller_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.object_num = new_num  # Add counter num to instance.
        
        self.__model_controller_counter[object_name] = new_num  # Add key and object_num to counter dict.
        self.__model_controller[object_name + str(product.object_num)] = product
        return product
    
    @property
    def file_io(self) -> dict:
        return self.__file_io
    
    @property
    def data(self) -> dict:
        return self.__data
    
    @property
    def model_controller(self) -> dict:
        return self.__model_controller
        
    def get_result(self) -> tuple:
        return self.__file_io, self.__data, self.__model_controller


class AbfFileBuilder(Builder):

    def create_file_io(self, factory_type) -> None:
        raise NotImplementedError()

    def create_data(self, factory_type) -> None:
        raise NotImplementedError()


    def create_model_controller(self, factory_type) -> None:
        raise NotImplementedError()
    

    def get_result(self) -> None:
        raise NotImplementedError()
        

class WcpFileBuilder(Builder):

    def create_file_io(self, factory_type) -> None:
        raise NotImplementedError()

    def create_data(self, factory_type) -> None:
        raise NotImplementedError()


    def create_model_controller(self, factory_type) -> None:
        raise NotImplementedError()
    

    def get_result(self) -> None:
        raise NotImplementedError()
    

class Director():
    def __init__(self) -> None:
        self.__builder = None  # This decide which file_type will it use. (e.g. .tsm)

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
        
        # make frames
        data = tsm.get_data()
        interval = tsm.get_infor()
        full_frames = data[0]
        ch1_frames = data[1][:, :, :, 0]
        ch2_frames = data[1][:, :, :, 1]
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
        elec_data = tbn.get_data()
        elec_interval = tbn.get_infor()
        num_elec_ch = elec_data.shape[1]

        for i in range(0, num_elec_ch):
            self.builder.create_data(CameraSyncElecTraceFactory(), elec_data[:,i], elec_interval)

        # make model controller
        roi = self.builder.create_model_controller(RoiFactory())
        frame_window = self.builder.create_model_controller(FrameWindowFactory())
        
        #bind controller to data
        roi.add_observer(full_trace)
        roi.add_observer(ch1_trace)
        roi.add_observer(ch2_trace)
        frame_window.add_observer(ch1_image)
        frame_window.add_observer(ch2_image)

    def build_traces(self, filename, filepath, full_frames: object, ch1_frames: object, ch2_frames: object) -> None:
        full_trace = self.builder.create_data(FullTraceFactory(), full_frames.get_data(), full_frames.get_infor())
        ch1_trace = self.builder.create_data(FullTraceFactory(), ch1_frames.get_data(), ch2_frames.get_infor())
        ch2_trace = self.builder.create_data(FullTraceFactory(), ch2_frames.get_data(), ch2_frames.get_infor())
        
        roi = self.builder.create_model_controller(RoiFactory())
        
        roi.add_observer(full_trace)
        roi.add_observer(ch1_trace)
        roi.add_observer(ch2_trace)
        
    def build_images(self, filename, filepath, full_frames: object, ch1_frames: object, ch2_frames: object) -> None:
        ch1_image = self.builder.create_data(CellImageFactory(), ch1_frames.get_data())
        ch2_image = self.builder.create_data(CellImageFactory(), ch2_frames.get_data())
        
        frame_window = self.builder.create_model_controller(FrameWindowFactory())
        
        frame_window.add_observer(ch1_image)
        frame_window.add_observer(ch2_image)
        
    
if __name__ == '__main__':
    pass
    


    
    

