# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 22:57:01 2023

@author: lulul
"""

from abc import ABCMeta, abstractmethod

"""
Chain of responsibility client
"""

class ModClient:  # Put every mods. Don't need to sepalate mods for each data type..
    def __init__(self):  # data_dict_list = [{data_io}, {data}, {controller}]
        self.mod_list = []
        self.no_mod = NoModHandler()
        self.bg_comp = BgCompMod()
        self.df_over_f = DFOverFMod()

        # Chain of resonsibility
        self.chain_of_responsibility = self.no_mod. \
                                       set_next(self.bg_comp). \
                                       set_next(self.df_over_f)
        
    def set_mod(self, original_data, mod_keys):
        if mod_keys == []:
            mod_trace = self.no_mod.apply_mod(original_data, None)

        else:
            for key in mod_keys:
                mod_trace = self.no_mod.apply_mod(original_data, key)

        return mod_trace
    
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
        return BgCompMod()
    

class DfOverFFactory(ModFactory):
    def create_mod(self):
        return DFOverFMod()
    

class TraceFilterFactory(ModFactory):
    def create_mod(self):
        return TraceFilterMod()
    
class FlamesFilterFactory(ModFactory):
    def create_mod(self):
        return FlamesFilterMod()
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
    
    def handle_request(self, original_data, key):
        if self._next_handler:
            return self._next_handler.apply_mod(original_data, key)
        
        
"""
ConcreteHandler
"""
class NoModHandler(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, original_data, key):
        if key is None:
            return original_data
        else:
            return super().handle_request(original_data, key)
                

class BgCompMod(ModHandler):
    def __init__(self):
        super().__init__()
        self.__bg_trace_entiry = None
        
    def apply_mod(self, original_data, key):
        if key == 'BgComp':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need Filter class for filtering a background trace')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = original_data - self.bg_trace_obj
            return mod_trace_obj
        else:
            return super().handle_request(original_data, key)
        
    @property
    def bg_trace(self):
        return self.__bg_trace

    @bg_trace.setter
    def bg_trace(self, bg_trace_entiry):
        self.__bg_trace_entiry = bg_trace_entiry

    def __str__(self):
    #return "[{0}]".format(self.__name)
        pass
    
    def handle_request(self, request):
        if request < 10:
            print("Request {} is handled by ConcreteHandlerA".format(request))
        elif self.next_handler is not None:
            self.next_handler.handle_request(request)


class DFOverFMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, original_data, key):
        if key == 'DFoverF':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need DF over F calculation')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(original_data, key)
    
    
class TraceMovingAveMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, original_data, key):
        if key == 'MovingAve':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need Moving Average')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(original_data, key)
    
class FlamesImFilterMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, original_data, key):
        if key == 'ImFilter':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need imfiler for frames data')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(original_data, key)