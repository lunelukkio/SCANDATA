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


class DataSetInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self, key, *args):
        raise NotImplementedError()
        
    @abstractmethod
    def set_data(self, key: str, val: tuple):
        raise NotImplementedError()
        
    @abstractmethod
    def add_data(self, key: str):
        raise NotImplementedError()
        
    @abstractmethod
    def get_data(self, key: str):
        raise NotImplementedError()
        
    def bind_data(self, controller_key: str, data_key: str):
        raise NotImplementedError()
        
    def bind_view(self, data_key: str, view_obj: object):
        raise NotImplementedError()
    
    @abstractmethod
    def reset_data(self, key: str):
        raise NotImplementedError()
     
    @abstractmethod
    def delete_entity(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def count_data(self, key: str):
        raise NotImplementedError()
        
    @abstractmethod
    def get_infor(self,  key: str):
        raise NotImplementedError()
        
        
class DataSet(DataSetInterface):
    def __init__(self, full_filename: str):
        self.__filename = Filename(full_filename)
        self.__builder = Translator.file_type_checker(self.__filename)  # Using statsitc method in Translator class.

        # Reset a data set.
        (self.__file_io, self.__data, self.__controller) = self.__builder.reset()
        
        # This list is for strategy_types
        self.__object_dict_list = [self.__file_io, self.__data, self.__controller]
        
        # Initialized the data set.
        self.__builder.initialize()
        self.print_infor()

    def create_data(self, key: str) -> None:
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        strategy_type.create_data(self.__builder, self.__data)
        self.print_infor()

    def set_data(self, key: str, val: tuple):
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        strategy_type.set_data(key, val)

    def add_data(self, key: str, val: tuple):
        return self.__controller[key].add_data(*val)
    
    def get_data(self, key: str) -> object:
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        data = strategy_type.get_data(key)
        # decorator.(write in strategy, because decoration is not the same in each data and controller)
        #mod_trace = mod_data(raw_trace)
        return data

    def bind_data(self, controller_key: str, data_key: str) -> None:
        self.__controller[controller_key].add_observer(self.__data[data_key])

    def bind_view(self, data_key: str, view_obj: object):
        self.__data[data_key].observer.add_observer(view_obj)

    def reset_data(self, key: str):
        self.__controller[key].reset()

    def delete_entity(self, key: str) -> None:
        if key in self.__data:
            del self.__data[key]
            print('Deleted ' + key + 'from data')
        elif key in self.__controller:
            del self.__controller[key]
            print('Deleted ' + key + ' from controller')
        else:
            print('====================================')
            print('No key. Can not delete ' + key)
            print('====================================')

    def count_data(self, key):
        num = KeyCounter.count_key(self.data, key)
        return num

    def get_infor(self, key):
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        infor = strategy_type.get_infor(key)
        return infor

    @property
    def data(self):
        return self.__data

    @property
    def controller(self):
        return self.__controller

    def print_infor(self):
        print('=================== Data keys of ' + str(self.__filename.name) + ' ====================')
        print('--- IO Keys = ' + str(list(self.__file_io.keys())))
        print('--- Data Keys = ' + str(list(self.__data.keys())))
        print('--- Controller Keys = ' + str(list(self.__controller.keys())))

    def help(self):
        print('===================================================================================')
        print('HELP for commands to MODEL')
        print('DataSet(filename)     <------------ only this is full file name.')
        print('            e.g. new_data_set = DataSet("..\\220408\\20408B002.tsm")')
        print('create_data(key: str): for making a new data in a data_set)')
        print('            e.g. key = "Image" or "FullTrace")')
        print('set_data(key: str, val:tuple')
        print('            e.g. test.set_data("Roi1", (40,40,1,1))')
        print('get_data(key: str): to get a data entity')
        print('            e.g. test.get_data("ChTrace1")')
        print('bind_data(controller_key, data_key): bind controller and data')
        print('            e.g. test.bind_data("Roi1", "ChTrace1")')
        print('reset_data(key: str): reset controller')
        print('            e.g. test.reset_data("Roi1")')
        print('===================================================================================')

"""
Strategy Method for set and get data
"""
class DataSetStrategyInterface(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
        raise NotImplementedError()   
        
    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
        
    @abstractmethod   
    def create_data(self):
        raise NotImplementedError() 
        
    @abstractmethod  
    def get_infor(self):
        raise NotImplementedError() 
     
        
class FilenameStrategy(DataSetStrategyInterface):        
    def set_data(self, key, *args):  
        #self.__file_io[key].set_data(*args)
        raise Exception('Filename cant be changed')

    def get_data(self, key):
        raise NotImplementedError()   # Shold it be filename?

    def create_data(self):
        raise Exception('Filename shold be only one in a data-set as its name.')
        
    def get_infor(self):
        pass

        
class DataStrategy(DataSetStrategyInterface):   
    def __init__(self, object_dict):  # object_dict = dataset._data defined by Translator class
        self._object_dict = object_dict
        
    def set_data(self, key, *val):  
        self._object_dict[key].set_data(val)

    def get_data(self, key):  # overrided by childern classes
        return self._object_dict[key].get_data()
    
    def get_infor(self, key):
        return self._ogject_dict[key].get_infor()
    
    
class ControllerStrategy(DataSetStrategyInterface):
    def __init__(self, object_dict):  # object_dict = dataset._controller defined by Translator class
        self._object_dict = object_dict

    def set_data(self, key, val):
        self._object_dict[key].set_data(*val)
        
    def get_data(self, key):
        return self._object_dict[key].get_data()
    
    def get_infor(self, key):
        return self._object_dict[key].get_infor()
    

class FramesStrategy(DataStrategy):
    def __init__(self, object_dict, builder):
        super().__init__(object_dict, builder)
        
    def create_data(self):
        pass


class ImageStrategy(DataStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._data defined by Translator class
        super().__init__(object_dict)
        
    def create_data(self, builder, data):
        builder.build_image_set(data)


class TraceStrategy(DataStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._data defined by Translator class
        super().__init__(object_dict)
        
    def create_data(self, builder, data):
        builder.build_trace_set(data)
        
    def get_data(self, key):
        return self._object_dict[key].get_data()
    
        
class RoiStrategy(ControllerStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._controller defined by Translator class
        super().__init__(object_dict)
        
    def create_data(self, builder, data_set):
        pass
        
class FrameWindowStrategy(ControllerStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._controller defined by Translator class
        super().__init__(object_dict)
        
    def create_data(self):
        pass


class ModStrategy(DataSetStrategyInterface):
    def set_data(self, key):
        raise NotImplementedError()   
        
    def get_data(self, key):
        raise NotImplementedError() 
        
    def get_infor(self, key):
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

    filename1 = Filename('..\\220408\\20408B001.tsm')
    filename2 = Filename('..\\220408\\20408B002.tsm')
    #make dataset
    exp1 = DataSet(filename1)
    exp2 = DataSet(filename2)
    exp1.help()
        
    # show traces

    exp1.data['ChTrace1'].show_data()
    exp1.data['ChTrace1'].show_data()
    


    
    

