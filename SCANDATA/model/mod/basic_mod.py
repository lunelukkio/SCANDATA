# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:29:05 2023
When adding a new mod, make a new instance of it \ 
and add it to instance of chain of responsibility in ModCliet class.
Also check ModList class in user_controller.py
@author: lunelukkio@gmail.com
"""

import numpy as np
from SCANDATA.model.value_object import TraceData
from SCANDATA.model.mod.mod_main import ModHandler

        
"""
ConcreteHandler
"""

class BgCompMod(ModHandler):
    def __init__(self, data_dict):
        super().__init__()
        self.trace_calc = TraceCalculation()
        #self.__controller_entities = controller_entities
        self.__data_dict = data_dict
        self.__bg_roi_num = 1  # This is the roi number for backgrand trace (Roi1)
        
    def apply_mod(self, data_key, original_data, key):
        if key == 'BgComp':
            bg_trace_entitiy = self.__get_bg_trace(data_key)
            bg_comp_trace_obj = self.trace_calc.create_bg_comp(original_data, bg_trace_entitiy.trace_obj)
            return bg_comp_trace_obj
        else:
            return super().handle_request(data_key, original_data, key)
        
    def __get_bg_trace(self, data_key):
        print('Tip: Need refactoring. Now is only for two traces. bg traces should be got from Roi class observers and macth the data_key to an obserber name')
        if 'Full' in data_key:
            bg_trace_entity = self.__data_dict['FullTrace1']
        elif 'ChTrace' in data_key:
            last_digit = int(data_key[-1])
            if last_digit % 2 == 0:
                bg_trace_entity = self.__data_dict['ChTrace2']
            else:
                bg_trace_entity = self.__data_dict['ChTrace1']
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
    
    def delta_f(self, trace_obj, bg_trace_obj):
        return trace_obj - bg_trace_obj
    
    def create_bg_comp(self, trace_obj, bg_trace_obj):
            f = self.f_value(trace_obj)
            delta_F_trace = self.delta_f(trace_obj, bg_trace_obj)
            trace_obj.show_data()
            delta_F_trace.show_data()
            bg_comp_trace = delta_F_trace + f
            return bg_comp_trace

    