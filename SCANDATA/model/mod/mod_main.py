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
    def __init__(self, data_service):
        self.blComp = BlCompMod(data_service)  # photo bleach compensation
        self.df_over_f = DFOverFMod()
        self.normalize = Normalize()
        self.error_mod = ErrorMod()
        
        self.mod_dict_order = ["BLCOMP", "DFOF", "NORMALIZE"]

        # Chain of resonsibility
        self.chain_of_responsibility = self.blComp. \
                              set_next(self.df_over_f). \
                              set_next(self.normalize). \
                              set_next(self.error_mod)
        
    def apply_mod(self, original_data_dict, mod_dict):
        if mod_dict == {}:
            mod_data_dict = original_data_dict
        else:
            mod_data_dict = {}
            # send each ch data
            for original_ch_key in original_data_dict.keys():
                # set each mod key to the chain of responsibility
                original_data = original_data_dict[original_ch_key]
                for mod_key in self.mod_dict_order:
                    if mod_key in mod_dict:
                        original_data = self.blComp.apply_mod(mod_key, mod_dict[mod_key], original_data, original_ch_key)
                mod_data_dict[original_ch_key] = original_data
        return mod_data_dict  
        
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
    
    def handle_request(self, mod_key, mod_val, original_data, original_ch_key):
        if self.__next_handler:
            return self.__next_handler.apply_mod(mod_key, mod_val, original_data, original_ch_key)

"""
ConcreteHandler
"""

class BlCompMod(ModHandler):
    def __init__(self, data_service):
        super().__init__()
        self.trace_calc = TraceCalculation()
        self.__data_service = data_service
        
    def apply_mod(self, mod_key: str, mod_val, original_data: dict, original_ch_key: str) -> dict:
        mod_key = mod_key.upper()
        if mod_key == 'BLCOMP':
            # separate a data from dict
            bl_trace = self.__get_bl_trace(original_ch_key, mod_val)
            if bl_trace is None:
                return super().handle_request(mod_key, mod_val, original_data, original_ch_key)
            blComp_trace_obj = self.trace_calc.create_blComp(original_data, bl_trace)
            return blComp_trace_obj
        else:
            return super().handle_request(mod_key, mod_val, original_data, original_ch_key)

    def __get_bl_trace(self, ch_key, mod_val):
        data_dict = self.__data_service.get_data(mod_val[0], mod_val[1])
        if data_dict is None:
            return
        if ch_key in data_dict:
            bl_trace = data_dict[ch_key]
        else:
            print(f"There is no {ch_key} in the background dict.")
            bl_trace = None
        return bl_trace


class DFOverFMod(ModHandler):  # %
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        
    def apply_mod(self, mod_key: str, mod_val, original_data: dict, original_ch_key: str) -> dict:
        mod_key = mod_key.upper()
        if mod_key == 'DFOF':
            df_over_f = self.trace_calc.create_df_over_f(original_data)
            mod_trace_obj = df_over_f
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, mod_val, original_data, original_ch_key)
        
        
class Normalize(ModHandler):
    def __init__(self):
        super().__init__()
        self.trace_calc = TraceCalculation()
        
    def apply_mod(self, mod_key: str, mod_val, original_data: dict, original_ch_key: str) -> dict:
        mod_key = mod_key.upper()
        if mod_key == 'NORMALIZE':
            normalize = self.trace_calc.create_normalize(original_data)
            mod_trace_obj = normalize
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, mod_val, original_data, original_ch_key)
        
        
    # This should be in View class?
class Invert(ModHandler):
    pass
    
    
class TraceMovingAveMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, mod_key: str, mod_val, original_data: dict, original_ch_key: str) -> dict:
        mod_key = mod_key.upper()
        if mod_key == 'MOVINGAVE':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need Moving Average')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, mod_val, original_data, original_ch_key)
    
    
class FlamesImFilterMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, mod_key: str, mod_val, original_data: dict, original_ch_key: str) -> dict:
        mod_key = mod_key.upper()
        if mod_key == 'IMFILTER':
            print('----------------------- !!!!!!!!! --------------------')
            print('Tip Need imfiler for frames data')
            print('----------------------- !!!!!!!!! --------------------')
            mod_trace_obj = None
            return mod_trace_obj
        else:
            return super().handle_request(mod_key, mod_val, original_data, original_ch_key)

    
class ErrorMod(ModHandler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, mod_key: str, mod_val, original_data: dict, original_ch_key: str) -> dict:
        print('----------------------- !!!!!!!!! --------------------')
        print('No　Mod: ' + str(mod_key))
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
        new_obj = TraceData(val, interval, "Roi")
        return new_obj
    
    def create_normalize(self, trace_obj):
        min_val = np.min(trace_obj.data)
        pre_trace_obj = trace_obj - min_val
        max_val = np.max(pre_trace_obj.data)
        norm_obj = pre_trace_obj/max_val
        return norm_obj
    
    def delta_f(self, trace_obj, bl_trace_obj):
        return trace_obj - bl_trace_obj
    
    def create_blComp(self, trace_obj, bl_trace_obj):
        f = self.f_value(trace_obj)
        delta_F_trace = self.delta_f(trace_obj, bl_trace_obj)
        #trace_obj.show_data()
        #delta_F_trace.show_data()
        blComp_trace = delta_F_trace + f
        return blComp_trace

    