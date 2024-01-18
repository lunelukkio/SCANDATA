# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022
lunelukkio@gmail.com
main for controller
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.model_main import DataService
from SCANDATA.controller.controller_axis import TraceAxisController, ImageAxisController
from SCANDATA.common_class import WholeFilename, DataKeySet, DataSwitchSet
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
    def onclick_axis(self, event, axis_name):
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
        self.__ax_dict = {}  # {"ImageAxis": ImageAxsis class, FluoAxis: TraceAx class, ElecAxis: TraceAx class}\
        
        self.__data_key_dict = DataKeySet()  #singleton
        self.__operating_controller_set = DataSwitchSet()  #observer
        self.__data_key_dict.add_observer(self.__operating_controller_set)
        
    def __del__(self):
        print('.')
        #print('Deleted a MainController.' + '  myId= {}'.format(id(self)))
        #pass
        
    """
    MainController 
    """
    def add_axis(self, axis_name: str, ax: object) -> None:
        new_axis_controller = ImageAxisController(self.__model, ax)
        self.__ax_dict[axis_name] = new_axis_controller
        self.__data_key_dict.add_observer(new_axis_controller)
    
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
        self.__model.create_experiments(filename_obj.fullname)
        # set key name list
        controller_dict_keys = self.__model.get_infor()
        self.__data_key_dict.set_data_key("FILENAME", filename_obj.name)
        for key in controller_dict_keys:
            self.__data_key_dict.set_data_key("CONTROLLER", key)
        for key in controller_dict_keys:
            self.__data_key_dict.set_data_key("CH", key)
        print(self.__data_key_dict.key_dict)
        # end proccess
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            print('============================== MainController: Suceeded to read data from data files.')
            print('')
        
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
    
    def onclick_axis(self, event, axis_name):
        if event.dblclick is False:
            if axis_name == "IMAGE_AXIS":
                if event.button == 1:  # left click
                    x = round(event.xdata)
                    y = round(event.ydata)
                    # set roi value in ROI
                    controller_list = self.get_operating_user_controller_list("IMAGE_AXIS")
                    for controller_key in controller_list:
                        self.__main_controller.set_controller_val(controller_key, [x, y, None, None])
                        new_roi_val_obj = self.__main_controller.get_controller_val(controller_key)
                        roi_pos = new_roi_val_obj.data
                        # adjust for image data pixels 0.5
                        roi_box_pos = roi_pos[0]-0.5, roi_pos[1]-0.5,roi_pos[2],roi_pos[3]
                        self.__main_controller.set_roibox(controller_key, roi_box_pos)
                    self.__main_controller.ax_update("FLUO_AXIS")
                elif event.button == 2:
                    pass
                elif event.button == 3:
                    # get current controller
                    old_controller_list = self.__main_controller.get_operating_controller_list()
                    # get whole ROI controller list. Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                    filtered_list = [item for item in self.__main_controller.ax_dict["FLUO_AXIS"]._active_controller_dict.keys() if "ROI" in item]
                    for old_controller in old_controller_list:
                        if old_controller in filtered_list:
                            index = filtered_list.index(old_controller)
                            if index < len(filtered_list) - 1:
                                next_controller =filtered_list[index + 1]
                            else:
                                next_controller =filtered_list[0]
                        else:
                            print("Not in the active controller list")
                        
                    self.__main_controller.set_operating_controller_list(old_controller)
                    self.__main_controller.set_operating_controller_list(next_controller)
                    # Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                    # Need refactoring.
                    self.__main_controller.ax_dict["FLUO_AXIS"]._active_controller_dict[next_controller].update(self.__main_controller._ax_dict["FLUO_AXIS"]._active_controller_dict[old_controller])
                    self.__main_controller._ax_dict["FLUO_AXIS"].set_active_controller_key(old_controller, False)
                    print(f"Switch to {next_controller}")
                    self.update_ax(0)
                    self.update_ax(1)
            elif axis_name == "FLUO_AXIS":
                raise NotImplementedError() 
            elif axis_name == "ELEC_AXIS":
                raise NotImplementedError() 
        elif event.dblclick is True:
            print("Double click is for ----")
        print('')
            
    """
    Delegation to the Model
    """           
    def create_user_controller(self, controller_key):
        new_key = self.__model.create_user_controller(controller_key)
        return new_key


        

        
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


