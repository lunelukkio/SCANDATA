# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022
lunelukkio@gmail.com
main for controller
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.model_main import DataService
from SCANDATA.controller.controller_axes import TraceAxesController, ImageAxesController
from SCANDATA.common_class import WholeFilename, SingletonKeyDict, Switch_dict
import tkinter as tk
import os
import psutil  # for memory check


class ControllerInterface(metaclass=ABCMeta):
    """
    MainController 
    """
    @abstractmethod
    def add_axes(self, axes_name: str, axes: object) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def open_file(self, filename_obj):
        raise NotImplementedError() 
        
    @abstractmethod
    def create_experiments(self, filename_obj):
        raise NotImplementedError() 
        
    @abstractmethod
    def onclick_axes(self, event, axes_name):
        raise NotImplementedError()
        
    # set a new traces to user controller with value from experiments entity
    @abstractmethod
    def update(self, controller_list, filename_list, ch_list):
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
        


    # These are in AxesController classes
    """
    # get cotroller value object such as RoiVal.
    @abstractmethod
    def get_controller_val(self, controller_key) -> object:
        raise NotImplementedError() 

    @abstractmethod
    def get_controller_data(self, controller_key) -> dict:
        raise NotImplementedError()
    """
        
    @abstractmethod
    def print_model_infor(self):
        raise NotImplementedError() 
        
    """
    Delegation to the AxesController
    """   

    @abstractmethod
    def set_view_switch(self, controller_key, data_key, bool_val) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def ax_update(self, ax_key: str) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def ax_update_enable(self, ax_key: str) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def ax_print_infor(self, ax_key: str) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def set_roibox(self, controller_key, roi_box_pos):
        raise NotImplementedError()
        
    @abstractmethod
    def set_observer(self, controller_key: str, ax_num: int) -> None:
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
        self.__ax_dict = {}  # {"ImageAxes": ImageAxsis class, FluoAxes: TraceAx class, ElecAxes: TraceAx class}\
        
        self.__singleton_key_dict = SingletonKeyDict()  #singleton. It has filename- and controller- and data-keys.
        self.__operating_controller_set = Switch_dict()  #observer. It has filename- and controller- and data-keys.
        
        self.__singleton_key_dict.set_observer(self.__operating_controller_set)
        #print(f"Set operating controller list from singleton keys.")
        #print(self.__singleton_key_dict.get_dict())
        
    def __del__(self):
        print('.')
        #print('Deleted a MainController.' + '  myId= {}'.format(id(self)))
        #pass
        
    """
    MainController 
    """
    def add_axes(self, ax_type, axes_name: str, ax: object) -> None:
        if ax_type == "IMAGE":
            new_axes_controller = ImageAxesController(self.__model, ax)
        elif ax_type == "TRACE":
            new_axes_controller = TraceAxesController(self.__model, ax)
        self.__ax_dict[axes_name] = new_axes_controller
        self.__singleton_key_dict.set_observer(new_axes_controller.view_switch_set)
    
    def open_file(self, filename_obj=None) -> dict:
        # get filename object
        if filename_obj is None:
            filename_obj = self.__file_service.open_file()
        # make experiments data
        self.create_experiments(filename_obj) 
        filename_key = filename_obj.name
        print("777777777777777777777777777777777777777777")
        print(self.__model.get_default_data_structure(filename_key))
        # copy default controller names and data names from the model
        self.__singleton_key_dict.copy_dict(self.__model.get_default_data_structure(filename_key))
        # set filename key to key_dict
        self.__singleton_key_dict.set_filename(filename_key)
        self.print_model_infor()
        print(f"   !!! Open {filename_obj.name}: suceeded!!!")
        print("")
        return filename_obj
    
    def create_experiments(self, filename_obj: object):
        self.__model.create_experiments(filename_obj.fullname)
        # create_model end proccess
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
    
    #data_dict (e.g. CH1, ELEC0) shold be bandled because there are always come from the same controller values.
    # Calculate new data with the new controller values
    def update(self) -> None:
        switch_dict = self.__operating_controller_set.get_dict()
        filename_dict = self.__operating_controller_set.get_filename_dict()
        for controller_key in switch_dict.keys():
            filename_key_list = [filename_key 
                                     for filename_key, bool_val 
                                     in filename_dict.items() 
                                     if bool_val]
            for filename_key in filename_key_list:
                data_key_list = [data_key 
                                     for data_key, bool_val 
                                     in switch_dict[controller_key].items() 
                                     if bool_val]
                # Model can recieve not only data_list but also individual data_key directly. 
                self.__model.set_controller_data(filename_key, controller_key, data_key_list)
        
    def set_operating_controller_val(self, controller_key, data_key, bool_val):
        self.__operating_controller_set.set_val(controller_key, data_key, bool_val)
    
    def get_memory_infor(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        memory_infor = process.memory_info().rss
        maximum_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        return memory_infor, maximum_memory, available_memory
    
    def onclick_axes(self, event, axes_name):
        if event.dblclick is False:
            #if axes_name == "IMAGE_AXES":
            if event.inaxes == self.__ax_dict["IMAGE_AXES"]:
                if event.button == 1:  # left click
                    x = round(event.xdata)
                    y = round(event.ydata)
                    # set roi value in ROI
                    controller_list = self.get_operating_user_controller_list("IMAGE_AXES")
                    for controller_key in controller_list:
                        self.__main_controller.set_controller_val(controller_key, [x, y, None, None])
                        new_roi_val_obj = self.__main_cntroller.get_controller_val(controller_key)  # need change
                        roi_pos = new_roi_val_obj.data
                        # adjust for image data pixels 0.5
                        roi_box_pos = roi_pos[0]-0.5, roi_pos[1]-0.5,roi_pos[2],roi_pos[3]
                        self.__main_controller.set_roibox(controller_key, roi_box_pos)
                    self.__main_controller.ax_update("FLUO_AXES")
                elif event.button == 2:
                    pass
                elif event.button == 3:
                    # get current controller
                    old_controller_list = self.__main_controller.get_operating_controller_list()
                    # get whole ROI controller list. Violation of scorpe range.  _activePcontoller_dict should not be used from the outside of the class.
                    filtered_list = [item for item in self.__main_controller.ax_dict["FLUO_AXES"]._active_controller_dict.keys() if "ROI" in item]
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
                    self.__main_controller.ax_dict["FLUO_AXES"]._active_controller_dict[next_controller].update(self.__main_controller._ax_dict["FLUO_AXES"]._active_controller_dict[old_controller])
                    self.__main_controller._ax_dict["FLUO_AXES"].set_active_controller_key(old_controller, False)
                    print(f"Switch to {next_controller}")
                    self.update_ax(0)
                    self.update_ax(1)
            elif axes_name == "FLUO_AXES":
                if event.inaxes == self.__ax_dict["FLUO_AXES"]:
                    raise NotImplementedError()
                elif event.inaxes == self.__ax_dict["ELEC_AXES"]:
                    raise NotImplementedError()
            elif axes_name == "ELEC_AXES":
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
    
    # set UserController value. but not calculate data. Currently, self.update calculate data.
    def set_controller_val(self, val: list, key_type=None):  # e.g. val = [x, y, None, None]
        controller_list = self.__operating_controller_set.get_true_list("CONTROLLER", key_type)  # e.g. key_type = "ROI"
        for controller_key in controller_list:
            self.__model.set_controller_val(controller_key, val)
        print(f"{controller_list}: ", end='')


    def print_model_infor(self):
        self.__model.print_infor()
        
    def print_infor(self):
        print("Singleton key dict")
        self.__singleton_key_dict.print_infor()
        print("Operating controller list")
        self.__operating_controller_set.print_infor()
        print("Axes controller infor")
        for ax in self.__ax_dict.values():
            ax.print_infor()
        
    def get_key_dict(self):
        return self.__singleton_key_dict.get_dict()
        
    @property
    def ax_dict(self):
        return self.__ax_dict
    
    @property
    def operating_controller_set(self):
        return self.__operating_controller_set
        
    """
    Delegation to the AxesController
    """               
    def set_view_switch(self, ax_key, controller_key, data_key, bool_val) -> None:
        if ax_key == "ALL":
            for ax in self.__ax_dict.values():
                ax.set_switch(controller_key, data_key, bool_val)
        else:
            if ax_key not in self.__ax_dict:
                print(f"There is no Axes: {ax_key}")
            else:
                self.__ax_dict[ax_key].set_switch(controller_key, data_key, bool_val)
                
    def ax_update(self, ax_key: str) -> None:
        if ax_key == "ALL":
            for ax in self.__ax_dict.values():
                ax.update()
        else:
            if ax_key not in self.__ax_dict:
                print(f"There is no Axes: {ax_key}")
            else:
                self.__ax_dict[ax_key].update()
                
    def ax_update_enable(self, ax_key: str):
        self.__ax_dict[ax_key].ax_update_enable()
        
    def ax_print_infor(self, ax_key):
        self.__ax_dict[ax_key].print_infor()
        
    def set_roibox(self, controller_key, roi_box_pos):
        self.__ax_dict["IMAGE_AXES"].set_roibox(controller_key, roi_box_pos)
        
    def set_observer(self, controller_key: str, ax_name: str) -> None:
        self.__ax_dict[ax_name].set_observer(controller_key)
    
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


