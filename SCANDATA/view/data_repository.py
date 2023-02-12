# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:13:56 2023

lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod


"""
abstract factory
"""
class DataRepositoryFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_data_repository(self):
        raise NotImplementedError()


"""
contrete factory
"""
class RoiRepositoryFactory(DataRepositoryFactory):
    def create_data_repository(self):
        return RoiRepository()
        
class ImageRepositoryFactory(DataRepositoryFactory):
    def create_data_repository(self):
        return ImageRepository()

class ElecRepositoryFactory(DataRepositoryFactory):
    def create_data_repository(self):
        return ElecRepository()
    
    
"""
abstract product
"""
class DataRepository(metaclass=ABCMeta):
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

class RoiRepository(DataRepository):
    def __init__(self, trace_data: object):
        self.__roi_val = contoller.create_
        self.__trace_data = []
        self.__roi_box = RoiBox(filename, controller, ax)
        self.__window = []
        self.__ax
        
    def print_infor(self):
        raise NotImplementedError()
    

    def reset(self):
        raise NotImplementedError()


    def update(self):
        raise NotImplementedError()


class ImageRepository(DataRepository):
    def print_infor(self):
        raise NotImplementedError()
    

    def reset(self):
        raise NotImplementedError()


    def update(self):
        raise NotImplementedError()

class ElecRepository(DataRepository):
    def print_infor(self):
        raise NotImplementedError()
    

    def reset(self):
        raise NotImplementedError()


    def update(self):
        raise NotImplementedError()
        
        
        
class RoiBox():
    object_num = 0  # class variable 
    color_selection = ['white', 'red', 'blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        
    def __init__(self, filename, controller, ax):
        self.__filename = filename
        self.__roi_holder = controller
        RoiBox.object_num += 1
        self.__roi_num = copy.deepcopy(RoiBox.object_num)
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