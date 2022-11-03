# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:04:55 2022

lunelukkio@gmail.com
"""


from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

"""
Abstract desplayeddata factory
"""
class DisplayedDataFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_displayed_data(self, data_container, roi):
        pass


"""
Abstract desplayeddata product
"""
class DisplayedData(metaclass=ABCMeta):
    @abstractmethod
    def create_data(self):
        pass

    @abstractmethod
    def mod_data(self):
        pass



"""
Concrete factory
"""
class FullFluoTraceFactory(DisplayedDataFactory):

    def create_displayed_data(self, data_container, roi):
        return FullFluoTrace(data_container, roi)


class ChFluoTraceFactory(DisplayedDataFactory):

    def create_displayed_data(self, data_container, roi):
        return ChFluoTrace(data_container, roi)


class ElecTraceFactory(DisplayedDataFactory):

    def create_displayed_data(self, data_container, roi):
        return ElecTrace(data_container, roi)
    
    
class CellImageFactory(DisplayedDataFactory):

    def create_displayed_data(self, data_container, roi):
        return CellImage(data_container, roi)
    
class DifImageFactory(DisplayedDataFactory):

    def create_displayed_data(self, data_container, roi):
        return DifImage(data_container, roi)
        
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
        
        trace = FluoTraceCreator.fluo_trace_creator(
            frame[:,:,:,0], roi_xy_infor)
        self.ch_fluo_trace[:,0] = trace
        
        self.ch_fluo_trace[:,1] = FluoTraceCreator.fluo_trace_creator(
            data_container.imaging_data.ch_frame[:,:,:,1], roi_xy_infor)

    def mod_data(self):
        pass
    
    def plot_trace(self, ch):
        plt.plot(self.ch_fluo_trace[:, ch])


class ElecTrace(DisplayedData):
    def __init__(self, original_elec_data):
        self.original_elec_data = original_elec_data

    def create_data(self):
        self.original_elec_data.print_filename()

    def mod_data(sel):
        pass


class CellImage(DisplayedData):
    def __init__(self, original_fluo_frame):
        self.original_fluo_frame = original_fluo_frame

    def create_data(self):
        print('this is a cell image')

    def mod_data(sel):
        pass
    
class DifImage(DisplayedData):
    def __init__(self, original_fluo_frame):
        self.original_fluo_frame = original_fluo_frame

    def create_data(self):
        print('this is a cell image')

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