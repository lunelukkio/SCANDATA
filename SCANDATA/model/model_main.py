# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

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
from SCANDATA.model.value_object import Filename, FramesData, TraceData


class ExperimentsInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_data_set(self, fullname):
        raise NotImplementedError()
        
    @abstractmethod
    def create_data(self, filename, key, *args):
        raise NotImplementedError()
        
    @abstractmethod
    def set_data(self, filename: str, key: str, val: tuple):
        raise NotImplementedError()
        
    @abstractmethod
    def add_data(self, filename: str, key: str):
        raise NotImplementedError()
        
    @abstractmethod
    def get_data(self, filename: str, key: str):
        raise NotImplementedError()
    
    @abstractmethod
    def reset_data(self, filename: str, key: str):
        raise NotImplementedError()
        
    @abstractmethod
    def data_set(self):  # get a list of data_set objects
        raise NotImplementedError()


class Experiments(ExperimentsInterface):
    def __init__(self):
        self.__data_set = {}
        print('Created an empty model.')
    
    def create_data_set(self, fullname: str):
        filename = Filename(fullname)
        
        self.__data_set[filename.name] = DataSet(filename)  # dict of data_file(key filename : object)
        print(self.data_set)
        print('Created {} data set.'.format(filename.name))
        
    def create_data(self, filename, key: str, *args):
        self.__data_set[filename].create_data(key)
            
    def set_data(self, filename: str, key: str, val: tuple):
        self.data_set[filename].set_data(key, val)
        
    def add_data(self, filename: str, key: str, val: tuple):
        self.data_set[filename].add_data(key, val)
        
    def get_data(self, filename: str, key: str):
        return self.data_set[filename].get_data(key)
    
    def bind_data(self, controller: str, data: str, filename_ctrl: str, filename_data: str):
        binding_controller = self.data_set[filename_ctrl].controller[controller]
        binding_key = self.data_set[filename_data].data[data]
        binding_controller.add_observer(binding_key)
        
    def reset_data(self, filename: str, key: str):
        self.data_set[filename].reset_data(key)
        
    @property
    def data_set(self):
        return self.__data_set
        
    def help(self):
        print('===================================================================================')
        print('HELP for commands to MODEL')
        print('create_data_set(fullname: str): for making a new data set.     <------------ only this is full file name.')
        print('            e.g. create_data_set("..\\220408\\20408B002.tsm")')
        print('create_data(filename: str, key: str): for making a new data in a data_set)')
        print('            e.g. filename = "20408B002.tsm"  key = "Image", "FluoTrace")')
        print('set_data(filename: str, key: str, val:tuple')
        print('            e.g. test.set_data("20408B002.tsm", "Roi1", (40,40,1,1))')
        print('get_data(filename: str, key: str): to get a data valu object')
        print('            e.g. test.get_data("20408B002.tsm", "ChTrace1")')
        print('bind_data(controller, data, filename_ctrl, filename_data): bind controller and data')
        print('            e.g. test.reset_data("20408B002.tsm", "Roi1")')
        print('reset_data(filename: str, key: str): reset controller')
        print('            e.g. test.reset_data("20408B002.tsm", "Roi1")')
        print('===================================================================================')


class DataSet:
    def __init__(self, filename: object):
        self.__filename = filename
        builder_type = Translator.file_type_checker(filename)  # Using statsitc method in Translator class.
        
        self.__director = Director()  # Director makes the cartain default set of the experiments. 
        self.__builder = builder_type
        self.__director.builder = self.__builder  # Set a builder throuh the setter of Director.

        #initial deta set
        self.__director.build_initial_data_set(filename)
        
        # get dict from the builder
        objects = self.__builder.get_result()
        self.__file_io = objects[0]
        self.__data = objects[1]
        self.__controller = objects[2]
        
        self.__object_dict_list = [self.__file_io, self.__data, self.__controller]
        #self.print_infor()
        
    @property
    def data(self):
        return self.__data
    
    @property
    def controller(self):
        return self.__controller

    def set_data(self, key: str, val: tuple):
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        strategy_type.set_data(key, val)
    
    def add_data(self, key: str, val: tuple):
        return self.__controller[key].add_data(*val)

    def get_data(self, key: str) -> object:
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        return strategy_type.get_data(key)
    
    def reset_data(self, key: str):
        self.__controller[key].reset()
    
    """
    Need refactoring
    """
    def create_data(self, key: str) -> None:
        if 'Filename' in key:
            pass
            
        elif 'CellImage' in key:
            self.create_image()
                                                   
        elif 'Trace' in key:
            self.create_trace()
        
        self.print_infor()
                
    def create_image(self):
        self.__director.build_images_data_set(self.__data['ChFrames1'],
                                              self.__data['ChFrames2'])

    def create_trace(self):  # args = ch_frames
        self.__director.build_traces_data_set(self.__data['FullFrames1'],
                                              self.__data['ChFrames1'],
                                              self.__data['ChFrames2'])
            

    """
    Need refactoring
    """
        
    def print_infor(self):
        print('=================== Data keys of ' + str(self.__filename.name) + ' ====================')
        print('--- IO Keys = ' + str(list(self.__file_io.keys())))
        print('--- Data Keys = ' + str(list(self.__data.keys())))
        print('--- Controller Keys = ' + str(list(self.__controller.keys())))


