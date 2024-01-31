# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 09:01:53 2023

@author: lunel
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.common_class import Switch_dict
import matplotlib.patches as patches
import json


class AxesController(metaclass=ABCMeta):
    def __init__(self, model, ax):
        self._tools = AxesTools(ax)
        self._ax_obj = ax
        self._model = model
        
        self._view_switch_set = Switch_dict()

        self._marker_obj = {}  # This is for makers in axes windows.
        
        self.sync_switch = False  # This switch is to show each data in each controllers.
        self.update_switch = True  # This switch is for avoiding image view update. Ture or False or empty: flip switch.
        
        # color selection for traces and RoiBoxes
        try:
            with open("../setting/axes_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        except:
            with open("./setting/axes_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        self._ch_color = setting.get("ch_color")
        self._controller_color = setting.get("controller_color")
            
    def set_switch(self, controller_key, data_key, bool_val):
            self._view_switch_set.set_val(controller_key, data_key, bool_val)
     
    # to get a controller valueobject
    def get_controller_val(self, controller_key) -> object:
        return self._model.get_controller_val(controller_key)
        
    # get value object from controllers
    def get_controller_data(self, controller_key) -> dict:
        data_dict = self._model.get_controller_data(controller_key)
        if data_dict is None:
            print(f"Can't find data_dict in {controller_key}")
        else:
            return data_dict
        
    def set_observer(self, controller_key) -> None:
        self._model.set_observer(controller_key, self)

    @abstractmethod
    def set_view_data(self, active_controller_dict):
            raise NotImplementedError()
            
    """
    def set_user_controller_list(self, controller_key):
        if controller_key not in self._user_controller_list:
            self._user_controller_list.append(controller_key)
            print(f"Added {controller_key} to {self._user_controller_list} of {self.__class__.__name__}")
        else:
            self._user_controller_list.remove(controller_key)
            print(f"Removed {controller_key} from {self._user_controller_list} of {self.__class__.__name__}")
            
    def set_operating_user_controller_list(self, controller_key):
        if controller_key not in self._operating_user_controller_list:
            self._operating_user_controller_list.append(controller_key)
            print(f"Added {controller_key} to {self._operating_user_controller_list} of {self.__class__.__name__}")
        else:
            self._operating_user_controller_list.remove(controller_key)
            print(f"Removed {controller_key} from {self._operating_user_controller_list} of {self.__class__.__name__}")
            
    def set_operating_filename_list(self, filename_key):
        if filename_key not in self._operating_filename_list:
            self._operating_filename_list.append(filename_key)
            print(f"Added {filename_key} to {self._operating_filename_list} of {self.__class__.__name__}")
        else:
            self._operating_filename_list.remove(filename_key)
            print(f"Removed {filename_key} from {self._operating_filename_list} of {self.__class__.__name__}")
            
    def set_operating_ch_list(self, ch_key):
        if ch_key not in self._operating_ch_list:
            self._operating_ch_list.append(ch_key)
            print(f"Added {ch_key} to {self._operating_ch_list} of {self.__class__.__name__}")
        else:
            self._operating_ch_list.remove(ch_key)
            print(f"Removed {ch_key} from {self._operating_ch_list} of {self.__class__.__name__}")
    
    """

    def ax_update_switch(self, val=None):
        if val is True:
            self.update_switch = True
        elif val is False:
            self.update_switch = False
        else:
            self.update_switch = not self.update_switch
        
    def draw_ax(self):
        self.set_view_data()
        self._ax_obj.relim()
        self._ax_obj.autoscale_view()
        self.canvas.draw()
        
    def update(self):  # It is overrided by ImageAx
        if self.update_switch == True:
            self._ax_obj.cla()  # clear ax
            for controller_key in self._operating_user_controller_list:
                for filename_key in self._operating_filename_list:
                    self._main_controller.set_controller_data(controller_key,
                                                         filename_key,
                                                         self._operating_ch_list)
            self.draw_ax()
    
    def print_infor(self):
        print("")
        print(f"{self.__class__.__name__} current data list = ")
        print(self._operating_filename_list)
        print(self._user_controller_list)
        print(self._operating_user_controller_list)
        print(self._operating_ch_list)
        
    def get_operating_user_controller_list(self):
        return self._view_switch_set.__switch_set
    
    @property
    def view_switch_set(self):
        return self._view_switch_set
    
class TraceAxesController(AxesController):
    def __init__(self, controller, ax):
        super().__init__(controller, ax)
        self.mode = "CH_MODE"  # or "ROI MODE" for showing sigle ch of several ROIs.
        self.ax_update_switch()
     
    def set_view_data(self):
        if self.update_switch is True:
            for controller_key in self._operating_user_controller_list:
                #get data from current user controller
                data_dict = self._main_controller.get_controller_data(controller_key)
                for ch_key in data_dict.keys():
                    data = data_dict[ch_key]
                    if type(data).__name__ == "TraceData":
                        # get a graph
                        ax_data, = data.show_data(self._ax_obj)
                        # color setting
                        if self.mode == "CH_MODE":
                            ax_data.set_color(self._ch_color[ch_key])
                        elif self.mode == "ROI_MODE":
                            ax_data.set_color(self._ch_color[controller_key])
        else:
            pass


class ImageAxesController(AxesController):
    def __init__(self, model, ax):
        super().__init__(model, ax)
        self.mode = None  # no use
        self.ax_update_switch()
        
    def set_click_position(self, event):  
            raise NotImplementedError()
        
    # There are three dict. active_controller_dict is to switching. self._ax_data_dict is to keep ax data. controller_data_dict is from user controller.
    def set_view_data(self):
        if self.update_switch is True:
            for controller_key in self._operating_user_controller_list:
                #get data from current user controller
                data_dict = self._main_controller.get_controller_data(controller_key)
                for ch_key in data_dict.keys():
                    data = data_dict[ch_key]
                    if type(data).__name__ == "ImageData":
                        # get a graph
                        image = data.show_data(self._ax_obj)  # ax_data can use for image setting.
                        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                        print(image.get_zorder())
        else:
            pass
                    
    # override
    def draw_ax(self):
        print(self._marker_obj)
        if self._marker_obj  == {}:
            print("ttttttttttttttttttttttttttttttttttttt")
        else:
            order_box = self._marker_obj["ROI1"].rectangle_obj.get_zorder()
            print("dddddddddddddddddddddddddddddddddd")
            print(order_box)
            self._marker_obj["ROI1"].rectangle_obj.set_zorder(1)
        self.set_view_data()
        self._ax_obj.set_axis_off()
        self.canvas.draw()
        
    # override            
    def update(self):
        if self.update_switch == True:
            self._ax_obj.cla()  # clear ax
            for controller_key in self._operating_user_controller_list:
                for filename_key in self._operating_filename_list:
                    self._main_controller.set_controller_data(controller_key,
                                                         filename_key,
                                                         self._operating_ch_list)
        print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuupdate")
        self.draw_ax()
                 
    def set_roibox(self, controller_key, roi_pos):  # roi[x,y,width,height]. controller_list came from the trace axes
        if controller_key not in self._marker_obj:
            self._marker_obj[controller_key] = RoiBox(roi_pos, self._controller_color[controller_key])
            self._ax_obj.add_patch(self._marker_obj[controller_key].rectangle_obj)
        else:
            self._marker_obj[controller_key].set_roi(roi_pos)
        self.canvas.draw()
        
    # override
    def get_operating_user_controller_list(self):
        return self._view_switch_set.get_true_list("CONTROLLER")


class RoiBox():
    #""" class variable """
    #color_selection = ['white', 'red', 'blue', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'orange']

    #""" instance method """
    def __init__(self, roi_num, color):
        self.__rectangle_obj = patches.Rectangle(xy=(40, 40), 
                                                 width=1, 
                                                 height=1,
                                                 linewidth=0.7,
                                                 ec=color, 
                                                 fill=False)

    def set_roi(self, roi_val):
        x = roi_val[0]
        y = roi_val[1]
        self.__rectangle_obj.set_xy([x, y])
        width = roi_val[2]
        height = roi_val[3]
        self.__rectangle_obj.set_width(width)
        self.__rectangle_obj.set_height(height)
        
    def delete(self):
        raise NotImplementedError()

    @property
    def rectangle_obj(self):
        return self.__rectangle_obj
      

class AxesTools:
    def __init__(self, axes):
        self.axes = axes

    def axes_patches_check(self, target_class):
        target_list = []
        for target in  self.axes.patches:
            if isinstance(target, target_class):
                target_list.append(target)
        return target_list



