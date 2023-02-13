# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:13:56 2023

lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod



class ViewDataRepository:
    def __init__(self):
        self.model = None
        self.view_data = []
        
    def create_view_data(self, factory_type, key: str):
        self.view_data.append(factory_type.create_view_data(self.model, key))


"""
abstract factory
"""

class ViewDataFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_view_data(self):
        raise NotImplementedError()


"""
contrete factory
"""
class RoiViewFactory(ViewDataFactory):
    def create_view_data(self, model, key: str):
        return RoiView(model, key)
        
class ImageViewFactory(ViewDataFactory):
    def create_view_data(self, model, key: str):
        return ImageView(model, key)

class ElecViewFactory(ViewDataFactory):
    def create_view_data(self, model, key:str):
        return ElecView(model, key)
    
    
"""
abstract product
"""
class ViewData(metaclass=ABCMeta):
    @abstractmethod
    def print_infor(self):
        raise NotImplementedError()
    
    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()
        
        
"""
concrete product
"""

#subscriber of data entities
class RoiView(ViewData):
    def __init__(self, model, key: str):
        self.__key = key
        self.__model = model
        self.__roi_val = self.__model.get_data(self.__key)
        self.__roi_box = RoiBox(ax)
        
        self.__window_observers = []
        self.__ax
        self.__trace_data = []  # a list of value object 
        
    def print_infor(self):
        raise NotImplementedError()
    

    def reset(self):
        raise NotImplementedError()


    def update(self):
        raise NotImplementedError()


class ImageView(ViewData):
    def print_infor(self):
        raise NotImplementedError()
    

    def reset(self):
        raise NotImplementedError()


    def update(self):
        raise NotImplementedError()

class ElecView(ViewData):
    def print_infor(self):
        raise NotImplementedError()
    

    def reset(self):
        raise NotImplementedError()


    def update(self):
        raise NotImplementedError()
        
        
        
class RoiBox():
    color_selection = ['white', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        
    def __init__(self, ax):
        self.__rectangle_obj = patches.Rectangle(xy=(40, 40), 
                                                 width=1, 
                                                 height=1, 
                                                 ec=RoiBox.color_selection[self.__roi_num - 1], 
                                                 fill=False)
        ax.add_patch(self.__rectangle_obj)

    def set_roi(self):
        roi_obj = self.__roi_holder.get_controller(self.__filename.name, 'Roi' + str(self.__roi_num))
        self.__rectangle_obj.set_xy([roi_obj.data[0], roi_obj.data[1]])
        self.__rectangle_obj.set_width(roi_obj.data[2])
        self.__rectangle_obj.set_height(roi_obj.data[3])    
        
        
        
        
""" no use """
class RoiVienoUse:
    roi_num = 0
    def __init__(self, filename):
        RoiView.roi_num += 1
        self.__filename = filename

        self.__roi_num = copy.deepcopy(RoiView.roi_num)
        self.__ax = []
        self.__roi = []
        self.__roi_val = 0
        self.__roi_box = []
        self.__trace = []
        
    def add_ax(self, ax: object):
        self.__ax.append(ax)
        
    def delete_ax(self, ax: object):
        self.__ax.remove(ax)
        
    def add_roi(self, key: str):
        self.__roi.append(key)
        
    def delete_roi(self, key: str):
        self.__roi.remove(key)

    def get_roi_val(self):
        pass
    
    def add_roi_box(self, roi_box: str):
        self.__roi_box.append(roi_box)
        
    def delete_roi_box(self, roi_box: str):
        self.__roi_box.remove(roi_box)
    
    def add_trace(self, key: str):
        self.__trace.append(key)
        
    def delete_trace(self, key: str):
        self.__trace.remove(key)
        
    def show_data(self, ax, data_type):
        value_obj = self.controller.get_data(self.__filename, data_type)
        try:
            line_2d, = value_obj.show_data(ax)  # line, mean the first element of a list (convert from list to objet)
            self.trace_y1.append(line_2d)  # Add to the list for trace_y1 trace line objects [Line_2D] of axis abject
        except:
            value_obj.show_data(ax)