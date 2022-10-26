# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 19:29:23 2022

lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod

"""
Abstract factory
"""
class DisplayedDataFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_displayed_data(self, original_data):
        pass


"""
Abstract product
"""
class DisplayedData(metaclass=ABCMeta):
    
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def mod_data(self):
        pass