# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:11:15 2023

@author: lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA2.model.value_object import WholeFilename
from SCANDATA2.model.user_controller import RoiFactory, FrameWindow, FrameShift, Line
#import inspect
#from SCANDATA.model.mod_factory import ModClient
#from weakref import WeakValueDictionary

"""
Service
"""
class ModelInterface(metaclass=ABCMeta):   
    @abstractmethod
    def create_model(self, fullname):
        raise NotImplementedError()
        
        
    """    
        
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
    """
    
        
class DataService(ModelInterface):
    def __init__(self):
        experiments_repository = ExperimentsRepository()
        user_controller_repository = UserControllerRepository()
        mod_repository = ModRepository()
        self.repository = {"ExperimentsRepository":experiments_repository,
                             "UserContoller":user_controller_repository,
                             "ModCOntoller":mod_repository}
        
    def __create_filename_obj(self, fullname):
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_model(self, fullname):
        # make a filename value obj from fullname
        filename_obj = self.__create_filename_obj(fullname)
        # make a data entity
        experiments = Experiments(filename_obj)
        # save entity to the repository
        self.repository["ExperimentsRepository"].save(filename_obj.name,
                                                        experiments)
        # make user controller
        self.make_user_controller(filename_obj)
        
    def make_user_controller(self, filename_obj, controller_key):
        controller_factory = self.__check_controller_type(controller_key)   # get a controller factory 
        new_controller = controller_factory.create_controller(self, filename_obj)  # make a new controller
        # save to the repository
          #self.repository["UserContoller"].save("key???", new_controller)
        return
    
    # This shold be used by a frontend or user controllers.
    def get_data(self, key):  # return whole data_dict in experiments
        experiments_entity = self.__find_by_key(key)
        if experiments_entity is None:
            raise Exception(f"There is no {key}")
        data_dict = experiments_entity.get_data()
        print(f"Return the key = {key}" )
        return data_dict

    def bind_user_controller(self):
        pass
    
    def repository_key_list(self):
        pass
        

    def __find_by_key(self, key) -> object:   # return experiments entity by key
        if key in list(self.repository["ExperimentsRepository"].data.keys()):
            print(f"The key = {key} is in ExperimentsRepository")
            return self.repository["ExperimentsRepository"].data[key]
        elif key in list(self.repository["UserControllerRepositor"].data.keys()):
            print(f"The key = {key} is in UserControllerRepositor")
            return self.repository["UserControllerRepositor"].data[key]
        elif key in list(self.repository["ModRepository"].data.keys()):
            print(f"The key = {key} is in ModRepository")
            return self.repository["ModRepository"].data[key]
        else:
            raise Exception(f"There is no {key}")
            
    def __check_controller_type(self, key):
        if key == "ROI":
            return RoiFactory()
        elif key == "FrameWindow":
            return FrameWindow()
        elif key == "FrameShift":
            return FrameShift()
        elif key == "Line":
            return Line()

        
 

"""
Repository
"""
class RepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def save(self, key: str, data):
        raise NotImplementedError()
        
    @abstractmethod
    def find_by_name(self, key: str):
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, key: str):
        raise NotImplementedError()
        
        
    
class ExperimentsRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    
    def save(self, key: str, data):
        self.__data[key] = data
        
    def find_by_name(self, key: str):
        return self.__data[key]
    
    def delete(self, key: str):
        del self.__data[key]
        
    @property
    def data(self) -> dict:
        return self.__data
        
    
class UserControllerRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    
    def save(self, key: str, data):
        self.__data[key] = data
        
    def find_by_name(self, key: str):
        return self.__data[key]
    
    def delete(self, key: str):
        del self.__data[key]
        
    @property
    def data(self) -> dict:
        return self.__data
    
class ModRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    
    def save(self, key: str, data):
        self.__data[key] = data
        
    def find_by_name(self, key: str):
        return self.__data[key]
    
    def delete(self, key: str):
        del self.__data[key]
        
    @property
    def data(self) -> dict:
        return self.__data
    
    