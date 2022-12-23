# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:33:20 2022
concrete classes for file io
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import copy
import os

class TsmFileIO():
    def __init__(self, filename, filepath):
        # about file
        self.filename = filename
        self.file_path = filepath
        self.full_filename = os.path.join(filepath, filename)
        self.header = 0 # byte: it needs to chage to str [self.header.decode()]
        self.elec_header = 0
        
        #about fluo frame
        self.full_frame = np.array([0,])
        self.dark_frame = np.array([0,])
        self.ch_frame = np.array([0,])
        
        self.num_fluo_ch = 2  # Use () for PMT
        self.full_frame_interval = 0  # (ms)
        self.ch_frame_interval = 0  # (ms)
        self.data_pixel = np.empty([0,0])
        self.num_full_frame = np.empty([0,])
        self.num_ch_frame = np.empty([0,])
        self.full_3D_size = 0
        self.ch_3D_size = 0

        # about elec
        self.elec_trace = np.empty([0, 0])
        self.bnc_ratio = 0
        self.num_elec_ch = 0
        self.elec_interval = 0
        self.num_elec_data = 0
        
        # read data
        self.read_fileinfor()
        self.read_frame_data()
        self.read_tbn_data()
        
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
                str_num_full_frame = str_header[index+10:index+30]
                self.num_full_frame = np.array(int(str_num_full_frame))
                self.num_ch_frame = self.num_full_frame // self.num_fluo_ch
                
                # frame interval
                index = str_header.find('EXPOSURE')
                str_frame_interval = str_header[index+10:index+30]
                self.full_frame_interval = 1000*float(str_frame_interval)
                
                self.ch_frame_interval = self.full_frame_interval*self.num_fluo_ch
                
                # frame size
                self.full_3D_size = np.append(self.data_pixel, 
                                                self.num_full_frame)
                self.ch_3D_size = np.append(self.data_pixel, 
                                              self.num_full_frame//self.num_fluo_ch)

        except OSError as file_infor_error:
            print(file_infor_error)
            print('----------------------------------')
            print('Failed to import a TSM file infor.')
            print('----------------------------------')
            
        else:
            print('Imported a TSM file infor class.')
            
    def read_frame_data(self):
        try:
            # read shirt camera header information
            # https://fits.gsfc.nasa.gov/fits_primer.html
            file_dtype = np.int16
            path = self.full_filename
            frame_count = (self.data_pixel[0] *
                           self.data_pixel[1] *
                           self.num_full_frame) + (
                           self.data_pixel[0] *
                           self.data_pixel[1])

            full_with_dark_frame = np.fromfile(path, dtype=file_dtype,
                                          count=frame_count,
                                            offset=2880)
            full_dark_framesize = tuple(self.full_3D_size + [0, 0, 1] )  #including dark frame
            full_with_dark_frame = full_with_dark_frame.reshape(full_dark_framesize,
                                                                order = 'F')
            full_with_dark_frame = np.rot90(full_with_dark_frame, 3)
            full_with_dark_frame = np.fliplr(full_with_dark_frame)
            self.full_frame = full_with_dark_frame[:, :, 0:-1]
            self.dark_frame = full_with_dark_frame[:, :, -1]
            self.full_frame = self.full_frame - self.dark_frame[:, :, np.newaxis]

            self.ch_frame = self.split_frame(self.full_frame, self.num_fluo_ch)


        except IndexError as tsm_error:
            print(tsm_error)
            print('------------------------------------')
            print('Failed to import a TSM imaging data.')
            print('------------------------------------')
            
        else:
            print('Imported a TSM imaging data class.')
            
    @staticmethod
    def split_frame(frame, num_ch):
        ch_frame = np.empty([frame.shape[0], frame.shape[1], frame.shape[2]//num_ch, num_ch])
        
        for i in range(0, num_ch):
           for j in range(i, frame.shape[2], num_ch):
               ch_frame[:, :, j//num_ch, i] = frame[:, :, j]
        return ch_frame
    
    def read_image_data(self):
        pass  # No cell image from tsm data
    
    def read_tbn_data(self):  # from .tbn files
        try:
            # read a header
            # https://fits.gsfc.nasa.gov/fits_primer.html
            elec_full_filename = self.full_filename[0:-3] + ('tbn')
            elec_header_list = np.fromfile(elec_full_filename,
                                                      np.int16, count=2)
            self.num_elec_ch = elec_header_list[0] * -1
            self.bnc_ratio = elec_header_list[1]
            self.elec_interval = self.full_frame_interval/self.bnc_ratio
            self.num_elec_data = self.num_full_frame * self.bnc_ratio
            
            # read elec data
            pre_raw_elec = np.fromfile(elec_full_filename, np.float64, offset=4)
            self.elec_trace = pre_raw_elec.reshape(self.num_elec_data, 
                                               self.num_elec_ch, 
                                               order = 'F')
            
            # scale set
            self.elec_trace[:, 0] = (self.elec_trace[:, 0]/10)*1000  # The amp output is Vm*10, and V to mV
            self.elec_trace[:, 1] = (self.elec_trace[:, 1]*2)*1000  # Output of MaltiClamp700A is 0.5V/nA, and V to pA
            self.elec_trace[:, 2] = (self.elec_trace[:, 2]/10)*1000
            self.elec_trace[:, 3] = (self.elec_trace[:, 3]/10)*1000
            self.elec_trace[:, 4] = (self.elec_trace[:, 4]/10)*1000
            self.elec_trace[:, 5] = (self.elec_trace[:, 5]/10)*1000
            self.elec_trace[:, 6] = (self.elec_trace[:, 6]/10)*1000
            self.elec_trace[:, 7] = (self.elec_trace[:, 7]/10)*1000
            
        except OSError as e:
            print(e)
            print('----------------------------------')
            print('Failed to import a TSM (.tbn) file')
            print('----------------------------------')
            
        else:
            print('Imported a TSM(.tbn) elec data file.')
            
    def print_fileinfor(self):
        print(self.header.decode())
        print('elec_header = ' + str(self.elec_header))
        print('filenmae = ' + self.full_filename)
        print('num_fluo_ch = ' + str(self.num_fluo_ch))
        print('full_frame_interval = ' + str(self.full_frame_interval))
        print('ch_frame_interval = ' + str(self.ch_frame_interval))
        print('num_full_frame = ' + str(self.num_full_frame))
        print('num_ch_frame = ' + str(self.num_ch_frame))
        print('full_3D_size = ' + str(self.full_3D_size))
        print('ch_3D_size = ' + str(self.ch_3D_size))
        
        print('data_pixel = ' + str(self.data_pixel))
        print('bnc_ratio = ' + str(self.bnc_ratio))
        print('num_elec_ch = ' + str(self.num_elec_ch))
        print('elec_interval = ' + str(self.elec_interval))
        print('num_elec_data = ' + str(self.num_elec_data)) 
        