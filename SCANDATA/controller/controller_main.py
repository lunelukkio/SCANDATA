# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022
lunelukkio@gmail.com
main for controller
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.model_main import DataService
from SCANDATA.controller.controller_axes import TraceAxesController, ImageAxesController
from SCANDATA.common_class import FileService, SingletonKeyDict, FlagDict
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
    def print_infor(self):
        raise NotImplementedError() 
        
    """
    Delegation to the AxesController
    """   

    @abstractmethod
    def set_view_flag(self, controller_key, ch_key, bool_val) -> None:
        raise NotImplementedError()
        
    @abstractmethod
    def ax_update_flag(self, ax_key: str) -> None:
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
        self.__ax_dict = {}  # {"ImageAxes": ImageAxsis class, FluoAxes: TraceAx class, ElecAxes: TraceAx class}\
        
        self.__singleton_key_dict = SingletonKeyDict()  #singleton. It has filename- and controller- and data-keys.
        self.__operating_controller_set = FlagDict()  #observer. It has filename- and controller- and data-keys.
        
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
    def add_axes(self, ax_type, axes_name: str, canvas, ax: object) -> None:
        if ax_type == "IMAGE":
            new_axes_controller = ImageAxesController(self, self.__model, canvas, ax)
        elif ax_type == "TRACE":
            new_axes_controller = TraceAxesController(self, self.__model, canvas, ax)
        self.__ax_dict[axes_name] = new_axes_controller
        self.__singleton_key_dict.set_observer(new_axes_controller.view_flag_set)
    
    def open_file(self, filename_obj=None) -> dict:
        print("========== Open a new file. ==========")
        # get filename object
        if filename_obj is None:
            filename_obj = self.__file_service.open_file()
        # make experiments data
        open_experiments = self.create_experiments(filename_obj) 
        if open_experiments is True:
            print("============================================================")
            print(f"========== Open {filename_obj.name}: suceeded!!! ==========")
            print("============================================================")
            self.__model.print_infor()
            print("")
        else:
            print("=============================================")
            print("========== Failed to open the file ==========")
            print("=============================================")
            print("")
        
        filename_key = filename_obj.name
        # copy default controller names and data names from the model
        self.__singleton_key_dict.copy_dict(self.__model.get_default_data_structure(filename_key))
        # set filename key to key_dict
        self.__singleton_key_dict.set_filename(filename_key)
        
        self.__default_view_data(filename_key)
        

        return filename_obj
    
    def create_experiments(self, filename_obj: object):
        print("Make a model (experiments entities and controllers) ---------->")
        self.__model.create_experiments(filename_obj.fullname)
        # create_model end proccess
        if self.__model == None:
            raise Exception('Failed to create a model.')
        else:
            return True
        
    def get_controller_infor(self, controller_key=None) -> dict:
        if controller_key is None:
            data_infor = self.__model.get_infor()
        else:
            data_infor = self.__model.get_infor(controller_key)
        return data_infor
    
    #data_dict (e.g. CH1, ELEC0) shold be bandled because there are always come from the same controller values.
    # Calculate new data with the new controller values
    def update(self, controller=None) -> None:  # "controller" should not have numbers
        # get a list with filename True.
        filename_true_list = self.__operating_controller_set.find_true_filename_keys()
        # get true flag controller list
        controller_true_list = self.__operating_controller_set.find_true_controller_keys(controller)
        for filename_key in filename_true_list:
            for controller_key in controller_true_list:
                # get only True ch data flag from the dict.
                ch_key_list = self.__operating_controller_set.find_true_ch_keys(controller_key)
                # Model can recieve not only data_list but also individual ch_key directly.
                self.__model.set_controller_data(filename_key, controller_key, ch_key_list)
        
    def set_operating_controller_val(self, controller_key, ch_key, bool_val=None):
        self.__operating_controller_set.set_val(controller_key, ch_key, bool_val)
        
    def __default_view_data(self, filename_key):
        print("=============================================")
        print("========== Start default settings. ==========")
        print("=============================================")
        
        self.set_observer("ROI0", "FLUO_AXES")   #background for bg_comp, (controller_key, AXES number)
        self.set_observer("ROI1", "FLUO_AXES")
        self.set_observer("IMAGE_CONTROLLER0", "IMAGE_AXES")  # base image for difference image
        self.set_observer("IMAGE_CONTROLLER1", "IMAGE_AXES")  # for difference image
        self.set_observer("ELEC_TRACE_CONTROLLER0", "ELEC_AXES")  # no use
        self.set_observer("ELEC_TRACE_CONTROLLER1", "ELEC_AXES")

        # set axes controllers view flages
        self.set_view_flag("ALL", "ALL", "ALL", False)  # (ax, controller_key, data_key, value) 
        self.set_view_flag("FLUO_AXES", "ROI1", "CH1", True)  # (ax, controller_key, data_key, value)
        self.set_view_flag("IMAGE_AXES", "IMAGE_CONTROLLER1", "CH1", True)  # (ax, controller_key, data_key, value) 
        self.set_view_flag("ELEC_AXES", "ELEC_TRACE_CONTROLLER1", "ELEC0", True)  # (ax, controller_key, data_key, value) 
        # set maincontroller keys "CH1", "ELEC0"
        self.set_operating_controller_val("ALL", "ALL", False)  # All flag is False
        self.set_operating_controller_val("ROI0", "CH1", True)  # This is for difference image
        self.set_operating_controller_val("ROI0", "CH2", True)  # This is for difference image
        self.set_operating_controller_val("ROI1", "CH1", True)  # This is for difference image
        self.set_operating_controller_val("ROI1", "CH2", True)  # This is for difference image
        self.set_operating_controller_val("IMAGE_CONTROLLER1", "CH1", True)  # This is for a cell image
        self.set_operating_controller_val("IMAGE_CONTROLLER1", "CH2", True)  # This is for a cell image
        self.set_operating_controller_val("ELEC_TRACE_CONTROLLER1", "ELEC0", True)  # This is for a elec trace

        """ about mod"""
        self.set_mod_val("BGCOMP", filename_key)
        self.set_mod_key("ROI1", "DFOVERF")
        self.set_mod_key("ROI1", "BGCOMP")
        # Set ROI0 as background in ROI1 controller
        # send background ROI. but it done outside of the model.
        #background_dict = self.get_controller_data("ROI0")
        #self.set_mod_val("ROI1", "BGCOMP", background_dict)
        # Turn on the flag of BGCOMP for ROI1.
        #self.set_mod_key("ROI1", "BGCOMP")
        """
        # set background roi to the mod class
        self.set_mod_val("ROI1", "BgCompMod")
        
        # set mod
        self.set_mod_key("ROI2", "BGCOMP")
        """
        print("========== End of default settings ==========")
    
    def get_memory_infor(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        memory_infor = process.memory_info().rss
        maximum_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        return memory_infor, maximum_memory, available_memory
    
    def onclick_axes(self, event, axes_name):
        axes_name = axes_name.upper()
        if event.dblclick is False:
            true_flag = self.__operating_controller_set.find_true_controller_keys()
            #if axes_name == "IMAGE_AXES":
            if axes_name == "IMAGE_AXES":
                if event.button == 1:  # left click
                    x = round(event.xdata)
                    y = round(event.ydata)
                    val = [x, y, None, None]
                    # set roi value in ROI
                    roi_true_flag = [key for key in true_flag if "ROI" in key]
                    for controller_key in roi_true_flag:
                        self.__model.set_controller_val(controller_key, val)
                    self.update("ROI")
                elif event.button == 2:
                    pass
                # move to next controller
                elif event.button == 3:
                    # move and copy ch boolen value
                    self.__operating_controller_set.next_controller_to_true("ROI")
                    self.__ax_dict["FLUO_AXES"].next_controller_to_true("ROI")
                    self.update("ROI")
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
        
    def change_roi_size(self, val:list):
        controller_true_list = self.__operating_controller_set.find_true_controller_keys("ROI")
        for controller_key in controller_true_list:
            # set roi in user controller
            self.__model.set_controller_val(controller_key, val)
        self.update("ROI")
            
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

    def print_infor(self):
        print("======================================")
        print("========== Data Information ==========")
        print("======================================")
        self.__model.print_infor()
        print("Operating controller list ---------->")
        self.__operating_controller_set.print_infor()
        print("Axes controller infor ---------->")
        for ax in self.__ax_dict.values():
            ax.print_infor()
        print("========== Data Information End ==========")
        print("")
        
    def get_key_dict(self):
        return self.__singleton_key_dict.get_dict()
    
    def get_canvas_axes(self, view_controller) -> object:
            return self.__ax_dict[view_controller].get_canvas_axes()
        
    @property
    def ax_dict(self):
        return self.__ax_dict
    
    @property
    def operating_controller_set(self):
        return self.__operating_controller_set
        
    """
    Delegation to the AxesController
    """               
    def set_view_flag(self, ax_key, controller_key, ch_key, bool_val=None) -> None:
        if ax_key == "ALL":
            for ax in self.__ax_dict.values():
                ax.set_flag(controller_key, ch_key, bool_val)
        else:
            if ax_key not in self.__ax_dict:
                print(f"There is no Axes: {ax_key}")
            else:
                self.__ax_dict[ax_key].set_flag(controller_key, ch_key, bool_val)

    def ax_update_flag(self, ax_key: str, val=None):
        self.__ax_dict[ax_key].ax_update_flag(val)
        
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
        self.__model.set_mod_key(controller_key, mod_key)
        
    def set_mod_val(self, mod_key, val):
        self.__model.set_mod_val(mod_key, val)
        
class AiController:
    def __init__(self):
        self.__file_service = FileService()
        
    def rename_files(self):
        self.__file_service.rename_files()



