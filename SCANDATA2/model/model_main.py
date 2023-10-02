# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:11:15 2023

@author: lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA2.common_class import WholeFilename
from SCANDATA2.model.experiments import Experiments
from SCANDATA2.model.user_controller import RoiFactory, ImageControllerFactory

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
    def bind_filename2controller(self, filename_key, controller_key):
        raise NotImplementedError()
        
    @abstractmethod
    def set_controller(self, controller_key: str, val: list):
        raise NotImplementedError()
        
    @abstractmethod
    def get_experiments(self, key) -> object:  # return whole data_dict in experiments
        raise NotImplementedError()
    
    @abstractmethod
    def get_user_controller(self, key) -> object:
        raise NotImplementedError()
        
    @abstractmethod
    def reset(self, controller_key):
        raise NotImplementedError() 
        
        
class DataService(ModelInterface):
    def __init__(self):
        self.__experiments_repository = ExperimentsRepository()
        self.__user_controller_repository = UserControllerRepository()
        
    def __create_filename_obj(self, fullname):
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_model(self, fullname): #Use the same name to delete a model
        # make a filename value obj from fullname
        filename_obj = self.__create_filename_obj(fullname)
        if self.__experiments_repository.find_by_name(filename_obj.name) is None:
            # make a data entity
            experiments = Experiments(filename_obj)
            # save entity to the repository
            print("====================Created the new expriments!!!")
            self.__experiments_repository.save(filename_obj.name, experiments)
            self.print_infor()
        else:
            # delete a model
            self.__experiments_repository.delete(filename_obj.name)
 
    def create_user_controller(self, controller_key):  # controller_key = "Roi", "TimeWindow". Use the same name to delete like "ROI1"
        controller_key = controller_key.upper()
        if self.__user_controller_repository.find_by_name(controller_key) is None:
            # get a controller factory 
            controller_factory = self.__check_controller_type(controller_key)
            # make a new controller with the method in DataService
            new_controller = controller_factory.create_controller(self.get_experiments)
            # save to the repository
            new_key = self.__key_num_maker(controller_key)
            print(f"====================Created the new controller {controller_key}")
            self.__user_controller_repository.save(new_key, new_controller)
            self.print_infor()
        else:
            self.__user_controller_repository.delete(controller_key)
        
    def bind_filename2controller(self, filename_key, controller_key):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        print(f"Add {filename_key} to {controller_key}")
        controller.add_experiments(filename_key)

    def set_controller(self, controller_key: str, val: list):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_controller(val)
    
    def get_experiments(self, key):  # return whole data_dict in experiments
        return self.__experiments_repository.data[key]

    def get_user_controller(self, controller_key):
        controller_key = controller_key.upper()
        return self.__user_controller_repository.data[controller_key]
    
    def reset(self, controller_key):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.reset()
        print(f"Reset: {controller_key}")
    
    def print_infor(self):
        print("DataService information ===========================")
        print(f"Current experiments data = {list(self.__experiments_repository.data.keys())}")
        print(f"Current user controllers = {list(self.__user_controller_repository.data.keys())}")
        print("======================= DataService information END")

    def __check_controller_type(self, key):
        if key == "ROI":
            return RoiFactory()
        elif key == "IMAGECONTROLLER":
            return ImageControllerFactory()

        # To make a number for controller key.
    def __key_num_maker(self, controller_key):
        controller_key = controller_key.upper()
        controller_dict = self.__user_controller_repository.data
        count = 0
        for key in controller_dict.keys():
            if controller_key in key:
                count += 1
        
        if count == 0:
            new_key = controller_key + "1"
        else:
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
            new_key = controller_key + str(min_missing_number)
        return new_key
    
    def help(self):
        
        print("==================== Help ======================")
        print("The first step: make a experiments model. ex.model.create_model(filename_obj.fullname)")
        print("The second step: make a user_controller. ex.model.create_controller(\"ROI\")")
        print("The third step: bind experiments to user_controller. ex.model.bind_filename2controller(\"20408B002.tsm\", \"Roi1\")")
        print("The last step: get data from a user_controller. ex. roi1 = model.get_user_controller(\"20408B002.tsm\", \"ROI1\")")
        



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
        print(f"Saved {key} experiments in the experiments repository.")
        
    def find_by_name(self, key: str):
        if key in self.__data:
            print(f"Found {key} experiments in the experiments repository.")
            return self.__data[key]
        else:
            print(f"There is no {key} experiments in the experiments repository.")
            return None

    def delete(self, key: str):
        self.__data.pop(key)
        print(f"Deleted {key} experiments from the experiments repository.")
        
    @property
    def data(self):
        return self.__data

        
class UserControllerRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    
    def save(self, key: str, data):
        self.__data[key] = data
        print(f"Saved {key} controller in the user controller repository.")
        
    def find_by_name(self, key: str):
        if key in self.__data:
            return self.__data[key]
        else:
            print(f"There is no {key} controller in the user repository")
            return None
    
    def delete(self, key: str):
        self.__data.pop(key)
        print(f"Deleted {key} controller from the user controller repository.")
        
    @property
    def data(self):
        return self.__data


class ModRepository(RepositoryInterface):
    def __init__(self):
        self.__data = {}   # {key:entiry}
    


    