"Strategy Method for set and get data"
class DataSetStrategy(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
        raise NotImplementedError()   
        
    @abstractmethod
    def get_data(self):
        raise NotImplementedError() 
     
        
class FilenameStrategy(DataSetStrategy):        
    def set_data(self, key, *args):  
        #self.__file_io[key].set_data(*args)
        raise NotImplementedError() 

    def get_data(self, key):
        #return self.__file_io[key].get_data()
        raise NotImplementedError() 

        
class DataStrategy(DataSetStrategy):   
    def __init__(self, object_dict):
        self.__object_dict = object_dict
        
    def set_data(self, key, *val):  
        self.__object_dict[key].set_data(val)

    def get_data(self, key):
        return self.__object_dict[key].get_data()
        
    
class ControllerStrategy(DataSetStrategy):
    def __init__(self, object_dict):
        self.__object_dict = object_dict

    def set_data(self, key, val):
        self.__object_dict[key].set_data(*val)
        
    def get_data(self, key):
        return self.__object_dict[key].get_data()


class ModStrategy(DataSetStrategy):
    def set_data(self, key):
        raise NotImplementedError()   
        
    def get_data(self, key):
        raise NotImplementedError() 
                   

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

    @property
    def builder(self) -> Builder:
        return self.__builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self.__builder = builder
        
    def build_initial_data_set(self, filename) -> None:
        # make file_io
        tsm = self.builder.create_file_io(TsmFileIOFactory(), filename)
        tbn = self.builder.create_file_io(TbnFileIOFactory(), filename, tsm)
        
        # get raw frames data and interval
        tsm_raw_data_tuple = copy.deepcopy(tsm.get_data())  # made indipendent from the file
        interval = copy.deepcopy(tsm.get_infor())  # made indipendent from the file
        full_interval = interval[0]
        ch_interval = interval[1]

        # make model controller
        roi = self.builder.create_controller(RoiFactory())
        frame_window = self.builder.create_controller(FrameWindowFactory())

        # make full data 
        full_frames = FramesData(tsm_raw_data_tuple[0])
        self.builder.create_data(FullFramesFactory(), full_frames, full_interval)
        full_trace = self.builder.create_data(FullTraceFactory(), full_frames, full_interval)
        roi.add_observer(full_trace)
        
        #make ch data set
        for i in range(0, tsm_raw_data_tuple[1].shape[3]):
            ch_frames = FramesData(tsm_raw_data_tuple[1][:, :, :, i])
            self.builder.create_data(ChFramesFactory(), ch_frames, ch_interval)
            image = self.builder.create_data(CellImageFactory(), ch_frames)
            trace = self.builder.create_data(ChTraceFactory(), ch_frames, ch_interval)
            #bind controller to data
            frame_window.add_observer(image)
            roi.add_observer(trace)

        #make elec traes
        elec_data = copy.deepcopy(tbn.get_data())  # made indipendent from the file
        elec_interval = copy.deepcopy(tbn.get_infor())    # made indipendent from the file
        num_elec_ch = elec_data.shape[1]

        for i in range(0, num_elec_ch):
            # Convert from raw data to a value object
            elec_trace_obj = TraceData(elec_data[:,i], elec_interval)
            # make ElecTrace
            self.builder.create_data(ChElecTraceFactory(), elec_trace_obj, elec_interval)
        
    def build_images_data_set(self, *args) -> None:
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

class Translator:
    @staticmethod
    def file_type_checker(filename):
        if filename.extension == '.tsm':
            print('Found a .tsm file')
            return TsmFileBuilder()
        elif filename.extension == '.abf':
            print('Found an .abf file')
            return AbfFileBuilder()
        elif filename.extension == '.wcp':
            print('Found a .wcp file')
            return WcpFileBuilder()
        else:
            print('--------------------------------------')
            print('Can not find any builder for this file')
            print('--------------------------------------')
            raise Exception("The file is incorrect!!!")
            
    @staticmethod
    def key_checker(key: str, object_dict_list: list):
        if 'Filename' in key:
            return FilenameStrategy(object_dict_list[0])
            
        elif 'Frames' in key or \
             'Image' in key or \
             'Trace' in key:
            return DataStrategy(object_dict_list[1])
                                                   
        elif 'Roi' in key or \
             'FrameWindow' in key:
            return ControllerStrategy(object_dict_list[2])

        elif 'Mod' in key:
            raise NotImplementedError()

        else:
            print('--------------------------------------')
            print('Can not find any Key')
            print('--------------------------------------')
            raise Exception("The key name is incorrect!!!")



"""  state method
class KeyState(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self):
        raise NotImplementedError()


class ConcreateKeyState(KeyState):
    def __init__(self, key_state):
        self.key_state = key_state
        
    def get_key_state(self):
        return self.key_state
    
    
class ImageState(ConcreateKeyState):
    def __init__(self, key_state):
        super(ImageState, self).__init__(state)
        
    def create_data(self, key_context):
        self.__director.build_images_data_set(data['ChFrames1'],
                                               data['ChFrames2'])
        
class TraceState(ConcreateKeyState):
    def __init__(self, key_state):
        super(TraceState, self).__init__(state)
        
    def create_data(self, key_context):
        self.__director.build_traces_data_set(data['FullFrames1'],
                                               data['ChFrames1'],
                                               data['ChFrames2'])


class KeyContext(object):
    def __init__(self, state_obj):
        self.key_state = state_obj
        
    def set_state(self, obj):
        self.key_state = obj
        
    def create_data(self):
        self.state.create_data(self)
            
    def get_state(self):
        return self.key_state.get_concreate_state()
    

"""

if __name__ == '__main__':
    filename1 = '..\\..\\220408\\20408B002.tsm'
    filename2 = '..\\..\\220408\\20408B001new.tsm'
    
    exp1 = Experiments()
    exp1.help()
    #make dataset
    exp1.create_data_set(filename1)
    exp1.create_data_set(filename2)
        
    # show traces

    exp1.data_set['20408B002.tsm'].data['ChTrace1'].show_data()
    exp1.data_set['20408B001new.tsm'].data['ChTrace1'].show_data()
    


    
    

