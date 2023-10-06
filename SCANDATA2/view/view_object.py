# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:46:13 2023

@author: lunelukkio@gmail.com
"""

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