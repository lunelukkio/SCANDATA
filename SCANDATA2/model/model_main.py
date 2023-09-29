# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:11:15 2023

@author: lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA2.model.value_object import WholeFilename
from SCANDATA2.model.experiments import Experiments
from SCANDATA2.model.user_controller import RoiFactory, FrameWindow, FrameShift, Line
import re
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
        
    @abstractmethod
    def create_user_controller(self, controller_key):
        raise NotImplementedError()
     
    @abstractmethod
    def resister_filename2controller(self, controller_key, filename_str):
        raise NotImplementedError()
        
    @abstractmethod
    def get_experiments(self, key):  # return whole data_dict in experiments
        raise NotImplementedError()
    
    @abstractmethod
    def get_user_controller(self, key):
        raise NotImplementedError()
        
    @abstractmethod
    def delete_experiments(self, key):
        raise NotImplementedError()

    @abstractmethod
    def delete_user_controller(self, key):
        raise NotImplementedError()
        
class DataService(ModelInterface):
    def __init__(self):
        self.__experiments_repository = ExperimentsRepository()
        self.__user_controller_repository = UserControllerRepository()
        
    def __create_filename_obj(self, fullname):
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_model(self, fullname):
        # make a filename value obj from fullname
        filename_obj = self.__create_filename_obj(fullname)
        # make a data entity
        experiments = Experiments(filename_obj)
        # save entity to the repository
        self.__experiments_repository.save(filename_obj.name,
                                                        experiments)
        print(f"Current experiments data = {list(self.__experiments_repository.data.keys())}")
 
    def create_user_controller(self, controller_key):  # controller_key = "Roi", "TimeWindow"
        controller_factory = self.__check_controller_type(controller_key)   # get a controller factory 
        new_controller = controller_factory.create_controller(self.get_experiments)  # make a new controller

        # save to the repository
        new_key = self.__key_num_checker(self.__user_controller_repository.data)
        if new_key is None:
            new_key = controller_key.upper() + "1"
        self.__user_controller_repository.save(new_key, new_controller)
        
    def resister_filename2controller(self, controller_key, filename_str):
        self.__user_controller_repository.data[controller_key.upper()].add_experiments(filename_str)
    
    def get_experiments(self, key):  # return whole data_dict in experiments
        return self.__experiments_repository.data[key]

    def get_user_controller(self, key):
        return self.__user_controller_repository.data[key.upper()]
    
    def delete_experiments(self, key):
        self.__experiments_repository.delete(key.upper())
        
    def delete_user_controller(self, key):
        self.__user_controller_repository.delete(key.upper())
    
    def print_infor(self):
        print(f"Current experiments data = {list(self.__experiments_repository.data.keys())}")
        print(f"Current user controllers = {list(self.__user_controller_repository.data.keys())}")
        

    def __check_controller_type(self, key):
        if key.upper() == "ROI":
            return RoiFactory()
        elif key.upper() == "FRAMEWINDOW":
            return FrameWindow()
        elif key.upper() == "FRAMESSHIFT":
            return FrameShift()
        elif key.upper() == "LINE":
            return Line()
        
    def __key_num_checker(self, controller_dict):
        if not bool(controller_dict):
            print("dict is empty.")
            return None
        numeric_keys = [key for key in controller_dict.keys() if any(char.isdigit() for char in key)]
        numeric_values = [int(''.join(filter(str.isdigit, key))) for key in numeric_keys]

        # sort from a small number
        sorted_keys = [x for _, x in sorted(zip(numeric_values, numeric_keys))]

        # find unexsisting number
        min_missing_number = None
        for i in range(1, len(sorted_keys) + 2):
            if i not in numeric_values:
                min_missing_number = i
                break
            
        # new key
        prefix = re.sub(r'\d+', '', numeric_keys[0])
        new_key = prefix + str(min_missing_number)
        return new_key



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
        entity = self.__data[key]
        if entity is None:
            raise Exception(f"There is no {key}")
        print(f"Return the key = {key}" )
        return entity

    def delete(self, key: str):
        self.__data.pop(key)
        
    @property
    def data(self):
        return self.__data

        
class UserControllerRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    
    def save(self, key: str, data):
        self.__data[key] = data
        
    def find_by_name(self, key: str):
        entity = self.__data[key]
        if entity is None:
            raise Exception(f"There is no {key}")
        print(f"Return the key = {key}" )
        return entity
    
    def delete(self, key: str):
        self.__data.pop(key)
        
    @property
    def data(self):
        return self.__data


class ModRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    


    