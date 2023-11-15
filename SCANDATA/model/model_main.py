# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:11:15 2023

@author: lunelukkio@gmail.com
When new controllers are added, import from "user controller" factory and __check_controller_type in DataService also should be modified.

"""
from abc import ABCMeta, abstractmethod
from SCANDATA.common_class import WholeFilename
from SCANDATA.model.experiments import Experiments
from SCANDATA.model.user_controller import RoiFactory, ImageControllerFactory, TraceControllerFactory
from SCANDATA.model.mod.mod_main import ModService

"""
Service
"""
class ModelInterface(metaclass=ABCMeta):   
    @abstractmethod
    def create_experiments(self, fullname):  # create epxeriments entity in the repository with filename.
        raise NotImplementedError()
        
    @abstractmethod
    def create_user_controller(self, controller_key) -> str:  # make a new value of data.
        raise NotImplementedError()
     
    @abstractmethod
    def bind_filename2controller(self, filename_key, controller_key):  # connect between the controller and experiments entities.
        raise NotImplementedError()

    @abstractmethod
    def set_experiments(self, controller_key:str, filename_key:str):  # make a new data from experiments entities into the controllers.
        raise NotImplementedError()
        
    @abstractmethod
    def set_controller_val(self, controller_key: str, val: list):  # set a new controller value.
        raise NotImplementedError()
        
    @abstractmethod
    def get_controller_val(self, key) -> object:  # value object ex RoiVal. It is used by controllers for chaning the size of ROI.
        raise NotImplementedError()
        
    @abstractmethod
    def set_observer(self, observer:object):  # set an axis observer of view into controller 
        raise NotImplementedError()
        
    @abstractmethod
    def get_controller_data(self, controller_key: str):  # return a dict of controller including value objects.
        raise NotImplementedError()
        
    @abstractmethod
    def get_experiments(self, key) -> object:  # return whole data_dict in experiments. It is used by user_controllers.
        raise NotImplementedError()
        
    @abstractmethod
    def set_mod_val(self, key) -> None:  # set background controller to the mod class.
        raise NotImplementedError()
        
    @abstractmethod
    def set_mod_key(self, key) -> None:  # set background controller to the mod class.
        raise NotImplementedError()    
        

    @abstractmethod
    def reset(self, controller_key):
        raise NotImplementedError() 
        
    @abstractmethod
    def help(self):
        raise NotImplementedError() 
        
        
class DataService(ModelInterface):
    def __init__(self):
        self.__experiments_repository = ExperimentsRepository()
        self.__user_controller_repository = UserControllerRepository()
        self.__mod_service = ModService(self.get_controller_data)  # send it to enable to use this method from mod class
        self.__mod_switch = True
        print("DataService.current_filename: Need refactoring for removing filename from controller. filename should be selected by dataService.")
        self.__current_filename = True
        
    def __create_filename_obj(self, fullname):
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_experiments(self, fullname): #Use the same name to delete a model
        # make a filename value obj from fullname
        filename_obj = self.__create_filename_obj(fullname)
        if self.__experiments_repository.find_by_name(filename_obj.name) is None:
            # make a data entity
            experiments = Experiments(filename_obj)
            # save entity to the repository
            print("====================Created the new expriments!!!")
            self.__experiments_repository.save(filename_obj.name, experiments)
            self.make_default_controllers(filename_obj)
            self.__current_filename = filename_obj.name
            self.print_infor()
            return self.get_infor()
        else:
            # delete a model
            self.__experiments_repository.delete(filename_obj.name)
 
    # make a new user controller
    def create_user_controller(self, controller_key) -> str:  # controller_key = "Roi", "TimeWindow". Use the same name to delete like "ROI1"
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
            return new_key  # This is to tell the key name to ViewController
        else:
            self.__user_controller_repository.delete(controller_key)
    
    def set_experiments(self, controller_key:str, filename_key:str):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_experiments(filename_key)
        
    def bind_filename2controller(self, filename_key, controller_key):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        print(f"Bind {filename_key} to {controller_key}")
        controller.set_experiments(filename_key)

    def set_controller_val(self, controller_key: str, val: list):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_controller_val(val)
        
    def set_observer(self, controller_key, observer:object):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_observer(observer)
        
    def get_controller_val(self, controller_key: str):  # This is for getting controller value ex.RoiVal
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        return controller.val_obj
        
    def get_controller_data(self, controller_key: str):  #This is for geting controller data dictionaly
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        data_dict = controller.get_controller_data()
        if self.__mod_switch == True:
            mod_keys = controller.get_mod_list()
            print("DataService.get_controller_data: Need refactoring")
            data_dict = self.__mod_service.set_dict_mod(mod_keys, data_dict, self.__current_filename)
        return data_dict 
    
    # Use this only for a test
    def get_user_controller(self, controller_key):  # return a controller object.
        controller_key = controller_key.upper()
        return self.__user_controller_repository.data[controller_key]
    
    def get_experiments(self, experiments_key):  # return whole data_dict in experiments
        return self.__experiments_repository.data[experiments_key]
    
    def set_mod_val(self, mod_key, controller_key):
        print("DataService.set_mod_val: Need refactoring. Delete current_filneame")
        self.__mod_service.set_mod_val(mod_key, controller_key, self.__current_filename)
        
    def set_mod_key(self, controller_key, mod_key) -> None:  # set background controller to the mod class.
        print(f"Set mod: {mod_key} in {controller_key}")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_mod_key(mod_key)
    
    def reset(self, controller_key):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.reset()
        print(f"Reset: {controller_key}")
        
    def make_default_controllers(self, filename_obj):
        default_controller_list, default_data_list = self.get_experiments(filename_obj.name).get_default()
        for controller_key in default_controller_list:
            new_key = self.create_user_controller(controller_key)
            self.bind_filename2controller(filename_obj.name, new_key)
        
    def get_infor(self, controller_key=None) -> dict:
        if controller_key is None:
            controller_key_dict = {}
            for controller_key in self.__user_controller_repository.data.keys():
                controller = self.__user_controller_repository.find_by_name(controller_key)
                controller_key_dict[controller_key] = controller.get_infor()
        else:
            controller_key = controller_key.upper()
            controller = self.__user_controller_repository.find_by_name(controller_key)
            controller_key_dict = {}
            controller_key_dict[controller_key] = controller.get_infor()
        return controller_key_dict
            
    
    def print_infor(self):
        print("DataService information ===========================")
        print(f"Current experiments data = {list(self.__experiments_repository.data.keys())}")
        print(f"Current user controllers = {list(self.__user_controller_repository.data.keys())}")
        print("======================= DataService information END")
        print("")

    def __check_controller_type(self, key):
        if key == "ROI":
            return RoiFactory()
        if key == "IMAGE_CONTROLLER":
            return ImageControllerFactory()
        if key == "TRACE_CONTROLLER":
            return TraceControllerFactory()

        # To make a number for controller key.
    def __key_num_maker(self, controller_key):
        controller_key = controller_key.upper()
        controller_dict = self.__user_controller_repository.data
        # Count exsisting key
        count = 0
        for key in controller_dict.keys():
            if controller_key in key:
                count += 1
        if count == 0:
            new_key = controller_key + "1"
        else:
            # from chatGTP. Take keys with number
            numeric_keys = [key for key in controller_dict.keys() if controller_key in key and any(char.isdigit() for char in key)]
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
        print("The first step: make a experiments model. ex.model.create_experiments(filename_obj.fullname)")
        print("The second step: make a user_controller. ex.model.create_controller(\"ROI\")")
        print("The third step: bind experiments to user_controller. ex.model.bind_filename2controller(\"20408B002.tsm\", \"Roi1\")")
        print("The last step: ")
        

"""
Repository
"""
class RepositoryInterface(metaclass=ABCMeta):
    def __init__(self):
        self._data = {}   # {key:entiry}
        
    def save(self, key: str, data):
        self._data[key] = data
        print(f"Saved {key} in {self.__class__.__name__}.")
        
    def find_by_name(self, key: str):
        if key in self._data:
            #print(f"Found {key} in {self.__class__.__name__}.")
            return self._data[key]
        else:
            print(f"{self.__class__.__name__}---")
            print(f"There is no {key} in {self.__class__.__name__}. Try to make a new {key}")
            return None
    
    def delete(self, key: str):
        self._data.pop(key)
        print(f"Deleted {key} from {self.__class__.__name__}.")
        
    @property
    def data(self):
        return self._data


class ExperimentsRepository(RepositoryInterface):
    def __init__(self):
        super().__init__()

        
class UserControllerRepository(RepositoryInterface):
    def __init__(self):
        super().__init__()

    


    