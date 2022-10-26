# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:08:17 2022
concrete classes for abstract factory method
lunelukkio@gmail.com
"""
import numpy as np
from abc import ABCMeta, abstractmethod

"""
Abstract experimentdata factory
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
Abstract experimentdata product
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


"""
Concrete experimentdata factory
"""
class TsmDataFactory(ExperimentDataFactory):
    def create_FileInfor(self, filename, filepath):
        return TsmFileInfor(filename, filepath)

    def create_ImagingData(self, file_infor):
        return TsmImagingData(file_infor)

    def create_ElecData(self, file_infor):     #from tbn files
        return TbnElecData(file_infor)


class DaDataFactory(ExperimentDataFactory):
    def create_FileInfor(self, filename):
        pass

    def create_ImagingData(self, file_infor):
        pass

    def create_ElecData(self, file_infor):
        pass


"""
Concrete experimentdata product
"""
class TsmFileInfor(FileInfor):
    def __init__(self, filename, filepath):
        self.file_name = filename
        self.file_path = filepath
        self.full_filename = filepath + filename
        self.header = 0

        self.num_fluo_ch = (2,)  # Use () for PMT
        self.frame_interval = (0,)
        self.num_frame = (0,)
        self.data_pixel = (80, 80)  # tuple; The number of frame pixels.
        
        self.num_elec_ch = (8,)
        self.elec_interval = (0,)
        self.num_elec_data = (0,)

        
        self.read_fileinfor()
        
        print('imported file infor')


    def read_fileinfor(self):
        try:
            with open(self.full_filename, 'rb') as f:
                b = f.read(2880)
                self.header = b.decode()
        except OSError as e:
            print(e)
                
            
    def print_header(self):
        print(self.header)    
            
            

class TsmImagingData(ImagingData):
    def __init__(self, file_infor):
        super().__init__(file_infor)
        
        framesize = self.file_infor.data_pixel + \
                    self.file_infor.num_frame + \
                    self.file_infor.num_fluo_ch
        self.imaging_data = np.empty(framesize)

        self.read_imaging_data()

    def read_imaging_data(self):
        try:
            dtype = 'int16'
            path = self.file_infor.full_filename
            self.imaging_data = np.fromfile(path, dtype=dtype, count=-1,
                                            offset=2880)
            print(self.imaging_data.shape)
            print('Read data')
        except OSError as e:
            print(e)
        
    def print_imaging_data(self):
        print(self.imaging_data)  

class TbnElecData(ElecData):
    def __init__(self, file_infor):
        super().__init__(file_infor)

        elecsize = self.file_infor.num_elec_data + self.file_infor.num_elec_ch
        self.elec_trace = np.empty(elecsize)

    def read_ElecData(self):
        pass

    def select_ch(self):
        pass

    