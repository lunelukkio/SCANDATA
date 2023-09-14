# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:11:15 2023

@author: lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA2.model.value_object import WholeFilename
from SCANDATA2.model.file_io import TsmFileIo
#import inspect
#from SCANDATA.model.mod_factory import ModClient
#from weakref import WeakValueDictionary

"""
Service
"""
class ModelInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_filename_obj(self, fullname):
        raise NotImplementedError()
    
    @abstractmethod
    def create_model(self, fullname):
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
    
    @abstractmethod
    def bind_data(self, controller_key: str, data_key: str):
        raise NotImplementedError()
    
    @abstractmethod
    def bind_view(self, data_key: str, view_obj: object):
        raise NotImplementedError()
        
    @abstractmethod
    def update_data(self, key):
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
        
        
class DataService(ModelInterface):
    def __init__(self):
        experiments_repository = ExperimentsRepository()
        user_controller_repository = UserControllerRepository()
        mod_repository = ModRepository()
        self.__repository = {"ExperimentsRepository":experiments_repository,
                             "UserContoller":user_controller_repository,
                             "ModCOntoller":mod_repository}
        
    def create_filename_obj(self, fullname):
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_model(self, fullname):
        # make a filename value obj from fullname
        filename_obj = self.create_filename_obj(fullname)
        # make a data entity
        experiments = Experiments(filename_obj)
        # save entity to the repository
        self.__repository["ExperimentsRespoitory"].save(filename_obj.filenmae,
                                                        experiments)
        
        
        
"""
Entity
"""
class Experiments:   # entity
    def __init__(self, filename_obj):
        self.filename_obj = filename_obj
        # create default data set.
        builder_factory = self.factory_selector(self.filename_obj)
        self.builder = builder_factory.create_builder()

        self.txt_data = None   # str???
        self.frame_dict = self.builder.get_frame()   # {type:data}
        self.image_dict = {}
        self.trace_dict = {}
        
        
        
        self.__observer = ExperimentsObserver()
    
    def factory_selector(self, filename_obj):
        if filename_obj.extension == ".tsm":
            return TsmBuilderFactory
        elif filename_obj.extension == ".da":
            raise NotImplementedError()
        else:
            raise Exception("This file is an undefineded file!!!")
            
    def get_data_type(self, dict_type):   # dict_type = txt_data, frame_dict...
        key_list = list(dict_type.keys())
        return key_list
    

# need refactoring(2023/09/13)
class ExperimentsObserver:
    def __init__(self):
        self.__observers = []
        
    def add_observer(self, observer):
        for check_observer in self.__observers:
            if check_observer == observer:
                self.remove_observer(observer)
                return
        self.__observers.append(observer)
        self.__observers = sorted(self.__observers, key=lambda x: str(x.sort_num)+x.name)

    def remove_observer(self, observer):
        self.__observers.remove(observer)
        name_list = []
        for i in self.__observers:
            name_list.append(i.name)
            
    def notify_observer(self, controller_obj):
        name_list = []
        for observer in self.__observers:
            name_list.append(observer.name)
        print('----- Notify to observers: ' + str(name_list))
        """ The order of ViewDatas should be after Data entiries """
        for observer_name in self.__observers:
            observer_name.update(controller_obj.data)
            
    def get_infor(self):
        name_list = []
        for observer in self.__observers:
            name_list.append(observer.name)
        return name_list

    @property
    def observers(self) -> list:
        return self.__observers



"""
Repository
"""
class RepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def save(self, key: str, data):
        raise NotImplementedError()
        
    @abstractmethod
    def find(self, key: str):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, key: str):
        raise NotImplementedError()
        
    
class ExperimentsRepository(RepositoryInterface):
    def __init__(self):
        self.data = {}   # {key:entiry}
    
    def save(self, key: str, data):
        self.data[key] = data
        
    def find(self, key: str):
        raise NotImplementedError()
    
    def delete(self, key: str):
        raise NotImplementedError()
    
class UserControllerRepository(RepositoryInterface):

    def save(self, data, key: str):
        raise NotImplementedError()
        
    def find(self, key: str):
        raise NotImplementedError()
    
    def delete(self, key: str):
        raise NotImplementedError()
    
class ModRepository(RepositoryInterface):
    def save(self, data, key: str):
        raise NotImplementedError()
        
    def find(self, key: str):
        raise NotImplementedError()
    
    def delete(self, key: str):
        raise NotImplementedError()
    
    
"""
Builder
"""
class BuilderFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_builder(filename_obj):
        raise NotImplementedError()


class TsmBuilderFactory(BuilderFactory):
    def create_builder(filename_obj):
        return TsmBuilder(filename_obj)





class Builder(metaclass=ABCMeta):
    @abstractmethod
    def get_infor(self, filename_obj) -> None:
        raise NotImplementedError()    

    @abstractmethod
    def get_frame(self, filename_obj) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def get_image(self, filename_obj) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def get_trace(self, filename_obj) -> None:
        raise NotImplementedError()


class TsmBuilder(Builder):
    def __init__(self, filename_obj):
        num_ch = 2   # this is for Na+ and Ca2+ recording.
        file_io = TsmFileIo(filename_obj, num_ch)
        
        # get and set data from files
        self.data_infor = file_io.get_infor
        self.frames = file_io.get_3d
        self.elec_data = file_io.get_1d
        
        file_io.print_data_infor()
        
        del file_io   # release the io object to allow file changes during recording.
        
    def get_infor(self):
        return self.data_infor
        
    def get_frame(self):
        return {"Full": self.frames[0],
                "Ch1": self.frames[1], 
                "Ch2": self.frame[2]}

    def get_image(self):
        return None
    
    def get_trace(self):
        return {"Elc_ch1": self.elec_data[0], 
                "Elc_ch2": self.elec_data[1], 
                "Elc_ch3": self.elec_data[2],
                "Elc_ch4": self.elec_data[3],
                "Elc_ch5": self.elec_data[4],
                "Elc_ch6": self.elec_data[5],
                "Elc_ch7": self.elec_data[6],
                "Elc_ch8": self.elec_data[7]}