# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:08:17 2022
concrete classes for abstract factory method
lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
"""
Abstract experimentdata factory
"""
class ExperimentDataFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_fileinfor(self, filename, filepath):
        pass

    @abstractmethod
    def create_imaging_data(self, fileinfor):
        pass

    @abstractmethod
    def create_elec_data(self, fileinfor):
        pass
    
    @abstractmethod
    def create_cell_image(self, fileinfor):
        pass


"""
Abstract experimentdata product
"""
class FileInfor(metaclass=ABCMeta):
    
    @abstractmethod
    def read_fileinfor(self):
        pass


class ImagingData(metaclass=ABCMeta):
    def __init__(self, fileinfor):
        self.fileinfor = fileinfor

    @abstractmethod
    def read_imaging_data(self):
        pass


class ElecData(metaclass=ABCMeta):
    def __init__(self, fileinfor):
        self.fileinfor = fileinfor

    @abstractmethod
    def read_elec_data(self):
        pass



"""
Concrete experimentdata factory
"""
class TsmDataFactory(ExperimentDataFactory):
    def create_fileinfor(self, filename, filepath):
        return TsmFileInfor(filename, filepath)

    def create_imaging_data(self, fileinfor):
        return TsmImagingData(fileinfor)

    def create_elec_data(self, fileinfor):     #from tbn files
        return TbnElecData(fileinfor)
    
    def create_cell_image(self, fileinfor):
        pass


class DaDataFactory(ExperimentDataFactory):
    def create_fileinfor(self, filename):
        pass

    def create_imaging_data(self, fileinfor):
        pass

    def create_elec_data(self, fileinfor):
        pass

    def create_cell_image(self, fileinfor):
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
        self.full_frame_interval = 0  # (ms)
        self.ch_frame_interval = 0  # (ms)
        self.data_pixel = np.empty([0,0])
        self.num_frame = np.empty([0,])
        self.full_framesize = 0
        self.ch_framesize = 0

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
                
                self.data_pixel = np.array([num_x, num_y])
                
                # z: number of frames
                index = str_header.find('NAXIS3')
                str_num_frame = str_header[index+10:index+30]
                self.num_frame = np.array(int(str_num_frame))
                
                # frame interval
                index = str_header.find('EXPOSURE')
                str_frame_interval = str_header[index+10:index+30]
                self.full_frame_interval = 1000*float(str_frame_interval)
                
                self.ch_frame_interval = self.full_frame_interval*self.num_fluo_ch
                
                # frame size
                self.full_framesize = np.append(self.data_pixel, 
                                                self.num_frame)
                self.ch_framesize = np.append(self.data_pixel, 
                                              self.num_frame//self.num_fluo_ch)

        except OSError as e:
            print(e)
                
    def print_fileinfor(self):
        print(self.header.decode())
        print('elec_header = ' + str(self.elec_header))
        print('filenmae = ' + self.full_filename)
        print('num_fluo_ch = ' + str(self.num_fluo_ch))
        print('full_frame_interval = ' + str(self.full_frame_interval))
        print('ch_frame_interval = ' + str(self.ch_frame_interval))
        print('num_frame = ' + str(self.num_frame))
        print('data_pixel = ' + str(self.data_pixel))
        print('bnc_ratio = ' + str(self.bnc_ratio))
        print('num_elec_ch = ' + str(self.num_elec_ch))
        print('elec+interval = ' + str(self.elec_interval))
        print('num_elec_data = ' + str(self.num_elec_data))


class TsmImagingData(ImagingData):
    def __init__(self, fileinfor):
        super().__init__(fileinfor)
        
        self.full_frame = 0
        self.ch_frame = 0
        self.dark_frame = 0

        self.read_imaging_data()
        self.ch_frame = FrameSpliter.split_frame(self.full_frame, fileinfor.num_fluo_ch)
        

    def read_imaging_data(self):
        try:
            # https://fits.gsfc.nasa.gov/fits_primer.html
            file_dtype = np.int16
            path = self.fileinfor.full_filename
            frame_count = (self.fileinfor.data_pixel[0] *
                          self.fileinfor.data_pixel[1] *
                          self.fileinfor.num_frame) + (
                              self.fileinfor.data_pixel[0] *
                              self.fileinfor.data_pixel[1])

            full_with_dark_frame = np.fromfile(path, dtype=file_dtype,
                                          count=frame_count,
                                            offset=2880)
            full_dark_framesize = tuple(self.fileinfor.full_framesize + [0, 0, 1] )  #including dark frame
            full_with_dark_frame = full_with_dark_frame.reshape(full_dark_framesize,
                                                                order = 'F')
            full_with_dark_frame = np.rot90(full_with_dark_frame, 3)
            full_with_dark_frame = np.fliplr(full_with_dark_frame)
            self.full_frame = full_with_dark_frame[:, :, 0:-1]
            self.dark_frame = full_with_dark_frame[:, :, -1]
            self.full_frame = self.full_frame - self.dark_frame[:, :, np.newaxis]
            
        except OSError as e:
            print(e)
        
    def show_frame(self, ch, frame):
        if ch == -1:
            plt.imshow(self.dark_frame[:, :])
        elif ch == 0:
            plt.imshow(self.full_frame[:, :, frame])
        elif ch == 1:
            plt.imshow(self.ch_frame[:, :, frame, 0])
        elif ch == 2:
            plt.imshow(self.ch_frame[:, :, frame, 1])
        elif ch == 3:
            plt.imshow(self.ch_frame[:, :, frame, 2])
            
    def print_frame(self):
        #np.set_printoptions(threshold=np.inf)
        print(self.fileinfor.full_framesize)
        print(self.fileinfor.ch_framesize)
        print(self.ch1_frame.shape)
        print(self.ch2_frame.shape)
        #np.set_printoptions(threshold=1000)
        
        
class TbnElecData(ElecData):
    def __init__(self, fileinfor):
        super().__init__(fileinfor)
        self.num_elec_data = 0
        self.elec_trace = 0
        
        self.read_elec_data()

    def read_elec_data(self):
        try:
            # read a header
            # https://fits.gsfc.nasa.gov/fits_primer.html
            elec_full_filename = self.fileinfor.full_filename[0:-3] + ('tbn')
            elec_header_list = np.fromfile(elec_full_filename,
                                                      np.int16, count=2)
            self.fileinfor.num_elec_ch = elec_header_list[0] * -1
            self.fileinfor.bnc_ratio = elec_header_list[1]
            self.fileinfor.elec_interval = \
            self.fileinfor.full_frame_interval/self.fileinfor.bnc_ratio
            self.fileinfor.num_elec_data = \
            self.fileinfor.num_frame * self.fileinfor.bnc_ratio
            
            # read elec data
            raw_elec = np.fromfile(elec_full_filename, np.float64, offset=4)
            self.elec_trace = raw_elec.reshape(self.fileinfor.num_elec_data, 
                                               self.fileinfor.num_elec_ch, 
                                               order = 'F')

        except OSError as e:
            print(e)

    
    def plot_elec_data(self, elec_ch):
        plt.plot(self.elec_trace[:, elec_ch])
        
class FrameSpliter:
    @staticmethod
    def split_frame(frame, num_ch):
        ch_frame = np.empty([frame.shape[0], frame.shape[1], frame.shape[2]//num_ch, num_ch])
        
        for i in range(0, frame.shape[2], num_ch):
            ch_frame[:, :, i//num_ch, 0] = frame[:, :, i]

        for i in range(1, frame.shape[2], num_ch):
            ch_frame[:, :, (i-1)//num_ch, 1] = frame[:, :, i]

        return ch_frame
