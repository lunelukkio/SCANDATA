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
        self.filename = filename
        self.file_path = filepath
        self.full_filename = filepath + filename
        self.header = 0 # byte: it needs to chage to str [self.header.decode()]
        self.str_header = 0

        self.num_fluo_ch = 2  # Use () for PMT
        self.frame_interval = 0
        self.num_frame = [0,]
        self.data_pixel = 0
        
        self.num_elec_ch = 8
        self.elec_interval = 0
        self.num_elec_data = 0
        
        self.fluo_ch_interval = self.frame_interval*self.num_fluo_ch

        self.read_fileinfor()
        print('imported file infor')

    def read_fileinfor(self):
        try:
            with open(self.full_filename, 'rb') as f:
                # https://fits.gsfc.nasa.gov/fits_primer.html
                
                b = f.read(2880)
                self.header = f.read(2880)
                self.str_header = b.decode()

                """x pixel"""
                index = self.str_header.find('NAXIS1')
                str_num_x = self.str_header[index+10:index+30]
                num_x = int(str_num_x)
                
                """y pixel"""
                index = self.str_header.find('NAXIS2')
                str_num_y = self.str_header[index+10:index+30]
                num_y = int(str_num_y)
                
                self.data_pixel = [num_x, num_y]
                
                """z: number of frames"""
                index = self.str_header.find('NAXIS3')
                str_num_frame = self.str_header[index+10:index+30]
                self.num_frame = [int(str_num_frame)]
                
                """ frame interval"""
                index = self.str_header.find('EXPOSURE')
                str_frame_interval = self.str_header[index+10:index+30]
                self.frame_interval = [1000*float(str_frame_interval)]
                
        except OSError as e:
            print(e)
                
    def print_fileinfor(self):
        print(self.str_header)    
        print('filenmae = ' + self.full_filename)
        print('num fluo ch = ' + str(self.num_fluo_ch))
        print('frame interval = ' + str(self.frame_interval))
        print('num frame = ' + str(self.num_frame))
        print('data pixel = ' + str(self.data_pixel))
        print('num elec ch = ' + str(self.num_elec_ch))
        print('elec interval = ' + str(self.elec_interval))
        print('num elec data = ' + str(self.num_elec_data))


class TsmImagingData(ImagingData):
    def __init__(self, file_infor):
        super().__init__(file_infor)
        
        self.framesize = tuple(self.file_infor.data_pixel +
                    self.file_infor.num_frame)
        self.fluo_frame = np.empty(self.framesize)

        self.read_imaging_data()

    def read_imaging_data(self):
        try:
            # https://fits.gsfc.nasa.gov/fits_primer.html
            dtype = 'int16'
            path = self.file_infor.full_filename
            frame_count = self.file_infor.data_pixel[0] * \
                          self.file_infor.data_pixel[1] * \
                          self.file_infor.num_frame[0]
            self.fluo_frame = np.fromfile(path, dtype=dtype,
                                          count=frame_count,
                                            offset=2880)
            self.fluo_frame = self.fluo_frame.reshape(self.framesize)
            
            print(self.fluo_frame.shape)
            print(self.fluo_frame.ndim)
            print(self.framesize)
        except OSError as e:
            print(e)
        
    def print_fluo_frame(self):
        print(self.fluo_frame)  

class TbnElecData(ElecData):
    def __init__(self, file_infor):
        super().__init__(file_infor)

        elecsize = self.file_infor.num_elec_data + self.file_infor.num_elec_ch
        self.elec_trace = np.empty(elecsize)

    def read_ElecData(self):
        pass

    def select_ch(self):
        pass

    