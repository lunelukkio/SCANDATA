# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 09:01:53 2023

@author: lunel
"""

from abc import ABCMeta, abstractmethod
import matplotlib.patches as patches
import json


class AxisController(metaclass=ABCMeta):
    def __init__(self, ax, controller):
        self._tools = AxesTools(ax)
        self._ax_obj = ax
        self._data_list = ViewData()
        
        self._main_controller = controller
        
        self._user_controller_list = []  # the list for showing RoiBox including the background ROI.
        self._operating_user_controller_list = []
        
        self._operating_filename_list = []
        self._operating_ch_list = []
        
        self._marker_obj = {}  # This is for makers in axis windows.
        
        self.sync_switch = False  # This switch is to show each data in each controllers.
        self.update_switch = True  # This switch is for avoiding image view update. Ture or False or empty: flip switch.
        
        # color selection for traces and RoiBoxes
        try:
            with open("../setting/axis_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        except:
            with open("./setting/axis_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        self._ch_color = setting.get("ch_color")
        self._controller_color = setting.get("controller_color")
     
    def set_controller_val(self, controller_key, val):  # e.g. val = [x, y, None, None]
        self._main_controller.set_controller_val(controller_key, val)
        print(f"{self._operating_user_controller_list}: ", end='')
            
    def get_controller_val(self):
        for user_controller in self._operating_user_controller_list:
             return self._main_controller.get_controller_val(user_controller)

    @abstractmethod
    def set_view_data(self, active_controller_dict):
            raise NotImplementedError()
    
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
        return self._operating_user_controller_list
    
class TraceAxisController(AxisController):
    def __init__(self, canvas, ax):
        super().__init__(ax)
        self.canvas = canvas
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


class ImageAxisController(AxisController):
    def __init__(self, canvas, ax):
        super().__init__(ax)
        self.canvas = canvas
        self.mode = None  # no use
        
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
                 
    def set_roibox(self, controller_key, roi_pos):  # roi[x,y,width,height]. controller_list came from the trace axis
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


class ViewData:
    def __init__(self):
        user_controller_dict = {}  # {key: bool}
        filename_dict = {}  # {key: bool}
        ch_dict = {}  # {key: bool}
        self.__view_dict = {"CONTROLLER": user_controller_dict,
                            "FILENAME": filename_dict, 
                            "CH": ch_dict}
        
    def set_view_data(self, dict_key, key, val=True):       
        if key in self.__view_dict[dict_key]:
            del self.__view_dict[dict_key][key]
            print(f"Deleted view data {key} in {dict_key}")
        elif key not in self.__view_dict[dict_key]:
            self.__view_dict[dict_key][key] = True
            print(f"Added view data {key} in {dict_key}")

    def set_view_data_val(self, key, val=None):
        if key in self.__view_dict["CONTROLLER"]:
            sub_dict = self.__view_dict["CONTROLLER"]
        elif key in self.__view_dict["FILENAME"]:
            sub_dict = self.__view_dict["FILENAME"]
        elif key in self.__view_dict["CH"]:
            sub_dict = self.__view_dict["CH"]
        else:
            raise Exception("No key in the view data dict")
        if val is not None:
            sub_dict[key] = val
        else:
            sub_dict[key] = not sub_dict[key]
            
    def get_view_data_val(self, key):
        if key in self.__view_dict["CONTROLLER"]:
            view_switch = self.__view_dict["CONTROLLER"][key]
        elif key in self.__view_dict["FILENAME"]:
            view_switch = self.__view_dict["FILENAME"][key]
        elif key in self.__view_dict["CH"]:
            view_switch = self.__view_dict["CH"][key]
        else:
            raise Exception("No key in the view data dict")
        return view_switch

    @property
    def view_dict(self):
        return self.__view_dict
