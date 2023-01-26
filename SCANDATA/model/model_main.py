# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

"""

from abc import ABCMeta, abstractmethod
from weakref import WeakValueDictionary
from SCANDATA.model.value_object import Filename
from SCANDATA.model.builder import TsmFileBuilder, AbfFileBuilder, WcpFileBuilder
from SCANDATA.model.builder import Director
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
    def data_set(self):  # get a list of data_set objects
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
        return strategy_type.get_data(key)

    def reset_data(self, key: str):
        self.__controller[key].reset()

    def create_data(self, key: str) -> None:
        strategy_type = Translator.key_checker(key, self.__object_dict_list)
        strategy_type.create_data(self.__director, self.__data)
        self.print_infor()

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
    def __init__(self, object_dict, director):
        super().__init__(object_dict, director)
        
    "Can it replace director methods???"
    def create_data(self):
        pass


class ImageStrategy(DataStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self, director, data):
        director.build_images_data_set(data)


class TraceStrategy(DataStrategy):
    def __init__(self, object_dict):
        super().__init__(object_dict)
        
    def create_data(self, director, data):
        director.build_traces_data_set(data)
        
    def get_data(self, key):
        return self._object_dict[key].get_data()
        #mod_trace = mod_data(raw_trace)
        "Tip 誰かがModdict{}を保持してfor 文でModをchain of responsibilityに入れ回す mod dictにはそれぞれt trace image frames用が必要"
        "Tip 管理はmoddicのオブジェを抜き差しでする"
        
        
        
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
    


    
    

