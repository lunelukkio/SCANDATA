# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:20:25 2023

@author: lunelukkio@gmail.com
"""
import numpy as np
    

class TsmFileIo:
    #load a .tsn file
    def __init__(self, filename, num_fluo_ch=2):
        # about file
        self.filename = filename.name
        self.file_path = filename.path
        self.full_filename = filename.fullname
        self.header = 0 # byte: it needs to chage to str [self.header.decode()]
        
        #about fluo frames
        self.full_frames = np.array([0,])
        self.dark_frame = np.array([0,])
        self.ch_frames = np.array([0,])
        
        self.num_fluo_ch = num_fluo_ch  # Use () for PMT
        self.full_frame_interval = 0  # (ms)
        self.ch_frame_interval = 0  # (ms)
        self.data_pixel = np.empty([0,0])
        self.num_full_frames = np.empty([0,])
        self.num_ch_frames = np.empty([0,])
        self.full_3D_size = 0
        self.ch_3D_size = 0
        
        self.object_num = 0  # for counter
        
        # read data
        self.read_infor()
        self.read_data()
        self.elec_data_obj = TbnFileIo(filename, 
                                   self. full_frame_interval, 
                                   self.num_full_frames)
        
    def read_infor(self):
        try:
            with open(self.full_filename, 'rb') as f:
                # redshirt data format
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
                str_num_full_frames = str_header[index+10:index+30]
                self.num_full_frames = np.array(int(str_num_full_frames))
                self.num_ch_frames = self.num_full_frames // self.num_fluo_ch
                
                # frame interval
                index = str_header.find('EXPOSURE')
                str_frame_interval = str_header[index+10:index+30]
                self.full_frame_interval = 1000*float(str_frame_interval)
                
                self.ch_frame_interval = self.full_frame_interval*self.num_fluo_ch
                
                # frames size
                self.full_3D_size = np.append(self.data_pixel, 
                                                self.num_full_frames)
                self.ch_3D_size = np.append(self.data_pixel, 
                                              self.num_full_frames//self.num_fluo_ch)

        except OSError as file_infor_error:
            print(file_infor_error)
            print('----------------------------------')
            print('Failed to import a TSM file infor.')
            print('----------------------------------')
            raise Exception('Failed to import a TSM data.')
            
        else:
            print('Imported a TSM file infor class.')
            
    def read_data(self):
        try:
            # read shirt camera header information
            # https://fits.gsfc.nasa.gov/fits_primer.html
            file_dtype = np.int16
            path = self.full_filename
            frames_count = (self.data_pixel[0] *
                           self.data_pixel[1] *
                           self.num_full_frames) + (
                           self.data_pixel[0] *
                           self.data_pixel[1])

            full_with_dark_frame = np.fromfile(path, dtype=file_dtype,
                                          count=frames_count,
                                            offset=2880)
            full_dark_framesize = tuple(self.full_3D_size + [0, 0, 1] )  #including dark frame
            full_with_dark_frame = full_with_dark_frame.reshape(full_dark_framesize,
                                                                order = 'F')
            full_with_dark_frame = np.rot90(full_with_dark_frame, 3)
            full_with_dark_frame = np.fliplr(full_with_dark_frame)
            self.full_frames = full_with_dark_frame[:, :, 0:-1]
            self.dark_frame = full_with_dark_frame[:, :, -1]
            self.full_frames = self.full_frames - self.dark_frame[:, :, np.newaxis]

            self.ch_frames = self.split_frames(self.full_frames, self.num_fluo_ch)


        except IndexError as tsm_error:
            print(tsm_error)
            print('------------------------------------')
            print('Failed to import a TSM data.')
            print('------------------------------------')
            raise Exception('Failed to import a TSM data.')
            
        else:
            print('Imported a TSM imaging data class.')
            
    @staticmethod
    def split_frames(frames, num_ch):
        ch_frames = np.empty([frames.shape[0], frames.shape[1], frames.shape[2]//num_ch, num_ch])
        
        for i in range(0, num_ch):
           for j in range(i, frames.shape[2], num_ch):
               ch_frames[:, :, j//num_ch, i] = frames[:, :, j]
        return ch_frames  # = [:,:,:,ch]
    
    def get_infor(self) -> tuple:
        data_infor = [self.full_frame_interval]
        for i in range(self.num_fluo_ch):
            data_infor.extend([self.ch_frame_interval])
        elec_interval = self.elec_data_obj.get_infor()
        for i in range(self.elec_data_obj.num_elec_ch):
            data_infor.extend([elec_interval])
        print(data_infor)
        return data_infor
    
    def get_3d(self) -> tuple:
        return self.full_frames, self.ch_frames[:,:,:,0], self.ch_frames[:,:,:,1]
    
    def get_2d(self):
        return []
    
    def get_1d(self):
        data_1d = self.elec_data_obj.get_data()
        return data_1d
        
    def print_data_infor(self):
        print(self.header.decode())
        print('filenmae = ' + self.full_filename)
        print('num_fluo_ch = ' + str(self.num_fluo_ch))
        print('full_frames_interval = ' + str(self.full_frames_interval))
        print('ch_frames_interval = ' + str(self.ch_frames_interval))
        print('num_full_frames = ' + str(self.num_full_frames))
        print('num_ch_frames = ' + str(self.num_ch_frames))
        print('full_3D_size = ' + str(self.full_3D_size))
        print('ch_3D_size = ' + str(self.ch_3D_size))
        print('data_pixel = ' + str(self.data_pixel))

        
class TbnFileIo:
    def __init__(self, filename, full_frame_interval, num_full_frames):
        # about file
        self.filename = filename.name
        self.file_path = filename.path
        self.full_filename = filename.fullname
        
        # from a .tsm file
        self.full_frame_interval = full_frame_interval
        self.num_full_frames = num_full_frames
        
        # about elec
        self.elec_header = 0
        self.elec_trace = np.empty([0, 0])  # = [data, ch]
        self.bnc_ratio = 0
        self.num_elec_ch = 0
        self.elec_interval = 0
        self.num_elec_data = 0
        
        self.object_num = 0  # for counter
        
        # read data
        self.read_data()
    
    def read_data(self):  # from .tbn files
        try:
            # read a header
            # https://fits.gsfc.nasa.gov/fits_primer.html
            elec_full_filename = self.full_filename[0:-3] + ('tbn')
            elec_header_list = np.fromfile(elec_full_filename,
                                                      np.int16, count=2)
            self.elec_header = elec_header_list
            self.num_elec_ch = elec_header_list[0] * -1
            self.bnc_ratio = elec_header_list[1]
            self.elec_interval = self.full_frame_interval/self.bnc_ratio
            self.num_elec_data = self.num_full_frames * self.bnc_ratio
            
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
            print('Failed to import a .tbn (Tsm) file')
            print('----------------------------------')
            raise Exception('Failed to import a .tbn (Tsm) data.')
            
        else:
            print('Imported a .tbn(.tsm) elec data file.')
       
    def get_infor(self):
        return self.elec_interval     
       
    def get_data(self):
        elec_data = []
        for i in range(0,8):
            elec_data.append(self.elec_trace[:,i])  # [data, ch]
        return elec_data 
    
            
    def print_data_infor(self):
        print('elec_header = ' + str(self.elec_header))
        print('filenmae = ' + self.full_filename)
        print('bnc_ratio = ' + str(self.bnc_ratio))
        print('num_elec_ch = ' + str(self.num_elec_ch))
        print('elec_interval = ' + str(self.elec_interval))
        print('num_elec_data = ' + str(self.num_elec_data))