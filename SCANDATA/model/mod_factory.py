# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 22:57:01 2023

@author: lulul
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import ImageData, TraceData
import numpy as np

"From get_data method in DataSet class"
class ModTrace():
    def wrapper(*args,**kwargs):

        raw_data = func(*args,**kwargs)
        
        return raw_data
    return wrapper
    
    
    

"""
Mod Factory
"""
class ModFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_mod(self):
        raise NotImplementedError()


class BackGroundComp(ModFactory):
    def create_mod(self):
        return BackGroundComp()
    
    

class BackGroundComp(ModFactory):
    def create_mod(self):
        return BackGroundComp()
    

class TraceFilterFactory(ModFactory):
    def create_mod(self):
        return TraceFilter()


    

class ModInterface(metaclass=ABCMeta):
    @abstractmethod
    def mod_trace(self):
        raise NotImplementedError()
        
    @abstractmethod
    def __str__(self):
        raise NotImplementedError()
        
        
class BackGroundComp(ModInterface):
    def __init__(self):
        pass
        
    def mod_trace(self, trace):
        pass
    
    
    def __str__(self):
    #return "[{0}]".format(self.__name)
        pass

class DfOverF(ModInterface):
    def __init__(self):
        pass
        
    def mod_trace(self, trace):
        pass
    
    
    def __str__(self):
        pass
    
    
class TraceFilter(ModInterface):
    def __init__(self):
        pass
        
    def mod_trace(self, trace):
        pass
    
    
    def __str__(self):
        pass