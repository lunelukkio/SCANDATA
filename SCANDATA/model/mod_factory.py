# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 22:57:01 2023

@author: lulul
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import ImageData, TraceData
import numpy as np

"""
Chain of responsibility client
"""

class ModClient:  # Put every mods. Don't need to sepalate mods for each data.
    def __init__(self, data_list: list):
        self.__data_list = data_list
        self.mod_list = []
        no_mod = NoModHandler()
        bg_comp = BgCompHandler()
        df_over_f = DfOverFHandler()

        
        # Chain of resonsibility
        self.chain_of_responsibility = no_mod. \
                                       set_next(bg_comp). \
                                       set_next(df_over_f)
        
    def set_mod(self, original_data, mod_switch):
        apply_mod(original_data, mod_switch)
        
    # Not use
    """
    def create_mod(self, mod_factory):
        product = mod_factory.create_mod()
        return product
    """

        

# NOT USE
"""
Mod Factory

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
    
"""
Handler
"""
class Handler(metaclass=ABCMeta):  # Handler interface
    
    @abstractmethod
    def set_next(self, handler):
        pass
    
    @abstractmethod
    def handle_request(self, request):
        pass
        

class ModHandler(Handler):  # BaseHandler
    def __init__(self):
        self.__next_handler = None

    def set_next(self, next_handler):
        self.__next_handler = next_handler
        return next_handler
    
    def handle_request(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)

        return None
        
        
"""
ConcreteHandler
"""
class NoModHandler(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, original_data, mod_switch):
        i = 0
        for mod in self.mod_switch:
            if mod_switch[i] is True:
                return
            else:
                return super().handle_request(request)
                

class BgCompHandler(ModHandler):
    def __init__(self):
        self.name = self.__class__.__name__
        super().__init__(self)
        self.__bg_trace = None
        
    @property
    def bg_trace(self):
        return self.__bg_trace

    @bg_trace.setter
    def bg_trace(self, bg_trace):
        self.__bg_trace = bg_trace
        
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