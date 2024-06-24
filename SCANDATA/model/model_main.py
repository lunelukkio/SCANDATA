# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:11:15 2023

@author: lunelukkio@gmail.com
When new controllers are added, import from "user controller" factory and __check_controller_type in DataService also should be modified.

"""
from abc import ABCMeta, abstractmethod
from SCANDATA.common_class import WholeFilename, FlagDict
from SCANDATA.model.experiments import Experiments
from SCANDATA.model.user_controller import RoiFactory, ImageControllerFactory, ElecTraceControllerFactory
from SCANDATA.model.mod.mod_main import ModService
import re  # This is for regular expression 

"""
Service
"""
class ModelInterface(metaclass=ABCMeta):
    # create epxeriments entity in the repository with filename.
    @abstractmethod
    def create_experiments(self, fullname):
        raise NotImplementedError()
        
    # make a new value of data. return controller a key name.
    @abstractmethod
    def create_user_controller(self, controller_key) -> str:
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
    # This method can receive a list or str as a ch_key
    @abstractmethod
    def set_controller_data(self, filename_key: str, controller_key: str, ch_key_or_list):  #ch_key = list or str
        raise NotImplementedError()

    # return a dict of value objects with filename.
    @abstractmethod
    def get_data(self, filename_key: str, controller_key) -> dict:
        raise NotImplementedError()

    # set an axes observer of view into controller. If observer is empty, update all controllers.
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
        
    # get data key dict from the data repository
    @abstractmethod
    def get_infor(self, controller_key):
        raise NotImplementedError()
        
    def get_default_data_structure(self, filename_key):
        raise NotImplementedError()
        
    def print_infor(self, filename_key):
        raise NotImplementedError()
        
    @abstractmethod
    def help(self):
        raise NotImplementedError() 
        
        
class DataService(ModelInterface):
    def __init__(self):
        self.__experiments_repository = Repository()
        self.__user_controller_repository = Repository()
        self.__data_repository = DataRepository()
        self.__mod_service = ModService(self)
        self.__mod_flag = True # This is for test.
        
    def __create_filename_obj(self, fullname):
        filename_obj = WholeFilename(fullname)
        return filename_obj
        
    def create_experiments(self, fullname): # Use the same name to delete a model
        # make a filename value obj from fullname
        filename_obj = self.__create_filename_obj(fullname)
        if self.__experiments_repository.find_by_name(filename_obj.name) is None:
            # make a data entity
            experiments = Experiments(filename_obj)
            # save entity to the repository
            self.__experiments_repository.save(filename_obj.name, experiments)
            print("===============================================")
            print("==========Created a new expriments!!!==========")
            print("===============================================")
            print("")
            # make controllers
            self.make_default_controllers(filename_obj)
        else:
            # delete a model
            self.__experiments_repository.delete(filename_obj.name)
        
    def make_default_controllers(self, filename_obj):
        experiments_data = self.__experiments_repository.find_by_name(filename_obj.name)
        default_data_structure = experiments_data.get_default_data_structure()
        for controller_key in default_data_structure.keys():
            controller_key_without_number = re.sub(r'\d+$', '', controller_key)
            self.create_user_controller(filename_obj, controller_key_without_number, default_data_structure[controller_key])

    # make a new user controller. New keys should not have any number.
    def create_user_controller(self, filename_obj, controller_key, ch_key_list) -> str:  # controller_key = "Roi", "TimeWindow". Use the same name to delete like "ROI1"
        controller_key = controller_key.upper()
        if self.__user_controller_repository.find_by_name(controller_key) is None:
            # get a controller factory 
            controller_factory = self.__check_controller_type(controller_key)
            # make a new controller with the method in DataService
            new_controller = controller_factory.create_controller()
            # set data in controller
                  #experiments_obj = self.get_experiments(filename_obj.name)
                  #new_controller.set_controller_data(experiments_obj, ch_key_list)
            # get a new controller key name
            new_key = self.__key_num_maker(controller_key)
            # save the controller to repository
            self.__user_controller_repository.save(new_key, new_controller)
            print("")
            return new_key  # This is to tell the key name to axtive_controller_dict in MainController ax
        else:
            self.__user_controller_repository.delete(controller_key)

    # set controller value and set controller data using the new value
    def set_controller_val(self, controller_key: str, val: list):
        print(f"DataService: set_controller_val ({controller_key}, {val}) ---------->")
        # get the controller
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        # set the controller values
        controller.set_controller_val(val)
        # notiry axes. then they will use "self.get_controller_data"
        print("----------> Done: set_controller_val")
        
    def get_controller_val(self, controller_key: str):  # This is for getting controller value ex.RoiVal
        print(f"DataService: get_controller_val ({controller_key}) ---------->")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        print("----------> Done: get_controller_val")
        return controller.val_obj
    
    
    # This method can receive a list or str as a ch_key, but usually it shold be data_list becase every data shold be produced by the same controller.
    def set_controller_data(self, filename_key:str, controller_key: str, ch_key_list):
        print(f"DataService: set_controller_data ({controller_key}) ---------->")
        experiments_obj = self.__experiments_repository.find_by_name(filename_key)
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        ch_data_dict = controller.set_controller_data(experiments_obj, ch_key_list)
        self.__data_repository.save(filename_key, controller_key, ch_data_dict)
        print("----------> Done: set_controller_data")

    # return a dict of value objects with filename.
    def get_data(self, filename_key, controller_key) -> dict:  # dict e.g.{'CH1': <SCANDATA.model.value_object.TraceData object at 0x000001905EC11850>, 'CH2': <SCANDATA.model.value_object.TraceData object at 0x000001905CC856D0>}
        print(f"DataService: get_data ({controller_key}) ---------->")
        controller_key = controller_key.upper()
        data_dict = self.__data_repository.find_by_name(filename_key, controller_key)
        if data_dict is None:
            print(f"Can't find {filename_key}, {controller_key}")
            return
        # apply mod 
        if self.__mod_flag is True:
            controller = self.__user_controller_repository.find_by_name(controller_key)
            mod_list = controller.get_mod_list()
            data_dict = self.__mod_service.apply_mod(data_dict, mod_list)
            print("Data modified")
        print("----------> Done: get_data")
        return data_dict
            
    def set_observer(self, controller_key, observer:object):
        print(f"DataService: set_observer ({observer.__class__.__name__} to {controller_key}) ---------->")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_observer(observer)
        print("----------> Done: set_observer")
        
    def update_observer(self, controller_key=None):
        if controller_key is None:
            print("DataService: update_observer (All user controller) ---------->")
            controller_key_list = self.__user_controller_repository.get_infor()
            for controller_key in controller_key_list:
                controller = self.__user_controller_repository.find_by_name(controller_key)
                controller.notify_observer()
        else:
            print(f"DataService: update_observer ({controller_key}) ---------->")
            controller = self.__user_controller_repository.find_by_name(controller_key)
            controller.notify_observer()
        print("----------> Done: update_observer")
            

    # Use this only for a test. return a controller object.
    def get_user_controller(self, controller_key):
        print(f"DataService: get_user_controller ({controller_key}) ---------->")
        controller_key = controller_key.upper()
        print("----------> Done: get_user_controller")
        return self.__user_controller_repository.data[controller_key]
    
        
    def set_mod_key(self,controller_key, mod_key) -> None:
        print(f"DataService: set_mod_key ({mod_key} in {controller_key})")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.set_mod_key(mod_key)
        print("----------> Done: set_mod_key")

    def set_mod_val(self, mod_key, val):
        print(f"DataService: set_mod_val ({val} to {mod_key})")
        self.__mod_service.set_mod_val(mod_key, val)
        print("----------> Done: set_mod_val")
    
    def reset(self, controller_key):
        print(f"DataService: reset ({controller_key}) ---------->")
        controller_key = controller_key.upper()
        controller = self.__user_controller_repository.find_by_name(controller_key)
        controller.reset()
        print("----------> Done: reset")

    # get data key dict from the data repository
    def get_infor(self, filename_key=None, controller_key=None) -> dict:
        if filename_key is None:
            return self.__data_repository.data
        else:
            if controller_key is None:
                print(self.__data_repository.data)
                data_keys = self.__data_repository.find_by_name(filename_key).get_infor()
                return data_keys[filename_key]   
            
    def get_default_data_structure(self, filename_key):
        experiments_entity = self.__experiments_repository.find_by_name(filename_key)
        return experiments_entity.get_default_data_structure()
    
    def print_infor(self):
        print("Model Repository Information ---------->")
        print(f"Experiments repository     = {self.__experiments_repository.get_infor()}")
        print(f"User controller repository = {self.__user_controller_repository.get_infor()}")
        print(f"Data repository            = {self.__data_repository.get_infor()}")
        print("----------> Model Repository Information END")
        print("")

    def __check_controller_type(self, key):
        if "ROI" in key:
            return RoiFactory()
        elif "IMAGE_CONTROLLER" in key:
            return ImageControllerFactory()
        elif "ELEC_TRACE_CONTROLLER" in key:
            return ElecTraceControllerFactory()
        else:
            print(f"{key} Factory done not exist.")

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
            new_key = controller_key + "0"
        else:
            # Take keys with number
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
# Need refactoring using keys* and recursive function
class RepositoryInterface(metaclass=ABCMeta):
    def __init__(self):
        self._data = {}   # {key:entity}
        
    def save(self, key: str, data):
        self._data[key] = data
        print(f"Saved {key} in {self.__class__.__name__}.")
        
    def find_by_name(self, key: str):
        if key in self._data:
            #print(f"Found {key} in {self.__class__.__name__}.")
            return self._data[key]
        else:
            return None
    
    def delete(self, key: str):
        self._data.pop(key)
        print(f"Deleted {key} from {self.__class__.__name__}.")
        
    # return data dict keys without value obujects
    def get_infor(self):
        return FlagDict.data_dict_to_key_dict(self._data)
        
    @property
    def data(self):
        return self._data


class Repository(RepositoryInterface):
    def __init__(self):
        super().__init__()

        
class DataRepository(RepositoryInterface):
    def __init__(self):
        super().__init__()
        
    # data should not be replaced.
    def save(self, filename_key: str, controller_key, ch_data_dict):
        if filename_key not in self._data:
            controller_dict = {}
            controller_dict[controller_key] = ch_data_dict
            self._data[filename_key] = controller_dict
        else:
            self._data[filename_key][controller_key] = ch_data_dict
        #print(f"Saved {filename_key} in {self.__class__.__name__}.")

        
    # override
    def find_by_name(self, filename_key, controller_key=None):
        if controller_key is None:
            if filename_key in self._data:
                return self._data[filename_key]
            else:
                print(f"There is no {filename_key} in the data_repository")
        else:
            if filename_key in self._data:
                if controller_key in self._data[filename_key]:
                    return self._data[filename_key][controller_key]
                else:
                    print(f"There is no {controller_key} in {filename_key}")
            else:
                print(f"There is no {filename_key} in the data_repository")
            
    # override        
    def delete(self, filename_key, controller_key):
        if filename_key in self._data:
            if controller_key in self._data[filename_key]:
                del self._data[filename_key][controller_key]
                print(f"Deleted {controller_key} from {filename_key} in the data_repository")
            else:
                print(f"There is no {controller_key} in {filename_key}")
        else:
            print(f"There is no {filename_key} in the data_repository")


        
        
            
        

    


    