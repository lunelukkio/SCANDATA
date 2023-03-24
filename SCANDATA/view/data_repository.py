# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:13:56 2023

lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
import matplotlib.patches as patches
import gc


class ViewDataRepository:
    def __init__(self):
        RoiBox.reset()  # for reset RoiBox color
        self.model = None     
        self.__view_data_counter = {}  # dict
        self.__view_data = {}  # dict

        
    def initialize_view_data_repository(self, ax_list):
        # default data
        self.create_image(ax_list)
        self.create_roi(ax_list)  # for backgound compensation
        self.create_roi(ax_list)  # for trace analysing red ROI
        self.create_elec(ax_list)
            
        print('View Data = ' + str(list(self.__view_data)))
    
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
        
    def create_image(self, ax_list):
        image = self.create_view_data(ImageViewFactory())
        image.add_observer(ax_list[0])  # for cell image
        frame_window_name = 'FrameWindow' + str(self.count_data('ImageView'))
        self.model.bind_view(frame_window_name, image)
    
    def create_roi(self, ax_list):
        roi_view = self.create_view_data(RoiViewFactory())  # This is Roi1 for background
        roi_view.add_observer(ax_list[0])  # Add axes to RoiView observer for roi
        roi_view.add_observer(ax_list[1])  # Add axes to RoiView observer for trace
        roi_name = 'Roi' + str(self.count_data('RoiView'))
        self.model.bind_view(roi_name, roi_view)  # Add RoiView to Roi class
        
    def create_elec(self, ax_list):
        elec = self.create_view_data(ElecViewFactory())
        elec.add_observer(ax_list[2])  # fof elec data
        elec_name = 'ElecController' + str(self.count_data('ElecView'))
        self.model.bind_view(elec_name, elec)
        
    def delete_roi(self, ax_list):
        roi_num = self.__view_data_counter['RoiView']
        del_obj = self.__view_data['RoiView' + str(roi_num)]
        DeleteObj.del_object(del_obj)
        self.__view_data_counter['RoiView'] -= 1
        print('Tip Need to fix bugs!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        
    def update(self, key):
        self.__view_data[key].notify_observer()
        
    def set_data(self, key: str, val: list):
        self.__view_data[key].set_data(val)
        
    def count_data(self, key):
       return self.__view_data_counter[key]
   
    def delete(self):
        for view_data in self.__view_data.values():  # get values from dict
            view_data.delete()
            
    @property
    def view_data_counter(self):
        return self.__view_data_counter


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
        self.__sort_num = 901  # to sort view object and data object in observers of model controllers.
        
    def create_data(self, object_num):
        self.__key = 'Roi' + str(object_num)
        self.__model.create_data('Trace')
        self.__roi_box = RoiBox(self.__model, self.__key)
        self.__data_list = []  # a list of value object 
        
        print('Created ' + self.__key + ' view instance including Roi controller and traces.')

    def reset(self):
        del self.__data_list
        del self.__roi_box

    def update(self, *no_use):  # "no_use" is a RoiVal object. it need for FluoTrace observers.
        # update Trace list from model controller
        observer_trace_list = []
        for key in self.__model.get_infor(self.__key):  # get only keys which include 'Trace' from DataSet class.
            if 'Trace' in key:
                observer_trace_list.append(key)
        # for traces
        new_data = []
        for data_name in observer_trace_list:
            new_data.append(self.__model.get_data(data_name))
        self.__data_list = new_data
        #for roibox
        self.__roi_box.set_roi()
        self.notify_observer()
        
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
        
    @property
    def roi_box(self):
        return self.__roi_box
    
    @property
    def sort_num(self):
        return self.__sort_num


class ImageView(ViewData):
    def __init__(self, model):
        self.__name = None
        self.__model = model
        self.__ax_observer = Observer(self)
        self.__sort_num = 902
        
    def create_data(self, object_num):
        self.__key = 'FrameWindow' + str(object_num)
        self.__model.create_data('Image')
        self.__frame_windoww_val = self.__model.get_data(self.__key)
        self.__data_name_list = self.__model.get_infor(self.__key)  # FrameWindow obserber names
        self.__data_list = []  # a list of value object 

    def reset(self):
        raise NotImplementedError()

    def update(self, *no_use):
        new_data = []
        new_data_name = []
        for data_name in self.__data_name_list:
            value_data_obj = self.__model.get_data(data_name)
            new_data.append(value_data_obj)
            new_data_name.append(value_data_obj.data_type)
        self.__data_list = new_data
        
        #print('ImageView Data updated: ' + str(new_data_name))
        self.notify_observer()
        
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
    
    @property
    def sort_num(self):
        return self.__sort_num


class ElecView(ViewData):
    def __init__(self, model):
        self.__name = None
        self.__model = model
        self.__ax_observer = Observer(self)
        self.__sort_num = 903
        
    def create_data(self, object_num):
        self.__key = 'ElecController' + str(object_num)
        self.__model.create_data('Elec')
        self.__data_list = []  # a list of value object 
        
        print('Created ' + self.__key + ' View instance.')
    
    def reset(self):
        del self.__data_list

    def update(self, *no_use):
        # update Elec list from model controller
        observer_trace_list = []
        for key in self.__model.get_infor(self.__key):  # get only keys which include 'Trace' from DataSet class.
            if 'ChElec' in key:
                observer_trace_list.append(key)
        # for traces
        new_data = []
        for data_name in observer_trace_list:
            new_data.append(self.__model.get_data(data_name))
        self.__data_list = new_data

        self.notify_observer()
        
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
    
    @property
    def sort_num(self):
        return self.__sort_num
        
        
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
        
        
class Observer:
    def __init__(self, view_data):
        self.view_data = view_data
        self.__observers = []
        
    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)
    
    def notify_observer(self):
        name_list = []
        for name in self.__observers:
            name_list.append(name.__class__.__name__)
        print('..... Notify to ax: ' + str(name_list))
        for observer_name in self.__observers:
            observer_name.update(self.view_data)

    @property
    def observers(self):
        return self.__observers
    
class DeleteObj:  # from ChatGPT
    @staticmethod
    def del_object(obj):
        """
        Delete an object and all other objects that refer to it
        """
        # Find all objects that refer to the given object
        referrers = gc.get_referrers(obj)

        # Add the object itself to the list of objects to delete
        to_del = [obj]

        # Add all objects that refer to the given object to the list of objects to delete
        for referrer in referrers:
            if hasattr(referrer, '__dict__'):
                for key, value in referrer.__dict__.items():
                    if value is obj:
                        to_del.append(referrer.__dict__[key])
            elif isinstance(referrer, list):
                for i in range(len(referrer)):
                    if referrer[i] is obj:
                        to_del.append(referrer[i])
            elif isinstance(referrer, dict):
                for key, value in referrer.items():
                    if value is obj:
                        to_del.append(referrer[key])

        # Delete all objects in the list of objects to delete
        for obj in to_del:
            del obj
    
        # Run garbage collection to clean up any remaining references
        gc.collect()