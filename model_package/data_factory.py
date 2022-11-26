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


"""
IOfoctory
"""
class IOFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_file_io(self, filename, filepath):  # Only this class is file format dependent.
        pass

class TmsIOFactory(IOFactory):
    def create_file_io(self, filename, filepath):
        return TsmFileIO(filename, filepath)
    
class DaIOFactory(IOFactory):
    def create_file_io(self, filename, filepath):
        raise NotImplementedError
    
class FileIO(metaclass=ABCMeta):
    @abstractmethod
    def read_fileinfor(self):
        pass

    @abstractmethod
    def read_frame_data(self):
        pass
    
    @abstractmethod
    def read_image_data(self):
        pass
    
    @abstractmethod
    def read_trace_data(self):
        pass


"""
Frame factory
"""
class FrameFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_frame(self, data):
        pass
    
class FullFrameFacoty(FrameFactory):
    def create_frame(self, data):  # data = file_io
        return FullFrame(data)
    
class ChFrameFacoty(FrameFactory):
    def create_frame(self, data):  # data = file_io
        return ChFrame(data)
    
class Frame(metaclass=ABCMeta):  # 3D frame data: full frame, ch image
    def __init__(self, data):
        self.data = 0
        self.time_data = 0  # (ms)
        
        self.interval = 0  # (ms)
        self.pixel = 0  # (um)
        self.unit = 0  # No unit because of raw camera data.
        
        self.file_io = data

        self.read_data()

    @abstractmethod
    def read_data(self):
        pass
    
    def get_data(self):
        frame = self.data
        interval = self.full_frame_interval
        return frame, interval

    def update(self):
        pass

    def show_frame(self, frame):
        plt.imshow(self.data[:, :, frame], cmap='gray', interpolation='none')

    def print_3d_infor(self):
        #np.set_printoptions(threshold=np.inf)
        print(self.data_type)
        print(self.data.shape)
        print(self.time_data)

        #np.set_printoptions(threshold=1000)


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
    
class Image(metaclass=ABCMeta):  # cell image, dif image
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def create_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass


"""
Trace factory
"""
class TraceFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_trace(self, data):
        pass
    
class FluoTraceFactory(TraceFactory):
    def create_trace(self, data):  # data = frame
        return FluoTrace(data)
    
class ElecTraceFactory(TraceFactory):
    def create_trace(self, data):  # data = file_io (.tbn)
        return ElecTrace(data)
    
class Trace(metaclass=ABCMeta):  # Fluo trae, Elec trace
    @abstractmethod
    def read_data(self):
        pass
    
    @abstractmethod
    def create_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

"""
Concrete product
"""
class TsmFileIO(FileIO):
    def __init__(self, filename, filepath):
        # about file
        self.filename = filename
        self.file_path = filepath
        self.full_filename = filepath + filename
        self.header = 0 # byte: it needs to chage to str [self.header.decode()]
        self.elec_header = 0
        
        #about fluo frame
        self.full_frame = 0
        self.dark_frame = 0
        self.ch_frame = 0
        
        self.num_fluo_ch = 2  # Use () for PMT
        self.full_frame_interval = 0  # (ms)
        self.ch_frame_interval = 0  # (ms)
        self.data_pixel = np.empty([0,0])
        self.num_full_frame = np.empty([0,])
        self.num_ch_frame = np.empty([0,])
        self.full_3D_size = 0
        self.ch_3D_size = 0

        # about elec
        self.bnc_ratio = 0
        self.num_elec_ch = 0
        self.elec_interval = 0
        self.num_elec_data = 0
        
        # read data
        self.read_fileinfor()
        self.read_frame_data()
        
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
            print('Failed to import a TMS file infor.')
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
            print('Failed to import a TMS imaging data.')
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
    
    def read_trace_data(self):  # from .tbn files
        try:
            # read a header
            # https://fits.gsfc.nasa.gov/fits_primer.html
            elec_full_filename = self.full_filename[0:-3] + ('tbn')
            elec_header_list = np.fromfile(elec_full_filename,
                                                      np.int16, count=2)
            self.num_elec_ch = elec_header_list[0] * -1
            self.bnc_ratio = elec_header_list[1]
            self.elec_interval = \
            self.full_frame_interval/self.bnc_ratio
            self.num_elec_data = \
            self.num_full_frame * self.bnc_ratio
            
            # read elec data
            raw_elec = np.fromfile(elec_full_filename, np.float64, offset=4)
            self.elec_trace = raw_elec.reshape(self.num_elec_data, 
                                               self.num_elec_ch, 
                                               order = 'F')

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
        

class FullFrame(Frame):
    def __init__(self, data):
        super().__init__(data)

    def read_data(self):
        self.data = copy.deepcopy(self.file_io.full_frame)
        self.interval = copy.deepcopy(self.file_io.full_frame_interval)

        if self.data == 0:
            print('---------------------')
            print('Can not make 3D data')
            print('---------------------')
            return None


class ChFrame(Frame):
    def read_data(self):
        if self.data_type.find('ch1') >= 0:
            self.data = copy.deepcopy(self.file_io.ch_frame[:,:,:,0])
            self.interval = copy.deepcopy(self.file_io.ch_frame_interval)

        elif self.data_type.find('ch2') >= 0:
            self.data = copy.deepcopy(self.file_io.ch_frame[:,:,:,1])
            self.interval = copy.deepcopy(self.file_io.ch_frame_interval)
            
        else:
            print('---------------------')
            print('Can not make 3D data')
            print('---------------------')
            return None
        
class CellImage(Image):
    def __init__(self, data_3d, data_type):
        super().__init__(data_3d, data_type)
        self.data = 0
        def read_data(self):
            pass
        
        def update_data(self):
            pass

        def get_data(self):
            pass
        
class DifImage(Image):
        pass
        
class FluoTrace(Trace):
    def __init__(self, data_3d, data_type):
        super().__init__(data_3d, data_type)
        # data_3d and data_type are in super class
        self.data = 0
        self.time_data = 0

    def read_data(self, roi_obj):
        roi_xy_infor = roi_obj.get_data()  # [x, y, x_length, y_length, roi_num]
        full_frame
        num_frame = data_3d['full_frame']
        frame = self.data_container.imaging_data.ch_frame
        
        self.ch_fluo_trace_data = np.empty([num_frame, num_fluo_ch])
        
        for i in range(self.data_container.fileinfor.num_fluo_ch):
            trace = FluoTraceCreator.fluo_trace_creator(frame[:,:,:,i], roi_xy_infor)  # abstract method
            self.ch_fluo_trace_data[:,i] = trace
    
        print('Unpated ROI = ' + str(roi_xy_infor))
    
    def update_data(self, roi_obj):
        self.read_data(roi_obj)
        print('Recieved a notify message.')
    
    def get_data(self):
        pass

    def plot_elec_data(self, elec_ch):
        plt.plot(self.elec_trace[:, elec_ch])
        
    
class ElecTrace(Trace):
    pass
    
if __name__ == '__main__':
    filename = '20408A001.tsm'
    filepath = '..\\220408\\'
    factory_type = TmsIOFactory()
    data_file1 = factory_type.create_file_io(filename, filepath)
    
    filename = '20408A002.tsm'
    data_file2 = factory_type.create_file_io(filename, filepath)
    
    
    print(data_file1.filename)
    print(data_file2.filename)
    

