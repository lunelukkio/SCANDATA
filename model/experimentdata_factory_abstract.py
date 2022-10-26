# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 14:55:37 2022
abstract classes for abstract factory method
lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod

"""
Abstract factory
"""
class ExperimentDataFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_FileInfor(self, filename, filepath):
        pass

    @abstractmethod
    def create_ImagingData(self, file_infor):
        pass

    @abstractmethod
    def create_ElecData(self, file_infor):
        pass


"""
Abstract product
"""
class FileInfor(metaclass=ABCMeta):

    @abstractmethod
    def read_fileinfor(self):
        pass


class ImagingData(metaclass=ABCMeta):
    def __init__(self, file_infor):
        self.file_infor = file_infor

    @abstractmethod
    def read_imaging_data(self):
        pass


class ElecData(metaclass=ABCMeta):
    def __init__(self, file_infor):
        self.file_infor = file_infor

    @abstractmethod
    def read_ElecData(self):
        pass

    @abstractmethod
    def select_ch(self):
        pass

