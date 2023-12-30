# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022
lunelukkio@gmail.com
main for controller
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.model_main import DataService
from SCANDATA.common_class import WholeFilename, ImagingDataStructure
import tkinter as tk
import os
import psutil  # for memory check


class ControllerInterface(metaclass=ABCMeta):
    """
    MainController 
    """
    @abstractmethod
    def add_axis(self, axis_name: str, axis: object) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def open_file(self, filename_obj):
        raise NotImplementedError() 
        
    @abstractmethod
    def create_experiments(self, filename_obj):
        raise NotImplementedError() 
        
    @abstractmethod
    def get_controller_infor(self, controller_key=None) -> dict:
        raise NotImplementedError()
        
    """
    Delegation to the Model
    """ 
    @abstractmethod
    def create_user_controller(self, controller_key):
        raise NotImplementedError() 
  
    # set a new user controller values such as RoiVal.
    @abstractmethod
    def set_controller_val(self, controller_key: str, val: list):
        raise NotImplementedError() 
        
    # get cotroller value object such as RoiVal.
    @abstractmethod
    def get_controller_val(self, controller_key) -> object:
        raise NotImplementedError() 
        
    # set a new traces to user controller with value from experiments entity
    @abstractmethod
    def set_controller_data(self, controller_list, filename_list, ch_list):
        raise NotImplementedError()

    @abstractmethod
    def get_controller_data(self, controller_key) -> dict:
        raise NotImplementedError()
        
    @abstractmethod
    def set_observer(self, controller_key: str, ax_num: int) -> None:
        raise NotImplementedError() 
        
    @abstractmethod
    def print_model_infor(self):
        raise NotImplementedError() 
        
    """
    Delegation to the AxisController
    """   
    @abstractmethod
    def get_operating_user_controller_list(self, ax_key: str):
        raise NotImplementedError()

    @abstractmethod
    def ax_update_switch(self, ax_key: str, swtch: bool) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def ax_update(self, ax_key: str) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def ax_print_infor(self, ax_key: str) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def set_roibox(self, controller_key, roi_box_pos):
        raise NotImplementedError()
    
    """
    Delegation to the Model
    """
    @abstractmethod
    def set_mod_key(self, controller_key, mod_key):
        raise NotImplementedError() 
        
    @abstractmethod
    def set_mod_val(self, controller_key, mod_key, val):
        raise NotImplementedError() 

class MainController(ControllerInterface):
    def __init__(self, view=None):
        self.__model = DataService()
        self.__file_service = FileService()
        self.__mod_controller = ModController(self.__model)
        self.__ax_dict = {}  # {"ImageAxis": ImageAxsis class, FluoAxis: TraceAx class, ElecAxis: TraceAx class}
        self.__imaging_data_structure = ImagingDataStructure()
        
    def __del__(self):
        print('.')
        #print('Deleted a MainController.' + '  myId= {}'.format(id(self)))
        #pass
        
    """
    MainController 
    """
    def add_axis(self, axis_name: str, axis_obj: object) -> None:
        self.__ax_dict[axis_name] = axis_obj
    
    def open_file(self, filename_obj=None) -> dict:
        # get filename object
        if filename_obj is None:
            filename_obj = self.__file_service.open_file()
        # make experiments data
        self.create_experiments(filename_obj) 
        self.print_model_infor()
        print(f"   !!! Open {filename_obj.name}: suceeded!!!")
        print("")
        return filename_obj
    
    def create_experiments(self, filename_obj: object):  
        controller_dict_keys = self.__model.create_experiments(filename_obj.fullname)
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== MainController: Suceeded to read data from data files.')
            print('')
            return controller_dict_keys
        
    def get_controller_infor(self, controller_key=None) -> dict:
        if controller_key is None:
            data_infor = self.__model.get_infor()
        else:
            data_infor = self.__model.get_infor(controller_key)
        return data_infor
    
    def get_memory_infor(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        memory_infor = process.memory_info().rss
        maximum_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        return memory_infor, maximum_memory, available_memory
            
    """
    Delegation to the Model
    """           
    def create_user_controller(self, controller_key):
        new_key = self.__model.create_user_controller(controller_key)
        return new_key

    def set_controller_val(self, controller_key: str, val: list):
        self.__model.set_controller_val(controller_key, val)
        
    def get_controller_val(self, controller_key) -> object:
        return self.__model.get_controller_val(controller_key)
        
    def set_controller_data(self, controller_list, filename_list, ch_list):
        self.__model.set_controller_data(controller_list, filename_list, ch_list)
        
    def get_controller_data(self, controller_key) -> dict:
        data_dict = self.__model.get_controller_data(controller_key)
        if data_dict is None:
            print(f"Can't find data_dict in {controller_key}")
        else:
            return data_dict
        
    def set_observer(self, controller_key: str, ax_key: str) -> None:
        self.__model.set_observer(controller_key, self.__ax_dict[ax_key])
        
    def print_model_infor(self):
        self.__model.print_infor()
        
    @property
    def ax_dict(self):
        return self.__ax_dict
        
    """
    Delegation to the AxisController
    """    
    def get_operating_user_controller_list(self, ax_key):
        return self.__ax_dict[ax_key].get_operating_user_controller_list()
    
    def ax_update_switch(self, ax_key: str, val=None) -> None:
        self.__ax_dict[ax_key].ax_update_switch(val)
        
    def ax_update(self, ax_key: str):
        self.__ax_dict[ax_key].update()
        
    def ax_print_infor(self, ax_key):
        self.__ax_dict[ax_key].print_infor()
        
    def set_roibox(self, controller_key, roi_box_pos):
        self.__ax_dict["IMAGE_AXIS"].set_roibox(controller_key, roi_box_pos)
    
    """
    Delegation to the ModController
    """        
    def set_mod_key(self, controller_key, mod_key):
        self.__mod_controller.set_mod_key(controller_key, mod_key)
        
    def set_mod_val(self, controller_key, mod_key, val):
        self.__mod_controller.set_mod_val(controller_key, mod_key, val)
        

        

class FileService:
    def open_file(self, *filename):  # it can catch variable num of filenames.
        if filename == ():
            fullname = self.get_fullname()  # This is str filename
            if fullname == None:
                print("There is no such a filename.")
                return
            new_full_filename = fullname
        else:
            new_full_filename = filename
        return WholeFilename(new_full_filename)
    
    
    @staticmethod
    def get_fullname(event=None):
        # open file dialog
        fullname = tk.filedialog.askopenfilename(
            initialdir = os.getcwd(), # current dir
            filetypes=(('All files', '*.*'), 
                       ('Tsm files', '*.tsm'),
                       ('Da files', '*.da'), 
                       ('Axon files', '*.abf'),
                       ('WinCP files', '*.wcp')
                      ))
        return fullname

class ModController:
    def __init__(self, model):
        self.__model = model
        
    def set_mod_key(self, controller_key, mod_key):
        self.__model.set_mod_key(controller_key, mod_key)
        
    def set_mod_val(self, controller_key, mod_key, val):
        self.__model.set_mod_val(controller_key, mod_key, val)


