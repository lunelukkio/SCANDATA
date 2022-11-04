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
    def mod_data(self):
        pass


        
"""
Concrete desplayeddata product
"""
class FullFluoTrace(DisplayedData):
    def __init__(self, data_container, roi):
        self.full_fluo_trace = np.empty(0)
        self.create_data(data_container, roi)
        
    def create_data(self, data_container, roi):
        print('this is a full fluo trace')
        frame = data_container.imaging_data.full_frame
        roi_xy_infor = [roi.x, roi.y, roi.x_length, roi.y_length]
        
        self.full_fluo_trace = FluoTraceCreator.fluo_trace_creator(
            frame, roi_xy_infor)
        #return self.full_fluo_trace
        
    def get_data(self):
        return self.full_fluo_trace

    def mod_data(self):
        pass
    
    def print_trace(self):
        print(self.full_fluo_trace)
        
    def plot_trace(self):
        plt.plot(self.full_fluo_trace[:])
    
    
class ChFluoTrace(DisplayedData):
    def __init__(self, data_container, roi):
        self.ch_fluo_trace = np.empty([0, 0])
        self.create_data(data_container, roi)

    def create_data(self, data_container, roi):
        print('this is ch fluo trace')
        num_fluo_ch = data_container.fileinfor.num_fluo_ch
        num_frame = data_container.fileinfor.num_frame//num_fluo_ch
        
        frame = data_container.imaging_data.ch_frame
        roi_xy_infor = [roi.x, roi.y, roi.x_length, roi.y_length]
        self.ch_fluo_trace = np.empty([num_frame, num_fluo_ch])
        
        for i in range(data_container.fileinfor.num_fluo_ch):
            trace = FluoTraceCreator.fluo_trace_creator(frame[:,:,:,i], roi_xy_infor)
            self.ch_fluo_trace[:,i] = trace
        

    def get_data(self):
        return self.ch_fluo_trace

    def mod_data(self):
        pass
    
    def plot_trace(self, ch):
        plt.plot(self.ch_fluo_trace[:, ch])


class ElecTrace(DisplayedData):
    def __init__(self, data_container):
        self.create_data(data_container)

    def create_data(self, data_container):
        self.elec_trace = data_container.elec_data.elec_trace

    def get_data(self):
        return self.elec_trace

    def mod_data(sel):
        pass
    
    def plot_trace(self, ch):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.elec_trace[:, ch])
        plt.show()


class CellImage(DisplayedData):
    def __init__(self, data_container, roi):
        pixel = data_container.fileinfor.data_pixel
        num_ch = data_container.fileinfor.num_fluo_ch
        self.cell_image = np.empty([pixel[0],pixel[1],num_ch])
        
        self.create_data(data_container, roi)

    def create_data(self, data_container, roi):
        print('this is a cell image')
        frame = data_container.imaging_data.ch_frame
        num_ch = data_container.fileinfor.num_fluo_ch
        roi = roi.ave_num_cell_image
        
        if roi[1] - roi[0] == 0:
            for i in range(num_ch):
                self.cell_image[:, :, i] = frame[:, :, roi[0], i]
                
        elif roi[1] - roi[0] > 0: 
            for i in range(num_ch):
                self.cell_image[:, :, i] = np.mean(frame[:, :, roi[0]:roi[1], i], axis = 2)
        
    def get_data(self):
        return self.cell.image

    def mod_data(sel):
        pass

    def show_frame(self, ch):
            plt.imshow(self.cell_image[:, :, ch])

    
class DifImage(DisplayedData):
    def __init__(self, original_fluo_frame):
        self.original_fluo_frame = original_fluo_frame

    def create_data(self):
        print('this is a cell image')
        
    def get_data(self):
        pass

    def mod_data(sel):
        pass

"""
common class
"""
class FluoTraceCreator:
    @staticmethod
    def fluo_trace_creator(frame, roi):
        x = roi[0]
        y = roi[1]
        x_length = roi[2]
        y_length = roi[3]
        mean_data = np.mean(frame[x:x+x_length, y:y+y_length, :], axis = 0)
        mean_data = np.mean(mean_data, axis = 0)
        return mean_data