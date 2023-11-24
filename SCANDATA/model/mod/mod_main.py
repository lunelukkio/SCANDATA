# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:49:05 2023

@author: lunelukkio@gmail.com
"""
import numpy as np
from SCANDATA.model.value_object import TraceData

"""
Chain of responsibility client
"""

class ModService:  # Put every mods. Don't need to sepalate mods for each data type..
    def __init__(self):
        self.__mod_list = []
        
        self.bg_comp = BgCompMod() 
        self.df_over_f = DFOverFMod()
        self.normalize = Normalize()
        self.error_mod = ErrorMod()

        # Chain of resonsibility
        self.chain_of_responsibility = self.bg_comp. \
                              set_next(self.df_over_f). \
                              set_next(self.normalize). \
                              set_next(self.error_mod)
                              
    def set_dict_mod(self, mod_keys: list, data_dict: dict, filename_key):
        print("ModService.set_dict_mod: Need refactoring. delete filename_key")
        mod_data_dict = {filename_key:{}}
        for data_key in data_dict[filename_key].keys():
            mod_data = self.set_mod(mod_keys, data_dict[filename_key][data_key], data_key)
            mod_data_dict[filename_key][data_key] = mod_data
            print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            print(data_key)
            print(mod_data_dict)
        return mod_data_dict
        
    def set_mod(self, mod_keys, original_data, data_key):
        if mod_keys == []:
            mod_data = original_data
        else:
            for mod_key in mod_keys:
                mod_data = self.bg_comp.apply_mod(mod_key, original_data, data_key)
        return mod_data

    def set_mod_val(self, mod_key, controller_key, filename_key):
        # This need refactoring. self,bg_comp shold be gotton by mod finding method.
        self.bg_comp.set_mod_val(controller_key, filename_key)
        
    def get_mod_list(self):
        return self.__mod_list
    
    def set_mod_list(self, mod_key):
        self.__mod_list.append(mod_key)
        
"""
Handler
"""
# super class
class ModHandler:  # BaseHandler
    def __init__(self):
        self.__next_handler = None

    def set_next(self, next_handler):
        self.__next_handler = next_handler
        return next_handler
    
    def handle_request(self, mod_key, original_data, data_key,):
        if self.__next_handler:
            return self.__next_handler.apply_mod(mod_key, original_data, data_key,)


"""
ConcreteHandler
"""

class BgCompMod(ModHandler):
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        self.bg_roi = None
        self.__bg_dict = None
        
    def apply_mod(self, mod_key, original_data, data_key):
        mod_key = mod_key.upper()
        if mod_key == 'BGCOMP':
            bg_trace = self.__get_bg_trace(data_key)
            bg_comp_trace_obj = self.trace_calc.create_bg_comp(original_data, bg_trace)
            return bg_comp_trace_obj
        else:
            return super().handle_request(mod_key, original_data, data_key,)
        
    def __get_bg_trace(self, data_key):
        if data_key in self.__bg_dict:
            bg_trace = self.__bg_dict[data_key]
        else:
            print(f"There is no {data_key} in the background dict.")
            bg_trace = None
        return bg_trace
    
    def set_bg_roi(self, bg_roi):
        self.bg_roi = bg_roi
    
    def handle_request(self, request):
        if request < 10:
            print("Request {} is handled by ConcreteHandlerA".format(request))
        elif self.next_handler is not None:
            self.next_handler.handle_request(request)
            
    def set_mod_val(self, controller_key: str, filename_key):
         controller_dict =  self.bg_roi.get_controller_data()
         self.__bg_dict = controller_dict[filename_key]


class DFOverFMod(ModHandler):
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        
    def apply_mod(self, mod_key, original_data, data_key,):
        mod_key = mod_key.upper()
        if mod_key == 'DFOVERF':
            df_over_f = self.trace_calc.create_df_over_f(original_data)
            mod_trace_obj = df_over_f
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, original_data, data_key,)
        
        
class Normalize(ModHandler):
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        
    def apply_mod(self, mod_key, original_data, data_key,):
        mod_key = mod_key.upper()
        if mod_key == 'NORMALIZE':
            normalize = self.trace_calc.create_normalize(original_data)
            mod_trace_obj = normalize
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, original_data, data_key,)
        
        
    # This should be in View class?
class Invert(ModHandler):
    pass
    
    
class TraceMovingAveMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, mod_key, original_data, data_key,):
        mod_key = mod_key.upper()
        if mod_key == 'MOVINGAVE':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need Moving Average')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, original_data, data_key,)
    
    
class FlamesImFilterMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, mod_key, original_data, data_key,):
        mod_key = mod_key.upper()
        if mod_key == 'IMFILTER':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need imfiler for frames data')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, original_data, data_key,)

    
class ErrorMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, mod_key, original_data, data_key,):
        print('----------------------- !!!!!!!!! --------------------')
        print('There is no such　Mod: ' + str(mod_key))
        print('----------------------- !!!!!!!!! --------------------')
        
        
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
    
    def delta_f(self, trace_obj, bg_trace_obj):
        return trace_obj - bg_trace_obj
    
    def create_bg_comp(self, trace_obj, bg_trace_obj):
        f = self.f_value(trace_obj)
        delta_F_trace = self.delta_f(trace_obj, bg_trace_obj)
        trace_obj.show_data()
        delta_F_trace.show_data()
        bg_comp_trace = delta_F_trace + f
        return bg_comp_trace

    