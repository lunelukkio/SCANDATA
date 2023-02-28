# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import Filename
from SCANDATA.model.builder import TsmFileBuilder, AbfFileBuilder, WcpFileBuilder, KeyCounter
from SCANDATA.model.mod_factory import ModClient
#from weakref import WeakValueDictionary


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
    def add_mod(self, key: str, mod_key: str):
        raise NotImplementedError()
        
    @abstractmethod
    def remove_mod(self, key: str, mod_key: str):
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
        self.__data_dict_list = [self.__file_io, self.__data, self.__controller]
        
        # Need refactoring for sepalate tsm information
        self.__tsm_data_context = TSMDataStrategyContext(self.__data_dict_list)
        
        # instance for mod.
        self.__mod_client = ModClient()
        
        # Initialized the data set.
        self.__builder.initialize()
        self.print_infor()
        
    def create_data(self, key: str) -> None:
        strategy_key = Translator.key_checker(key)
        self.__tsm_data_context.set_strategy(strategy_key)
        self.__tsm_data_context.create_data(self.__builder, self.__data)
        self.print_infor()

    def set_data(self, key: str, val: tuple):
        strategy_key = Translator.key_checker(key)
        self.__tsm_data_context.set_strategy(strategy_key)
        self.__tsm_data_context.set_data(key, val)

    def add_data(self, key: str, val: tuple):
        return self.__controller[key].add_data(*val)  # * unpacking val data
    
    def get_data(self, key: str) -> object:
        strategy_key = Translator.key_checker(key)
        self.__tsm_data_context.set_strategy(strategy_key)
        data = self.__tsm_data_context.get_data(key)
        if strategy_key in {'TraceStrategy', 'ImageStrategy', 'ElecStrategy'}:
            mod_key_list = self.__tsm_data_context.get_mod_key()
            data = self.__mod_client.set_mod(data, mod_key_list)
        return data

    def bind_data(self, controller_key: str, data_key: str) -> None:
        self.__controller[controller_key].add_observer(self.__data[data_key])

    def bind_view(self, controller_key: str, view_obj: object):
        self.__controller[controller_key].add_observer(view_obj)

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
    
    def add_mod(self, key: str, mod_key: str):  # add a mod to strategy class.
        strategy_key = Translator.key_checker(key)
        self.__tsm_data_context.set_strategy(strategy_key)
        self.__tsm_data_context.add_mod(mod_key)
        
    def remove_mod(self, key: str, mod_key: str):  # remove a mod from strategy class.
        strategy_key = Translator.key_checker(key)
        self.__tsm_data_context.set_strategy(strategy_key)
        self.__tsm_data_context.remove_mod(mod_key)

    def get_infor(self, key):
        strategy_key = Translator.key_checker(key)
        self.__tsm_data_context.set_strategy(strategy_key)
        infor = self.__tsm_data_context.get_infor(key)
        return infor

    @property
    def data(self):
        return self.__data

    @property
    def controller(self):
        return self.__controller

    def print_infor(self):
        print('=================== Data keys of ' + str(self.__filename.name) + ' ==================== (called by a DataSet class.create_data())')
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
class TSMDataStrategyContext:  # TMS data specific.
    def __init__(self, data_dict_list):  # data_dict_list: 1=data_io, 2=data, 3=controller
        self.data_set_strategy_dict = {}
        self.data_set_strategy_dict['FramesStrategy'] = FramesStrategy(data_dict_list)
        self.data_set_strategy_dict['ImageStrategy'] = ImageStrategy(data_dict_list)
        self.data_set_strategy_dict['TraceStrategy'] = TraceStrategy(data_dict_list)
        self.data_set_strategy_dict['ElecStrategy'] = ElecStrategy(data_dict_list)
        self.data_set_strategy_dict['RoiStrategy'] = RoiStrategy(data_dict_list)
        self.data_set_strategy_dict['FrameWindowStrategy'] = FrameWindowStrategy(data_dict_list)
        self.data_set_strategy_dict['ElecControllerStrategy'] = ElecControllerStrategy(data_dict_list)
        self.data_set_strategy_dict['ModStrategy'] = ModStrategy(data_dict_list)
        
        self.__strategy = self.data_set_strategy_dict['FramesStrategy']
        
    def set_strategy(self, strategy_key: str):
        self.__strategy = self.data_set_strategy_dict[strategy_key]
        
    def set_data(self, key, *val):
        self.__strategy.set_data(key, *val)
        
    def get_data(self, key):
        return self.__strategy.get_data(key)
        
    def create_data(self, builder, data):
        self.__strategy.create_data(builder, data)
        
    def get_infor(self, key):
        return self.__strategy.get_infor(key)
        
    def get_mod_key(self):
        return self.__strategy.get_mod_key()
        
    def add_mod(self, mod_key):
        self.__strategy.add_mod(mod_key)
        
    def remove_mod(self, mod_key):
        self.__strategy.remove_mod(mod_key)

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
        self._object_dict[2][key].set_data(*val)
        
    def get_data(self, key):
        return self._object_dict[2][key].get_data()
    
    def get_infor(self, key):
        return self._object_dict[2][key].get_infor()
    
