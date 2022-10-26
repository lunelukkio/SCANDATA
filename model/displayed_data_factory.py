# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:04:55 2022

lunelukkio@gmail.com
"""

"""
Concrete factory
"""

import numpy as np
import model.displayed_data_factory_abstract as ddabstract

class DisplayedFluoTraceFactory(ddabstract.DisplayedDataFactory):

    def create_displayed_data(self, original_fluo_frame):
        return DisplayedFluoTrace(original_fluo_frame)
    
class DisplayedElecTraceFactory(ddabstract.DisplayedDataFactory):

    def create_displayed_data(self, original_data):
        return DisplayedElecTrace(original_data)
    
class DisplayedImageFactory(ddabstract.DisplayedDataFactory):

    def create_displayed_data(self, original_data):
        return DisplayedImage(original_data)


"""
Concrete product
"""
class DisplayedFluoTrace(ddabstract.DisplayedData):
    def __init__(self, original_fluo_frame):
        self.original_fluo_frame = original_fluo_frame

    def get_data(self):
        print('this is a fluo trace')

    def mod_data(sel):
        pass


class DisplayedElecTrace(ddabstract.DisplayedData):
    def __init__(self, original_elec_data):
        self.original_elec_data = original_elec_data

    def get_data(self):
        self.original_elec_data.print_filename()

    def mod_data(sel):
        pass


class DisplayedImage(ddabstract.DisplayedData):
    def __init__(self, original_fluo_frame):
        self.original_fluo_frame = original_fluo_frame

    def get_data(self):
        print('this is a cell image')

    def mod_data(sel):
        pass
