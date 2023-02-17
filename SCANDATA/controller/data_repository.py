# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:13:56 2023

lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
from matplotlib.figure import Figure
import matplotlib.patches as patches


class ViewDataRepository:
    def __init__(self):
        self.model = None     
        self.__view_data_counter = {}  # dict
        self.__view_data = {}  # dict
    """    
    def create_view_data(self, factory_type):
        new_roi_view = factory_type.create_view_data(self.model)
        self.view_data.append(new_roi_view)
        return new_roi_view
    """
    
    def create_view_data(self,  factory_type):
        product = factory_type.create_view_data(self.model)
        object_name = product.__class__.__name__  # str
        
        last_num = self.__view_data_counter.get(object_name, 0)  # Get counter num of instance. If not exist, num is 0.
        new_num = last_num + 1
        product.name = object_name + str(new_num)
        product.create_data(new_num)
        
        #store in this class
        self.__view_data_counter[object_name] = new_num  # Add key and object_num to a counter dict. ex{RoiView: 1}
        self.__view_data[object_name + str(new_num)] = product
        return product

    def show_data(self):
        print('View Data = ' + str(list(self.__view_data)))


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
    def create_view_data(self, model):
        return RoiView(model)
        
class ImageViewFactory(ViewDataFactory):
    def create_view_data(self, model):
        return ImageView(model)

class ElecViewFactory(ViewDataFactory):
    def create_view_data(self, model):
        return ElecView(model)
    
    
"""
abstract product
"""
class ViewData(metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()
        
    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
        
    @abstractmethod
    def delete(self):
        raise NotImplementedError()

    @abstractmethod
    def add_observer(self, ax: object):
        raise NotImplementedError()

    @abstractmethod
    def remove_observer(self, ax: object):
        raise NotImplementedError()
        
    @abstractmethod
    def notify_observer(self, ax: object):
        raise NotImplementedError()
        
    @abstractmethod
    def print_infor(self):
        raise NotImplementedError()
        
"""
concrete product
"""

#subscriber of data entities
class RoiView(ViewData):
    def __init__(self, model):
        self.__name = None
        self.__model = model
        self.__ax_observer = Observer(self)
        
    def create_data(self, object_num):
        self.__key = 'Roi' + str(object_num)
        self.__model.create_data('Trace')
        self.__roi_val = self.__model.get_data(self.__key)
        self.__roi_box = RoiBox()
        self.__data_name_list = self.__model.get_infor(self.__key)
        self.__data_list = []  # a list of value object 
        self.update()
        
        print('Created ' + self.__key + ' view instance including Roi controller and traces.')

    def reset(self):
        raise NotImplementedError()

    def update(self):
        new_data = []
        for data_name in self.__data_name_list:
            new_data.append(self.__model.get_data(data_name))
        self.__data_list = new_data
        self.__ax_observer.notify_observer()
        
    def get_data(self) -> list:
        return self.__data_list
            
    def delete(self):
        pass
    
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


class ImageView(ViewData):
    def __init__(self, model):
        self.__name = None
        self.__model = model
        self.__ax_observer = Observer(self)
        
    def create_data(self, object_num):
        self.__key = 'FrameWindow' + str(object_num)
        self.__model.create_data('Image')
        self.__frame_windoww_val = self.__model.get_data(self.__key)
        self.__data_name_list = self.__model.get_infor(self.__key)
        self.__data_list = []  # a list of value object 
        self.update()

    def reset(self):
        raise NotImplementedError()

    def update(self):
        new_data = []
        for data_name in self.__data_name_list:
            new_data.append(self.__model.get_data(data_name))
        self.__data_list = new_data
        print('View Data updated')
        self.__ax_observer.notify_observer()
        
    def get_data(self) -> list:
        return self.__data_list
        
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
        

class ElecView(ViewData):
    def __init__(self, model):
        self.__name = None
        self.__model = model
        self.__ax_observer = Observer(self)
        
    def create_data(self, object_num):
        self.__key = 'ElecController' + str(object_num)
        self.__model.create_data('Elec')
        self.__time_windoww_val = self.__model.get_data(self.__key)
        self.__data_name_list = self.__model.get_infor(self.__key)
        self.__data_list = []  # a list of value object 
        self.update()
    
    def reset(self):
        raise NotImplementedError()

    def update(self):
        new_data = []
        for data_name in self.__data_name_list:
            new_data.append(self.__model.get_data(data_name))
        self.__data_list = new_data
        self.__ax_observer.notify_observer()
        
    def get_data(self) -> list:
        return self.__data_list
        
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
        
        
        
class RoiBox():
    roi_num = 0
    color_selection = ['white', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        
    def __init__(self):
        RoiBox.roi_num += 1
        self.__roi_num = RoiBox.roi_num
        self.__rectangle_obj = patches.Rectangle(xy=(40, 40), 
                                                 width=1, 
                                                 height=1, 
                                                 ec=RoiBox.color_selection[self.__roi_num - 1], 
                                                 fill=False)

    def set_roi(self):
        roi_obj = self.__roi_holder.get_controller(self.__filename.name, 'Roi' + str(self.__roi_num))
        self.__rectangle_obj.set_xy([roi_obj.data[0], roi_obj.data[1]])
        self.__rectangle_obj.set_width(roi_obj.data[2])
        self.__rectangle_obj.set_height(roi_obj.data[3])    
        
    def show_data(self, ax):
        ax.add_patch(self.__rectangle_obj)
        
        
        
class Observer:
    def __init__(self, view_data):
        self.view_data = view_data
        self.__observers = []
        
    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        for observer_name in self.__observers:
            observer_name.update(self.view_data)
        print('Notified to ax.')
        
        
    @property
    def observers(self):
        return self.__observers