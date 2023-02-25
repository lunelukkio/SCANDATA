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


class BgCompFactory(ModFactory):
    def create_mod(self):
        return BgCompHandler()
    

class DfOverFFactory(ModFactory):
    def create_mod(self):
        return DfOverFHandler()
    

class TraceFilterFactory(ModFactory):
    def create_mod(self):
        return TraceFilterHandler()
    
class FlamesFilterFactory(ModFactory):
    def create_mod(self):
        return FlamesFilterHandler()

    
"""
Handler(Interface)
"""
class ModHandler(metaclass=ABCMeta):
    def __init__(self, name):
        self.__name = name
        self.__next_handler = None

    def set_next_handler(self, handler):
        self.__next_handler = handler
        return self.__next_handler
    
    def hanle_request(self, request):
        pass

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
class BgCompHandler(ModHandler):
    def __init__(self, bg_trace_obj):
        self.name = self.__class__.__name__
        super().__init__(self.name)
        self.bg_trace_obj = self.filter_data(bg_trace_obj)


    def mod_data(self, trace_obj):
        mod_trace_obj = trace_obj - self.bg_trace_obj
        return mod_trace_obj
    
    def filter_data(self, data):
        print('----------------------- !!!!!!!!! --------------------')
        print('Tip Need Filter class for filtering a background trace')
        print('----------------------- !!!!!!!!! --------------------')
        return data
    
    def __str__(self):
    #return "[{0}]".format(self.__name)
        pass
    
    def handle_request(self, request):
        if request < 10:
            print("Request {} is handled by ConcreteHandlerA".format(request))
        elif self.next_handler is not None:
            self.next_handler.handle_request(request)

class DfOverFHandler(ModHandler):
    def __init__(self):
        super(NoSupport, self).__init__(name)
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
        pass
    
    
class TraceFilterHandler(ModHandler):
    def __init__(self):
        pass
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
        pass
    
class FlamesFilterHandler(ModHandler):
    def __init__(self):
        pass
        
    def mod_data(self, trace):
        pass
    
    
    def __str__(self):
        pass