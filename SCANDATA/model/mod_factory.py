# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 22:57:01 2023
@author: lunelukkio@gmail.com

When adding a mod, make a new instance of it \ 
and add it to instance of chain of responsibility in ModCliet class.
Also check ModList class in model_main.py
"""

from abc import ABCMeta, abstractmethod
import numpy as np
from SCANDATA.model.value_object import TraceData

"""
Chain of responsibility client
"""

class ModClient:  # Put every mods. Don't need to sepalate mods for each data type..
    def __init__(self, controller_entities):  # data_dict_list = [{data_io}, {data}, {controller}]
        self.mod_list = []
        self.no_mod = NoModHandler()
        self.bg_comp = BgCompMod(controller_entities)  # get controllers rather instead of the entities
        self.df_over_f = DFOverFMod()
        self.normalize = Normalize()
        self.error_mod = ErrorMod()

        # Chain of resonsibility
        self.chain_of_responsibility = self.no_mod. \
                                       set_next(self.bg_comp). \
                                       set_next(self.df_over_f). \
                                       set_next(self.normalize). \
                                       set_next(self.error_mod)
        
    def set_mod(self,data_key, original_data, mod_keys):
        if mod_keys == []:
            mod_trace = self.no_mod.apply_mod(data_key, original_data, None)
        else:
            for key in mod_keys:
                mod_trace = self.no_mod.apply_mod(data_key, original_data, key)
        return mod_trace
    
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
    
    def handle_request(self, data_key, original_data, key):
        if self.__next_handler:
            return self.__next_handler.apply_mod(data_key, original_data, key)
        
        
"""
ConcreteHandler
"""
class NoModHandler(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, data_key, original_data, key):
        if key is None:
            return original_data
        else:
            return super().handle_request(data_key, original_data, key)
                

class BgCompMod(ModHandler):
    def __init__(self, controller_entities):
        super().__init__()
        self.trace_calc = TraceCalculation()
        self.__controller_entities = controller_entities
        self.__roi_num = 1  # This is the roi number for backgrand trace (Roi1)
        
    def apply_mod(self, data_key, original_data, key):
        if key == 'BgComp':
            bg_trace_entitiy = self.__get_bg_trace(data_key)
            bg_comp_trace_obj = self.trace_calc.create_bg_comp(original_data, bg_trace_entitiy.trace_obj)
            return bg_comp_trace_obj
        else:
            return super().handle_request(data_key, original_data, key)
        
    def __get_bg_trace(self, data_key):
        print('Tip: Need refactoring. Now is only for two traces.')
        entities = self.__controller_entities['Roi' + str(self.__roi_num)].observers
        if 'Full' in data_key:
            bg_trace_entity = entities[0]
        elif 'ChTrace' in data_key:
            last_digit = int(data_key[-1])/(len(entities)-1)
            if last_digit % 2 == 0:
                bg_trace_entity = entities[1]
            else:
                bg_trace_entity = entities[2] 
        return bg_trace_entity
    
    def handle_request(self, request):
        if request < 10:
            print("Request {} is handled by ConcreteHandlerA".format(request))
        elif self.next_handler is not None:
            self.next_handler.handle_request(request)


class DFOverFMod(ModHandler):
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        
    def apply_mod(self, data_key, original_data, key):
        if key == 'DFoverF':
            df_over_f = self.trace_calc.create_df_over_f(original_data)
            mod_trace_obj = df_over_f
            return mod_trace_obj
        else:
            return super().handle_request(data_key, original_data, key)
        
class Normalize(ModHandler):
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        
    def apply_mod(self, data_key, original_data, key):
        if key == 'Normalize':
            normalize = self.trace_calc.create_normalize(original_data)
            mod_trace_obj = normalize
            return mod_trace_obj
        else:
            return super().handle_request(data_key, original_data, key)
        
    # This should be in View class?
class Invert(ModHandler):
    pass
    
    
class TraceMovingAveMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, data_key, original_data, key):
        if key == 'MovingAve':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need Moving Average')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(data_key, original_data, key)
    
class FlamesImFilterMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, data_key, original_data, key):
        if key == 'ImFilter':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need imfiler for frames data')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(data_key, original_data, key)

    
class ErrorMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, data_key, original_data, key):
        print('----------------------- !!!!!!!!! --------------------')
        print('There is no such　Mod: ' + str(key))
        print('----------------------- !!!!!!!!! --------------------')
        raise Exception('The end frame should be the same as the frames length or less.')
        
        
"""
Trace modify class
"""
class TraceCalculation:
    def __init__(self): # frames
        self.__average_start = 1  # this is for a F value
        self.__average_length = 4  # This is for a F value
        
    def create_df_over_f(self, trace_obj):
        f = self.f_value(trace_obj)
        df_over_f = (trace_obj/f -1) * 100
        return df_over_f
        
    def f_value(self, trace_obj) -> float: # trace is value object.
        part_trace = trace_obj.data[self.__average_start : self.__average_start + self.__average_length]
        average = np.average(part_trace)
        return average

    def create_new_value_obj(self, val, interval):
        new_obj = TraceData(val, interval)
        return new_obj
    
    def create_normalize(self, trace_obj):
        min_val = np.min(trace_obj.data)
        pre_trace_obj = trace_obj - min_val
        max_val = np.max(pre_trace_obj.data)
        norm_obj = pre_trace_obj/max_val
        return norm_obj
    

    
    def create_bg_comp(self, trace_obj, bg_trace_obj):
            f = self.f_value(trace_obj)


            
            
            
            delta_F_trace = trace_obj - bg_trace_obj
            bg_comp_trace = delta_F_trace + f
            return bg_comp_trace

    