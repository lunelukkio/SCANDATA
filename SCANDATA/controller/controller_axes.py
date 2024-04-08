# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 09:01:53 2023

@author: lunel
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.common_class import FlagDict
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
#import matplotlib.patches as patches
#from matplotlib.image import AxesImage
import json


class AxesController(metaclass=ABCMeta):
    def __init__(self, main_controller, model, canvas, ax):
        self._tools = AxesTools(ax)
        self._canvas = canvas
        self._ax_obj = ax
        self._main_controller = main_controller
        self._model = model
        
        self.ax_item_list = {}  # {ch_key: plot from value_obj, }
        self._marker_obj = {}  # This is for makers in axes windows.
        
        self._view_flag_set = FlagDict()  # see comon class
        self.update_flag = False  #  Ture or False or empty: flip flag.
        self.update_flag_lock = False # to skip ImageAxe update
        
        # color selection for traces and RoiBoxes
        try:
            with open("../setting/axes_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        except:
            with open("./setting/axes_data_setting.json", "r") as json_file:
                setting = json.load(json_file)
        self._ch_color = setting.get("ch_color")
        self._controller_color = setting.get("controller_color")
            
    def set_flag(self, controller_key, ch_key, bool_val):
        self._view_flag_set.set_val(controller_key, ch_key, bool_val)
        
    def next_controller_to_true(self, controller):
        self._view_flag_set.next_controller_to_true(controller)
        
    def get_canvas_axes(self):
        return self._canvas, self._ax_obj
     
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

    def update_flag_lock_sw(self, val=None) -> None:
        if val is True:
            self.update_flag_lock = True
        elif val is False:
            self.update_flag_lock = False
        else:
            self.update_flag_lock = not self.update_flag_lock
       
    # update flag from the UserController classes in the model
    def set_update_flag(self, update_flag):
        if self.update_flag_lock == True:
            pass
        else:
            self.update_flag = update_flag
       
    @abstractmethod
    def update(self):  # It is overrided by ImageAx
        raise NotImplementedError()
    
    def print_infor(self):
        print(f"{self.__class__.__name__} current data list = ")
        self._view_flag_set.print_infor()

    @property
    def view_flag_set(self):
        return self._view_flag_set
    
class TraceAxesController(AxesController):
    def __init__(self, main_controller, model, canvas, ax):  # controller is for getting ROI information from FLU-AXES.
        super().__init__(main_controller, model, canvas, ax)
        self.mode = "CH_MODE"  # or "ROI MODE" for showing sigle ch of several ROIs.
     
    def set_view_data(self):
        filename_true_dict = self._view_flag_set.find_true_filename_keys()
        controller_true_dict = self._view_flag_set.find_true_controller_keys()
        for filename_key in filename_true_dict:
            # get only True user controller flag from the dict.
            for controller_key in controller_true_dict:
                ch_data_dict = self._model.get_data(filename_key, controller_key)
                if ch_data_dict is None:
                    print("Ch data dict is None")
                    return
                # get only True ch data flag from the dict.
                ch_true_list = self._view_flag_set.find_true_ch_keys(controller_key)
                # Model can recieve not only data_list but also individual ch_key directly.
                for ch_key in ch_true_list:
                    if ch_key not in ch_data_dict:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print("No data. Check the opperating controller list in the ControllerMain Class")
                    else:
                        ax_data = ch_data_dict[ch_key].show_data(self._ax_obj)
                        self.ax_item_list[ch_key] = ax_data
                        # color setting
                        if self.mode == "CH_MODE":
                            ax_data.setPen(pg.mkPen(color=self._ch_color[ch_key]))
                        elif self.mode == "ROI_MODE":
                            ax_data.setPen(pg.mkPen(color=self._ch_color[controller_key]))
            
    def set_marker(self):
        # get flag data from FLUO_AXES
        image_canvas, image_axes = self._main_controller.get_canvas_axes("IMAGE_AXES")
        # get a true flag list
        true_controller = self._view_flag_set.find_true_controller_keys()
        roi_true_controller = [key for key in true_controller if "ROI" in key]
        for controller_key in roi_true_controller:          
            roi_val = self._model.get_controller_val(controller_key).data
            # adjust for image data pixels 0.5
            box_pos = [roi_val[0], 
                      roi_val[1], 
                      roi_val[2], 
                      roi_val[3]]
            if controller_key in self._marker_obj:
                self._marker_obj[controller_key].set_roi(box_pos)
            else:                     
                self._marker_obj[controller_key] = RoiBox(self._controller_color[controller_key])
                self._marker_obj[controller_key].set_roi(box_pos)
                # put the ROI BOX on the top of images.
                self._marker_obj[controller_key].rectangle_obj.setZValue(1)
                image_axes.addItem(self._marker_obj[controller_key].rectangle_obj)
    
    # override
    def update(self):  # It is overrided by ImageAx
        if self.update_flag is True:
            self._ax_obj.clear()
            self._ax_obj.setBackground('w')
            self.set_view_data()  # See each subclass.
            self.set_marker() # for ROIBOX
            self._ax_obj.autoRange()
        else:
            pass


class ImageAxesController(AxesController):
    def __init__(self,main_controller, model, canvas, ax):
        super().__init__(main_controller, model, canvas, ax)
        self.mode = None  # no use
        
    def set_click_position(self, event):  
            raise NotImplementedError()
        
    # There are three dict. active_controller_dict is to flaging. self._ax_data_dict is to keep ax data. controller_data_dict is from user controller.
    def set_view_data(self):
        filename_true_dict = self._view_flag_set.find_true_filename_keys()
        controller_true_dict = self._view_flag_set.find_true_controller_keys()
        for filename_key in filename_true_dict:
            # get only True user controller flag from the dict.
            for controller_key in controller_true_dict:
                ch_data_dict = self._model.get_data(filename_key, controller_key)
                # get only True ch data flag from the dict.
                ch_true_list = self._view_flag_set.find_true_ch_keys(controller_key)
                # Model can recieve not only data_list but also individual ch_key directly.
                for ch_key in ch_true_list:
                    value_data = ch_data_dict[ch_key]
                    value_data.show_data(self._ax_obj)
                    self.ax_item_list[ch_key] = value_data

    # override    shold be in main conrtoller         
    def update(self) -> None:
        if self.update_flag is True:
            # delete old image objects
            self.ax_item_list = {}
            self.set_view_data()  # This belong to Image Controller
        else:
            pass


class RoiBox():
    #""" class variable """
    #color_selection = ['white', 'red', 'blue', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'orange']

    #""" instance method """
    def __init__(self, color):
        self.__rectangle_obj = QtWidgets.QGraphicsRectItem(40, 40, 1, 1)
        self.__rectangle_obj.setPen(pg.mkPen(color=color, width=0.7))
        self.__rectangle_obj.setBrush(pg.mkBrush(None))

    def set_roi(self, roi_val):
        x, y, width, height = roi_val
        self.__rectangle_obj.setRect(x, y, width, height)
        
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



