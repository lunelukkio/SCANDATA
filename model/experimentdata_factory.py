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
        # about file
        self.filename = filename
        self.file_path = filepath
        self.full_filename = filepath + filename
        self.header = 0 # byte: it needs to chage to str [self.header.decode()]
        self.elec_header = 0
        
        #about fluo frame
        self.num_fluo_ch = 2  # Use () for PMT
        self.frame_interval = 0  # (ms)
        self.fluo_ch_interval = 0  # (ms)
        self.num_frame = [0,]
        self.data_pixel = 0
        self.framesize = 0

        # about elec
        self.bnc_ratio = 0
        self.num_elec_ch = 0
        self.elec_interval = 0
        self.num_elec_data = 0
        
        self.read_fileinfor()
        print('imported file infor')

    def read_fileinfor(self):
        try:
            with open(self.full_filename, 'rb') as f:
                # https://fits.gsfc.nasa.gov/fits_primer.html
                
                self.header = f.read(2880)
                str_header = self.header.decode()

                # x pixel
                index = str_header.find('NAXIS1')
                str_num_x = str_header[index+10:index+30]
                num_x = int(str_num_x)
                
                # y pixel
                index = str_header.find('NAXIS2')
                str_num_y = str_header[index+10:index+30]
                num_y = int(str_num_y)
                
                self.data_pixel = [num_x, num_y]
                
                # z: number of frames
                index = str_header.find('NAXIS3')
                str_num_frame = str_header[index+10:index+30]
                self.num_frame = [int(str_num_frame)]
                
                # frame interval
                index = str_header.find('EXPOSURE')
                str_frame_interval = str_header[index+10:index+30]
                self.frame_interval = 1000*float(str_frame_interval)
                
                self.fluo_ch_interval = self.frame_interval*self.num_fluo_ch
                
                # frame size
                self.framesize = np.array(self.data_pixel + self.num_frame)
                
        except OSError as e:
            print(e)
                
    def print_fileinfor(self):
        print(self.header.decode())
        print('elec header = ' + str(self.elec_header))
        print('filenmae = ' + self.full_filename)
        print('num fluo ch = ' + str(self.num_fluo_ch))
        print('frame interval = ' + str(self.frame_interval))
        print('ch frame interval = ' + str(self.fluo_ch_interval))
        print('num frame = ' + str(self.num_frame))
        print('data pixel = ' + str(self.data_pixel))
        print('BNC ratio = ' + str(self.bnc_ratio))
        print('num elec ch = ' + str(self.num_elec_ch))
        print('elec interval = ' + str(self.elec_interval))
        print('num elec data = ' + str(self.num_elec_data))


class TsmImagingData(ImagingData):
    def __init__(self, file_infor):
        super().__init__(file_infor)
        
        self.framesize = np.array(self.file_infor.framesize)
        self.full_frame = np.empty(self.framesize)
        self.dark_frame = np.empty(np.delete(self.framesize, -1))

        self.read_imaging_data()

    def read_imaging_data(self):
        try:
            # https://fits.gsfc.nasa.gov/fits_primer.html
            file_dtype = np.int16
            path = self.file_infor.full_filename
            frame_count = (self.file_infor.data_pixel[0] *
                          self.file_infor.data_pixel[1] *
                          self.file_infor.num_frame[0]) + (
                              self.file_infor.data_pixel[0] *
                              self.file_infor.data_pixel[1])

            full_with_dark_frame = np.fromfile(path, dtype=file_dtype,
                                          count=frame_count,
                                            offset=2880)
            full_dark_framesize = tuple(self.framesize + [0, 0, 1] )  #including dark frame
            full_with_dark_frame = full_with_dark_frame.reshape(full_dark_framesize,
                                                                order = 'F')
            full_with_dark_frame = np.rot90(full_with_dark_frame, 3)
            full_with_dark_frame = np.fliplr(full_with_dark_frame)
            self.full_frame = full_with_dark_frame[:, :, 0:-1]
            self.dark_frame = full_with_dark_frame[:, :, -1]
            self.full_frame = self.full_frame - self.dark_frame[:, :, np.newaxis]
            
        except OSError as e:
            print(e)
        
    def print_full_frame(self):
        #np.set_printoptions(threshold=np.inf)
        print(self.dark_frame)
        #print(self.full_frame.shape)
        print(self.dark_frame.shape)
        #np.set_printoptions(threshold=1000)
        
        
class TbnElecData(ElecData):
    def __init__(self, file_infor):
        super().__init__(file_infor)
        self.num_elec_data = 0
        self.elec_trace = 0
        
        self.read_ElecData()

    def read_ElecData(self):
        try:
            # read a header
            # https://fits.gsfc.nasa.gov/fits_primer.html
            elec_full_filename = self.file_infor.full_filename[0:-3] + ('tbn')
            elec_header_list = np.fromfile(elec_full_filename,
                                                      np.int16, count=2)
            self.file_infor.num_elec_ch = elec_header_list[0] * -1
            self.file_infor.bnc_ratio = elec_header_list[1]
            self.file_infor.elec_interval = \
            self.file_infor.frame_interval/self.file_infor.bnc_ratio
            self.file_infor.num_elec_data = \
            self.file_infor.num_frame[0]*self.file_infor.bnc_ratio
            
            # read elec data
            raw_elec = np.fromfile(elec_full_filename, np.float64, offset=4)
            self.elec_trace = raw_elec.reshape(self.file_infor.num_elec_data, 
                                               self.file_infor.num_elec_ch, 
                                               order = 'F')

        except OSError as e:
            print(e)

    def select_ch(self):
        pass
    