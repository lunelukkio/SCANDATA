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

"""
Service
"""
class ModelInterface(metaclass=ABCMeta):
    # create epxeriments entity in the repository with filename.
    @abstractmethod
    def create_experiments(self, fullname):
        raise NotImplementedError()
        
    @abstractmethod
    def change_current_filename(self, filename_obj):
        raise NotImplementedError()
        
    # make a new value of data.
    @abstractmethod
    def create_user_controller(self, controller_key) -> str:
        raise NotImplementedError()
        
    # return whole data_dict in experiments. It is used by user_controllers.
    @abstractmethod
    def get_experiments(self, key) -> object:
        raise NotImplementedError()
        
    # set a new controller value.
    @abstractmethod
    def set_controller_val(self, controller_key: str, val: list):
        raise NotImplementedError()
        
    # value object ex RoiVal. It is used by controllers for chaning the size of ROI.
    @abstractmethod
    def get_controller_val(self, controller_key) -> object:
        raise NotImplementedError()

    # make a new data from experiments entities into the controllers.
    @abstractmethod
    def set_controller_data(self, controller_key:str):
        raise NotImplementedError()
        
    # return a dict of controller including value objects.
    @abstractmethod
    def get_controller_data(self, controller_key: str):
        raise NotImplementedError()

    # set an axis observer of view into controller 
    @abstractmethod
    def set_observer(self, controller_key, observer:object):
        raise NotImplementedError()

    # set a mod key to the mod list
    @abstractmethod
    def set_mod_key(self, controller_key, mod_key) -> None:
        raise NotImplementedError()
        
    # set background controller to the mod class.
    @abstractmethod
    def set_mod_val(self, controller_key, mod_key, val) -> None:
        raise NotImplementedError()
        
    # reset controller_val
    @abstractmethod
    def reset(self, controller_key):
        raise NotImplementedError()
        
    # get infor of dict
    @abstractmethod
    def get_infor(self, controller_key):
        raise NotImplementedError() 
        
    @abstractmethod
    def help(self):
        raise NotImplementedError() 
        
        
class DataService(ModelInterface):
    def __init__(self):
        self.__experiments_repository = ExperimentsRepository()
        self.__user_controller_repository = UserControllerRepository()
        self.__current_filename_obj = None
        
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
            self.__experiments_repository.save(filename_obj.name, experiments)
            self.change_current_filename(filename_obj)
            print("====================Created a new expriments!!!")
            # make controllers
            self.make_default_controllers(filename_obj)
            self.print_infor()
        else:
            # delete a model
            self.__experiments_repository.delete(filename_obj.name)
            
    def change_current_filename(self, filename_obj):
        if filename_obj.name in self.__experiments_repository.data:
            self.__current_filename_obj = filename_obj
        else:
            print(f"There is no experiments file in the model: {filename_obj.name}")
        
    def make_default_controllers(self, filename_obj):
        default_controller_list, default_data_list = self.get_experiments(filename_obj.name).get_default()
        for controller_key in default_controller_list:  # controller_list doesn't have controller numbers
            self.create_user_controller(controller_key)

    # make a new user controller
    def create_user_controller(self, controller_key) -> str:  # controller_key = "Roi", "TimeWindow". Use the same name to delete like "ROI1"
        controller_key = controller_key.upper()
        if self.__user_controller_repository.find_by_name(controller_key) is None:
            # get a controller factory 
            controller_factory = self.__check_controller_type(controller_key)
            # make a new controller with the method in DataService
            new_controller = controller_factory.create_controller()
            # set data in controller
            experiments_obj = self.get_experiments(self.__current_filename_obj.name)
            new_controller.set_controller_data(experiments_obj)
            # get a new controller key name
            new_key = self.__key_num_maker(controller_key)
            # save the controller to repository
            self.__user_controller_repository.save(new_key, new_controller)
            print(f"====================Created the new controller {controller_key}")
            self.print_infor()
            return new_key  # This is to tell the key name to axtive_controller_dict in ViewController ax
        else:
            self.__user_controller_repository.delete(controller_key)

            
    def get_experiments(self, filename_key) -> object:  # return an experiments entity
        experiments_entity = self.__experiments_repository.find_by_name(filename_key)
        return experiments_entity

    def set_controller_val(self, controller_key: str, val: list):
        # get the controller
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        # set the controller values
        controller.set_controller_val(val)
        # get the experiments
        experiments_obj = self.get_experiments(self.__current_filename_obj.name)
        # get trace_obj from the exeriments
        controller.set_controller_data(experiments_obj)
        # notiry axis. then they will use "self.get_controller_data"
        controller.observer.notify_observer()
        
    def get_controller_val(self, controller_key: str):  # This is for getting controller value ex.RoiVal
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        return controller.val_obj
    
    def set_controller_data(self, controller_key:str):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        experiments_obj = self.get_experiments(self.__current_filename_obj.name)
        controller.set_controller_data(experiments_obj)
        
    def get_controller_data(self, controller_key: str):  #This is for geting controller data dictionaly
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        data_dict = controller.get_controller_data()
        return data_dict 
        
    def set_observer(self, controller_key, observer:object):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_observer(observer)

    # Use this only for a test. return a controller object.
    def get_user_controller(self, controller_key):
        controller_key = controller_key.upper()
        return self.__user_controller_repository.data[controller_key]
        
    def set_mod_key(self,controller_key, mod_key) -> None:
        print(f"Set mod: {mod_key} in {controller_key}")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_mod_key(mod_key)

    def set_mod_val(self, controller_key, mod_key, val):
        print(f"Set mod value: Set {type(val)} to {mod_key} in {controller_key}")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_mod_val(mod_key, val)
    
    def reset(self, controller_key):
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.reset()
        print(f"Reset: {controller_key}")

        
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
        # count the number of identiried controller
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

    


    