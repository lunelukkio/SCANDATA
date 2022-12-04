# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:08:17 2022
concrete classes for abstract factory method
lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import copy
import os

  
"""
Frame factory
"""
class FrameFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_frame(self, data, interval):
        pass
    
class FullFrameFactory(FrameFactory):
    def create_frame(self, data, interval):  # data = file_io
        return FullFrame(data, interval)
    
class ChFrameFactory(FrameFactory):
    def create_frame(self, data, interval):  # data = file_io
        return ChFrame(data, interval)
    

"""
Image factory
"""
class ImageFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_image(self, data):
        pass
    
class CellImageFactory(ImageFactory):
    def create_image(self, data):  # data = frame
        return CellImage(data)
    
class DifImageFactory(ImageFactory):
    def create_image(self, data):  # data = frame
        return DifImage(data)


"""
Trace factory
"""
class TraceFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_trace(self, data, interval):
        pass
    
class FluoTraceFactory(TraceFactory):
    def create_trace(self, data, interval):  # data = frame
        return FluoTrace(data, interval)
    
class ElecTraceFactory(TraceFactory):
    def create_trace(self, data, interval):  # data = file_io (.tbn)
        return ElecTrace(data, interval)
    

"""
product
"""
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
        
class Frame(metaclass=ABCMeta):  # 3D frame data: full frame, ch image
    def __init__(self, data, interval):
        self.frame_data = np.array([0,])
        self.time_data = np.array([0,])  # (ms)
        
        self.interval = 0  # (ms)
        self.pixel = 0  # (um)
        self.unit = 0  # No unit because of raw camera data.
        
        self.read_data(data, interval)

    def read_data(self, data, interval):
        self.frame_data = copy.deepcopy(data)
        self.interval = copy.deepcopy(interval)
        
        if len(self.frame_data) <= 1:
            print('---------------------')
            print('Can not make 3D data')
            print('---------------------')
            return None
        
        print('Read a frame data')
    
    def get_data(self):
        frame = self.frame_data
        interval = self.full_frame_interval
        return frame, interval

    def update(self):
        pass

    def show_frame(self, frame):
        plt.imshow(self.frame_data[:, :, frame], cmap='gray', interpolation='none')

    def print_frame_infor(self):
        #np.set_printoptions(threshold=np.inf)
        print(self.data_type)
        print(self.data.shape)
        print(self.time_data)

        #np.set_printoptions(threshold=1000)

class FullFrame(Frame):
    num_instance = 0  # Class member to count the number of instance
    def __init__(self, data, interval):
        super().__init__(data, interval)
        FullFrame.num_instance += 1

class ChFrame(Frame):
    num_instance = 0  # Class member to count the number of instance
    def __init__(self, data, interval):
        super().__init__(data, interval)
        ChFrame.num_instance += 1

class Image(metaclass=ABCMeta):  # cell image, dif image
    def __init__(self, data):
        self.image_data = np.array([0, 0])
        
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

class CellImage(Image):
    num_instance = 0  # Class member to count the number of instance
    def __init__(self, data):
        super().__init__(data)
        CellImage.num_instance += 1
        
        self.frame_data = data

    def read_data(self, val):
        start = val[0]
        end = val[1]

        if end - start == 0:
            self.image_data = self.frame_data[:, :, val[0]]
            print('Read a single cell image')
        elif end - start > 0: 
            self.image_data = np.mean(self.frame_data[:, :, start:end], axis = 2)
            print('Read an avarage cell image')
        else:
            self.image_data = np.zeros((2, 2))
            print('-----------------------------------------------------')
            print('The end frame should be higher than the start frame.')
            print('-----------------------------------------------------')
        
    def update(self, val):
        self.read_data(val)
        print('Recieved a notify message.')

    def get_data(self):
        pass
    
    def show_image(self):
            plt.imshow(self.image_data, cmap='gray', interpolation='none')
        
class DifImage(Image):
    num_instance = 0  # Class member to count the number of instance
    def __init__(self, data):
        super().__init__(data)
        DifImage.num_instance += 1

    def read_data(self):
        pass
        
    def update(self):
        pass

    def get_data(self):
        pass


class Trace(metaclass=ABCMeta):  # Fluo trae, Elec trace
    def __init__(self):
        self.trace_data = np.array([0,])
        self.time_data = np.array([0,])
        
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

    def plot_trace(self):
        plt.plot(self.time_data, self.trace_data)   

class FluoTrace(Trace):
    num_instance = 0  # Class member to count the number of instance
    def __init__(self, data, interval):
        super().__init__()
        FluoTrace.num_instance += 1
        
        self.frame_data = data
        self.interval = copy.deepcopy(interval)
        # trace_data and time_data are in the super class
        
        self.read_data([40, 40, 1, 1])
        self.create_time_data()

    def read_data(self, roi):  # roi[x, y, x_length, y_length]   
        self.trace_data = self.fluo_trace_creator(self.frame_data, roi)
        
    @staticmethod
    def fluo_trace_creator(frame, roi):
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frame[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data
        print('Undated ROI = ' + str(roi))
    
    def create_time_data(self):
        num_data_point = self.interval * np.shape(self.trace_data)[0]
        self.time_data = np.linspace(self.interval, 
                                     num_data_point, 
                                     np.shape(self.trace_data)[0])
    
    def update(self, roi_obj):
        self.read_data(roi_obj)
        print('Recieved a notify message.')
    
    def get_data(self):
        pass
 
    
class ElecTrace(Trace):
    num_instance = 0  # Class member to count the number of instance
    def __init__(self, data, interval):
        super().__init__()
        ElecTrace.num_instance += 1
        # trace_data and time_data are in the super class
        self.read_data(data, interval)

    def read_data(self, data, interval):
        self.trace_data = copy.deepcopy(data)
        self.interval = copy.deepcopy(interval)
        num_data_point = self.interval * np.shape(self.trace_data)[0]
        self.time_data = np.linspace(self.interval, 
                                     num_data_point, 
                                     np.shape(self.trace_data)[0])
        
        if len(self.trace_data) <= 1:
            print('---------------------')
            print('Can not make 3D data')
            print('---------------------')
            return None
        
        print('Read Elec frames')

    
    def update(self):
        pass

    def get_data(self):
        pass


if __name__ == '__main__':
    filename = '20408A001.tsm'
    filepath = '..\\220408\\'

    io = TsmFileIO(filename, filepath)
    factory_type = FullFrameFactory()
    data_file1 = factory_type.create_frame(io)
    
    
    data_file1.show_frame(0)

    

