# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 22:57:01 2023

@author: lulul
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import ImageData, TraceData
import numpy as np

    

"""
Mod Factory
"""
class ModFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_mod(self):
        raise NotImplementedError()


class BackGroundCompFactory(ModFactory):
    def create_mod(self):
        return BackGroundComp()
    

class DfOverFFactory(ModFactory):
    def create_mod(self):
        return BackGroundComp()
    

class TraceFilterFactory(ModFactory):
    def create_mod(self):
        return TraceFilter()
    
class FlamesFilterFactory(ModFactory):
    def create_mod(self):
        return FlamesFilter()

    
"""
Handler(Interface)
"""
class ModInterface(metaclass=ABCMeta):
    def __init__(self):
        self.__name = self.__class__.__name__
        self.__next = None

    def setNext(self, next):
        self.__next = next
        return next

    def support(self, trouble):
        if self.resolve(trouble):
            self.done(trouble)
        elif self.__next is not None:
            self.__next.support(trouble)
        else:
            self.fail(trouble)

    @abstractmethod
    def mod_data(self, trouble):
        pass

        
        
        
"""
ConcreteHandler
"""
class BackGroundComp(ModInterface):
    def __init__(self, name):
        super(NoSupport, self).__init__(name)

    def resolve(self, trouble):
        return False
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
    #return "[{0}]".format(self.__name)
        pass

class DfOverF(ModInterface):
    def __init__(self):
        pass
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
        pass
    
    
class TraceFilter(ModInterface):
    def __init__(self):
        pass
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
        pass
    
class FlamesFilter(ModInterface):
    def __init__(self):
        pass
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
        pass