# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

"""

from abc import ABCMeta, abstractmethod
from weakref import WeakValueDictionary
from SCANDATA.model.value_object import Filename
from SCANDATA.model.builder import TsmFileBuilder, AbfFileBuilder, WcpFileBuilder, KeyCounter
#from SCANDATA.model.mod_factory import ModTrace


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
    def delete_entity(self, filename: str, key: str):
        raise NotImplementedError()
        
    @abstractmethod
    def data_set(self):  # get a list of data_set objects (dict of filenames)
        raise NotImplementedError()
        
    @abstractmethod
    def count_data(self, filename: str, key: str):
        raise NotImplementedError()

class Experiments(ExperimentsInterface):
    def __init__(self):
        self.__data_set = {}
    
    def create_data_set(self, fullname: str):  # create a whole data set(frame, image, trace) 
        filename = Filename(fullname)
        
        self.__data_set[filename.name] = DataSet(filename)  # dict of data_file(key filename : object)
        print('Created {} data set.'.format(filename.name))
        
    def create_data(self, filename, key: str, *args):
        self.__data_set[filename].create_data(key)
            
    def set_data(self, filename: str, key: str, val: tuple):
        self.__data_set[filename].set_data(key, val)
        
    def add_data(self, filename: str, key: str, val: tuple):
        self.__data_set[filename].add_data(key, val)
        
    def get_data(self, filename: str, key: str):
        return self.__data_set[filename].get_data(key)
    
    def bind_data(self, controller: str, data: str, filename_ctrl: str, filename_data: str):
        binding_controller = self.__data_set[filename_ctrl].controller[controller]
        binding_key = self.__data_set[filename_data].data[data]
        binding_controller.add_observer(binding_key)

    def reset_data(self, filename: str, key: str):
        self.__data_set[filename].reset_data(key)
        
    def delete_entity(self, filename, key):
        self.__data_set[filename].delete_entity(key)

    @property
    def data_set(self):
        return self.__data_set
    
    def count_data(self, filename: str, key: str):
        num = self.__data_set[filename].count_data(key)
        return num
        
        
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
        self.__builder = Translator.file_type_checker(filename)  # Using statsitc method in Translator class.

        # Reset a data set.
        (self.__file_io, self.__data, self.__controller) = self.__builder.reset()
        
        # This list is for strategy_types
        self.__object_dict_list = [self.__file_io, self.__data, self.__controller]
        
        # Initialized the data set.
        self.__builder.initialize()

        self.print_infor()

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
        data = strategy_type.get_data(key)
        #mod_trace = mod_data(raw_trace)
        return data

    def reset_data(self, key: str):
        self.__controller[key].reset()

    def create_data(self, key: str) -> None:
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        strategy_type.create_data(self.__builder, self.__data)
        self.print_infor()
        
    def delete_entity(self, key: str) -> None:
        if key in self.__data:
            del self.__data[key]
            print('Deleted ' + key + 'from data')
        elif key in self.__controller:
            del self.__controller[key]
            print('Deleted ' + key + ' from controller')
        else:
            print('====================================')
            print('No key. Can not delet ' + key)
            print('====================================')
            
    def count_data(self, key):
        num = KeyCounter.count_key(self.data, key)
        return num

    def print_infor(self):
        print('=================== Data keys of ' + str(self.__filename.name) + ' ====================')
        print('--- IO Keys = ' + str(list(self.__file_io.keys())))
        print('--- Data Keys = ' + str(list(self.__data.keys())))
        print('--- Controller Keys = ' + str(list(self.__controller.keys())))



"""
Strategy Method for set and get data
"""
class DataSetStrategy(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
        raise NotImplementedError()   
        
    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
        
    @abstractmethod   
    def create_data(self):
        raise NotImplementedError() 
     
        
class FilenameStrategy(DataSetStrategy):        
    def set_data(self, key, *args):  
        #self.__file_io[key].set_data(*args)
        raise Exception('Filename cant be changed')

    def get_data(self, key):
        raise NotImplementedError()   # Shold it be filename?

    def create_data(self):
        raise Exception('Filename shold be only one in a data-set as its name.')

        
class DataStrategy(DataSetStrategy):   
    def __init__(self, object_dict):
        self._object_dict = object_dict
        
    def set_data(self, key, *val):  
        self._object_dict[key].set_data(val)

    def get_data(self, key):  # overrided by childern classes
        return self._object_dict[key].get_data()
    
    
class ControllerStrategy(DataSetStrategy):
    def __init__(self, object_dict):
        self._object_dict = object_dict

    def set_data(self, key, val):
        self._object_dict[key].set_data(*val)
        
    def get_data(self, key):
        return self._object_dict[key].get_data()


class FramesStrategy(DataStrategy):
    def __init__(self, object_dict, builder):
        super().__init__(object_dict, builder)
        
    def create_data(self):
        pass


class ImageStrategy(DataStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self, builder, data):
        builder.build_image_set(data)


class TraceStrategy(DataStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self, builder, data):
        builder.build_trace_set(data)
        
    def get_data(self, key):
        return self._object_dict[key].get_data()
    
        
class RoiStrategy(ControllerStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self):
        pass
        
        
class FrameWindowStrategy(ControllerStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self):
        pass


class ModStrategy(DataSetStrategy):
    def set_data(self, key):
        raise NotImplementedError()   
        
    def get_data(self, key):
        raise NotImplementedError() 
                   

class Translator:
    @staticmethod
    def file_type_checker(filename):
        if filename.extension == '.tsm':
            print('Found a .tsm file')
            return TsmFileBuilder(filename)
        elif filename.extension == '.abf':
            print('Found an .abf file')
            return AbfFileBuilder(filename)
        elif filename.extension == '.wcp':
            print('Found a .wcp file')
            return WcpFileBuilder(filename)
        else:
            print('--------------------------------------')
            print('Can not find any builder for this file')
            print('--------------------------------------')
            raise Exception("The file is incorrect!!!")
            
    @staticmethod
    def key_checker(key: str, object_dict_list: list) -> object:  # [file_io, self.__data, self.__controller]  
        if 'Filename' in key:
            return FilenameStrategy(object_dict_list[0])
            
        elif 'Frames' in key :
            return FramesStrategy(object_dict_list[1])
        
        elif 'Image' in key:
            return ImageStrategy(object_dict_list[1])

        elif 'Trace' in key:
            return TraceStrategy(object_dict_list[1])
                                                   
        elif 'Roi' in key:
            return RoiStrategy(object_dict_list[2])
            
        elif 'FrameWindow' in key:
            return FrameWindowStrategy(object_dict_list[2])

        elif 'Newkey' in key:
            raise NotImplementedError()
            
        else:
            print('--------------------------------------')
            print('Can not find any Key')
            print('--------------------------------------')
            raise Exception("The key name is incorrect!!!")




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
    


    
    

