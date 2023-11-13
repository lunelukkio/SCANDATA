# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:49:05 2023

@author: lunelukkio@gmail.com
"""

from SCANDATA.model.mod.basic_mod import BgCompMod, \
                                         DFOverFMod, \
                                         Normalize ,\
                                         ErrorMod

"""
Chain of responsibility client
"""

class ModClient:  # Put every mods. Don't need to sepalate mods for each data type..
    def __init__(self):
        self.mod_list = []
        
        self.bg_comp = BgCompMod()  # [1] = data_list
        self.df_over_f = DFOverFMod()
        self.normalize = Normalize()
        self.error_mod = ErrorMod()

        # Chain of resonsibility
        self.chain_of_responsibility = self.bg_comp. \
                              set_next(self.df_over_f). \
                              set_next(self.normalize). \
                              set_next(self.error_mod)
        
    def set_mod(self, mod_keys, original_data):
        if mod_keys == []:
            mod_data = original_data
        else:
            for key in mod_keys:
                mod_data = self.bg_comp.apply_mod(key, original_data)
        return mod_data
    
    
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
    
    def handle_request(self, data_key, original_data, key):
        if self.__next_handler:
            return self.__next_handler.apply_mod(data_key, original_data, key)