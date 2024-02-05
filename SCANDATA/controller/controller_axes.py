# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 09:01:53 2023

@author: lunel
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.common_class import Switch_dict, DictTools
import matplotlib.patches as patches
import json


class AxesController(metaclass=ABCMeta):
    def __init__(self, model, canvas, ax):
        self._tools = AxesTools(ax)
        self._canvas = canvas
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
            
    def set_switch(self, controller_key, ch_key, bool_val):
            self._view_switch_set.set_val(controller_key, ch_key, bool_val)
     
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

    def ax_update_enable(self, val=None) -> None:
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
        print(f"{self.__class__.__name__} current data list = ")
        self._view_switch_set.print_infor()

    @property
    def view_switch_set(self):
        return self._view_switch_set
    
class TraceAxesController(AxesController):
    def __init__(self, model, canvas, ax):
        super().__init__(model, canvas, ax)
        self.mode = "CH_MODE"  # or "ROI MODE" for showing sigle ch of several ROIs.
     
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
    def __init__(self, model, canvas, ax):
        super().__init__(model, canvas, ax)
        self.mode = None  # no use
        
    def set_click_position(self, event):  
            raise NotImplementedError()
        
    # There are three dict. active_controller_dict is to switching. self._ax_data_dict is to keep ax data. controller_data_dict is from user controller.
    def set_view_data(self):
        filename_dict = self._view_switch_set.get_filename_dict()
        view_switch_dict = self._view_switch_set.get_dict()
        filename_key_list = [filename_key 
                                 for filename_key, bool_val 
                                 in filename_dict.items() 
                                 if bool_val]
        for filename_key in filename_key_list:
            # get only True user controller switch from the dict.
            for controller_key in view_switch_dict.keys():
                ch_data_dict = self._model.get_data(filename_key, controller_key)
                
                # get only True ch data switch from the dict.
                ch_key_list = [ch_key 
                                     for ch_key, bool_val 
                                     in view_switch_dict[controller_key].items() 
                                     if bool_val]
                # Model can recieve not only data_list but also individual ch_key directly.
                for ch_key in ch_key_list:
                    value_data = ch_data_dict[ch_key]
                    image = value_data.show_data(self._ax_obj)
                    print("image order in matplotlib")
                    print(image.get_zorder())

        
    def set_marker(self, controller_key):
        print(controller_key)
        if "ROI" not in controller_key:
            return
        view_switch_dict = self._view_switch_set.get_dict()
            # get only True user controller switch from the dict.
        check_true = DictTools.find_true_controller_key(view_switch_dict[controller_key])
        print(check_true)
        
        
        print("ttttttttttttttttttttttttttttttttttttt")
        
        if check_true is not None:
            if controller_key in self._marker_obj:
                roi_val = self._model.get_controller_val(controller_key)
                self._marker_obj[controller_key].set_roi(roi_val.data)
                
            else:
                self._marker_obj[controller_key] = RoiBox(self._controller_color[controller_key])
        else:
            order_box = self._marker_obj["ROI1"].rectangle_obj.get_zorder()
            print("dddddddddddddddddddddddddddddddddd")
            print(order_box)
            self._marker_obj["ROI1"].rectangle_obj.set_zorder(1)
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        print(self._marker_obj)
        self._ax_obj.set_axis_off()
        self.canvas.draw()

    # override    shold be in main conrtoller         
    def update(self) -> None:
        if self.update_switch is True:
            self.set_view_data()  # This belong to Image Controller
            print("Skip ROI BOX draw. it should be controlled by trace axes")
            #self.set_marker() # This belong to ROI
            self._ax_obj.set_axis_off()
            self.canvas.draw()

                 
    def set_roibox(self, controller_key, roi_pos):  # roi[x,y,width,height]. controller_list came from the trace axes
        if controller_key not in self._marker_obj:
            self._marker_obj[controller_key] = RoiBox(roi_pos, self._controller_color[controller_key])
            self._ax_obj.add_patch(self._marker_obj[controller_key].rectangle_obj)
        else:
            self._marker_obj[controller_key].set_roi(roi_pos)
        self.canvas.draw()


class RoiBox():
    #""" class variable """
    #color_selection = ['white', 'red', 'blue', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'orange']

    #""" instance method """
    def __init__(self, color):
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