# Not use in initializeing process
class FramesStrategy(DataStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self):
        pass


class ImageStrategy(DataStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._data defined by Translator class
        super().__init__(object_dict)
        self.__mod_list = ModList()  #delegation class
        
    def create_data(self, builder, data):
        builder.build_image_set(data)
        
    def get_data(self, key):
        return self._object_dict[1][key].get_data()
    
    def get_mod_key(self):
        return self.__mod_list.get_mod_key()
    
    def add_mod(self, key: str):
        self.__mod_list.add_mod(key)
    
    def remove_mod(self, key: str):
        self.__mod_list.remove_mod(key)


class TraceStrategy(DataStrategy):  # FluoTrace
    def __init__(self, object_dict):  # object_dict = dataset._data defined by Translator class
        super().__init__(object_dict)
        self.__mod_list = ModList()  #delegation class

    def create_data(self, builder, data):
        builder.build_trace_set(data)
        
    def get_data(self, key):
        return self._object_dict[1][key].get_data()
    
    def get_mod_key(self):
        return self.__mod_list.get_mod_key()
    
    def add_mod(self, key: str):
        self.__mod_list.add_mod(key)
    
    def remove_mod(self, key: str):
        self.__mod_list.remove_mod(key)

    
class ElecStrategy(DataStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._data defined by Translator class
        super().__init__(object_dict)
        self.__mod_list = ModList()  #delegation class
        
    def create_data(self, builder, data):
        builder.build_elec_data_set(self._object_dict[0])
        
    def get_data(self, key):
        return self._object_dict[1][key].get_data()
    
    def get_mod_key(self):
        return self.__mod_list.get_mod_key()
    
    def add_mod(self, key: str):
        self.__mod_list.add_mod(key)
    
    def remove_mod(self, key: str):
        self.__mod_list.remove_mod(key)
    
        
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
    
class ElecControllerStrategy(ControllerStrategy):
    def __init__(self, object_dict):  # object_dict = dataset._controller defined by Translator class
        super().__init__(object_dict)
        
    def create_data(self):
        pass
    
class ModList():
    def __init__(self):
        self.__mod_key_list = []  # mod keys: str
    
    def get_mod_key(self):
        return self.__mod_key_list
            
    def add_mod(self, key: str):
        for key_in_list in self.__mod_key_list:
            if key == key_in_list:
                return
        self.__mod_key_list.append(key)
        self.__mod_key_list = sorted(self.__mod_key_list)
        print('Current mod list = ' + str(self.__mod_key_list))
    
    def remove_mod(self, key: str):
        if not self.__mod_key_list:
            return
        self.__mod_key_list.remove(key)
        print('Current mod list = ' + str(self.__mod_key_list))

class ModStrategy(DataSetStrategyInterface):
    def __init__(self, data):
        self.data = data
        
    def set_data(self, key):
        raise NotImplementedError()   
        
    def get_data(self, key):
        raise NotImplementedError() 
        
    def create_data(self):
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
    def key_checker(key: str) -> str:
        print('Key Checker received a key: ' + str(key))
        
        if 'Roi' in key:
            return 'RoiStrategy'
            
        elif 'FrameWindow' in key:
            return 'FrameWindowStrategy'
        
        elif 'ElecController' in key:
            return 'ElecControllerStrategy'
            
        elif 'Frames' in key :
            return 'FramesStrategy'
        
        elif 'Image' in key:
            return 'ImageStrategy'

        elif 'Trace' in key:  # Trace should be fluo trace
            return 'TraceStrategy'

        elif 'Elec' in key:  # Elec should be elec trace
            return 'ElecStrategy'

        elif 'Mod' in key:
            return 'ModStrategy'
            
        elif 'Newkey' in key:
            raise NotImplementedError()
            
        else:
            print('--------------------------------------')
            print('Can not find any Key: ' + key)
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
    


    
    

