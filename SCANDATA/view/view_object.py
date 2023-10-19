# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:46:13 2023

@author: lunelukkio@gmail.com
"""


#subscriber of data entities
# RoiView knows the names of traces as self.data_dict{}
class ObjectController:
    def __init__(self, ax, model, color):
        self.__model = model
        self.__user_controller = []
        self.__ax = ax
        self.__color = color
        
        
        
        
        
    def create_data(self, object_num):
        self.__key = 'Roi' + str(object_num)
        self.__entity_name_list = self.__model.create_data('Trace')
        
        for key in self.__entity_name_list:
            self.__data_dict[key] = None
            
        self.__roi_box = RoiBox(self.__model, self.__key)

        print('Created ' + self.__key + ' view instance including Roi controller and traces.')

    def reset(self):
        del self.__data_dict
        del self.__roi_box

    def update(self, *no_use):  # "no_use" is a RoiVal object. it need for FluoTrace observers.
        # update entity list from model controller
        observer_entity_list = []
        for key in self.__model.get_infor(self.__key):  # get only keys which include 'Trace' from DataSet class.
            if 'Trace' in key:
                observer_entity_list.append(key)
        # for traces
        for data_name in observer_entity_list:
            self.__data_dict[data_name] = self.__model.get_data(data_name)
        #for roibox
        self.__roi_box.set_roi()
        self.notify_observer()
        
    def get_data(self) -> dict:
        i = 0
        for data in self.__entity_name_list:
            self.__ax_data_dict['Data' + str(i)] = self.__data_dict[data]
            i += 1
        return self.__ax_data_dict
            
    def delete(self):
        raise NotImplementedError()
    
    def add_observer(self, ax: object):
        self.__ax_observer.add_observer(ax)
        
    def remove_observer(self, ax: object):
        self.__ax_observer.remove_observer(ax)
        
    def notify_observer(self):
        self.__ax_observer.notify_observer()
        
    def print_infor(self):
        raise NotImplementedError()
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name
        
    @property
    def roi_box(self):
        return self.__roi_box
    
    @property
    def sort_num(self):
        return self.__sort_num
    
    @property
    def key(self):
        return self.__key


class RoiBox():
    roi_num = 0
    color_selection = ['white', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    @classmethod
    def get_roi_num(cls):
        return cls.roi_num
    
    @classmethod
    def increase_roi_num(cls):
        cls.roi_num += 1
    
    @classmethod
    def reset(cls):
        cls.roi_num = 0
    
    def __init__(self, model, key):
        self.__model = model
        self.__key = key
        self.color_num = RoiBox.get_roi_num()
        self.__rectangle_obj = patches.Rectangle(xy=(40, 40), 
                                                 width=1, 
                                                 height=1,
                                                 linewidth=0.7,
                                                 ec=RoiBox.color_selection[self.color_num], 
                                                 fill=False)
        RoiBox.increase_roi_num()

    def set_roi(self):
        roi_obj = self.__model.get_data(self.__key)
        self.__rectangle_obj.set_xy([roi_obj.data[0], roi_obj.data[1]])
        self.__rectangle_obj.set_width(roi_obj.data[2])
        self.__rectangle_obj.set_height(roi_obj.data[3])
        
    def delete(self):
        raise NotImplementedError()

    @property
    def rectangle_obj(self):
        return self.__rectangle_obj