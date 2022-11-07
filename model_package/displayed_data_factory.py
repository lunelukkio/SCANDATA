# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:04:55 2022

lunelukkio@gmail.com
"""


from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


"""
Abstract desplayeddata product
"""
class DisplayedData(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def get_object(self):
        pass

    @abstractmethod
    def mod_data(self):
        pass
    
    @abstractmethod
    def update(self):
        pass

        
"""
Concrete desplayeddata product
"""
class FullFluoTrace(DisplayedData):
    def __init__(self, data_container, roi_val):
        self.data_container = data_container
        self.roi_val = roi_val

        self.full_fluo_trace = np.empty([0,])
        self.full_fluo_time = np.empty([0,])
        self.full_fluo_mod = 0
        
        self.create_time()

    def create_data(self):
        print('Full fluo trace')
        roi_xy_infor = self.roi_val.get_data()  # [x, y, x_length, y_length, roi_num]
        frame = self.data_container.imaging_data.full_frame
        
        self.full_fluo_trace = FluoTraceCreator.fluo_trace_creator(
            frame, roi_xy_infor)
        
    def create_time(self):
        time_start = self.data_container.fileinfor.full_frame_interval
        num_frame = self.data_container.fileinfor.num_full_frame
        time_last = num_frame * time_start
        self.full_fluo_time = np.linspace(time_start, time_last, num_frame)
        
    def get_data(self):
        print('Get full fluo trace.')
        return self.full_fluo_trace
    
    def get_object(self):
        return self

    def mod_data(self):
        pass
    
    def update(self):
        self.create_data()
        print('Updated')
    
    def print_trace(self):
        print(self.full_fluo_trace)
        
    def plot_trace(self):
        plt.plot(self.full_fluo_trace[:])
    
    
class ChFluoTrace(DisplayedData):
    def __init__(self, data_container, roi_val):
        self.roi_val = roi_val
        self.data_container = data_container
        self.ch_fluo_trace = np.empty([0, 0])
        self.ch_fluo_time = np.empty([0,])
        
        self.create_time()

    def create_data(self):
        print('Ch fluo trace')
        roi_xy_infor = self.roi_val.get_data()  # [x, y, x_length, y_length, roi_num]
        num_fluo_ch = self.data_container.fileinfor.num_fluo_ch
        num_frame = self.data_container.fileinfor.num_ch_frame
        frame = self.data_container.imaging_data.ch_frame
        
        self.ch_fluo_trace = np.empty([num_frame, num_fluo_ch])
        
        for i in range(self.data_container.fileinfor.num_fluo_ch):
            trace = FluoTraceCreator.fluo_trace_creator(frame[:,:,:,i], roi_xy_infor)  # abstract method
            self.ch_fluo_trace[:,i] = trace
            
    def create_time(self):

        time_start = self.data_container.fileinfor.ch_frame_interval
        num_frame = self.data_container.fileinfor.num_ch_frame
        time_last = num_frame * time_start
        self.ch_fluo_time = np.linspace(time_start, time_last, num_frame)
        
    def get_data(self):
        return self.ch_fluo_trace
    
    def get_object(self):
        return self

    def mod_data(self):
        pass
    
    def update(self):
        self.create_data()
        print('Updated')
    
    def plot_trace(self, ch):
        plt.plot(self.ch_fluo_trace[:, ch])


class ElecTrace(DisplayedData):
    def __init__(self, data_container, elec_val):
        self.elec_val = elec_val
        self.data_container = data_container
        self.elec_trace = np.empty([0,])

    def create_data(self):
        print('Elec trace')
        self.elec_trace = self.data_container.elec_data.elec_trace

    def get_data(self):
        return self.elec_trace
    
    def get_object(self):
        return self

    def mod_data(sel):
        pass
    
    def update(self):
        self.create_data()
        print('Updated')
    
    def plot_trace(self, ch):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.elec_trace[:, ch])
        plt.show()


class CellImage(DisplayedData):
    def __init__(self, data_container, cell_image_val):
        self.cell_image_val = cell_image_val
        self.data_container = data_container
        
        pixel = data_container.fileinfor.data_pixel
        num_ch = data_container.fileinfor.num_fluo_ch
        self.cell_image_data = np.empty([pixel[0],pixel[1],num_ch])

    def create_data(self):
        print('Cell image')
        frame = self.data_container.imaging_data.ch_frame
        num_ch = self.data_container.fileinfor.num_fluo_ch
        frame_num = self.cell_image_val.get_data()
        
        if frame_num[1] - frame_num[0] == 0:
            for i in range(num_ch):
                self.cell_image_data[:, :, i] = frame[:, :, frame_num[0], i]
                
        elif frame_num[1] - frame_num[0] > 0: 
            for i in range(num_ch):
                self.cell_image_data[:, :, i] = np.mean(frame[:, :, frame_num[0]:frame_num[1], i], axis = 2)

        else:
            print("The start frame shoud be less than the end frame.")
            self.cell_image_data = None
        
    def get_data(self):
        return self.cell_image_data
    
    def get_object(self):
        return self

    def mod_data(sel):
        pass
    
    def update(self):
        self.create_data()
        print('updated')

    def show_frame(self, ch):
            plt.imshow(self.cell_image_data[:, :, ch])

    
class DifImage(DisplayedData):
    def __init__(self, original_fluo_frame):
        self.original_fluo_frame = original_fluo_frame

    def create_data(self):
        print('Dif cell image.')
        
    def get_data(self):
        pass
    
    def get_object(self):
        return self

    def mod_data(sel):
        pass
    
    def update():
        pass


"""
common class
"""
class FluoTraceCreator:
    @staticmethod
    def fluo_trace_creator(frame, RoiVal):
        x = RoiVal[0]
        y = RoiVal[1]
        x_length = RoiVal[2]
        y_length = RoiVal[3]
        mean_data = np.mean(frame[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data