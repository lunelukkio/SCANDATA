# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""

from abc import ABCMeta, abstractmethod
from model_package.roi import RoiVal
from model_package.roi import ElecVal
from model_package.roi import CellImageVal
from model_package.experimentdata_factory import TsmDataFactory
from model_package.experimentdata_factory import DaDataFactory
from model_package.displayed_data_factory import FullFluoTrace
from model_package.displayed_data_factory import ChFluoTrace
from model_package.displayed_data_factory import ElecTrace
from model_package.displayed_data_factory import CellImage

class ModelInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def create_model(self, filename, filepath):
        pass

    @abstractmethod
    def set_data(self, control_type, val):  # control_type = RoiVal()
        pass
    
    @abstractmethod
    def get_data(self, data_type):
        pass
    
    @abstractmethod
    def get_object(self, data_type):
        pass
    
    
class Model(ModelInterface):
    def __init__(self):
        self.filename = 'no file'
        self.filepath = 'no path'
        self.data_type = None
        self.data_container = None
        
        self.full_fluo_trace = []
        self.bg_full_fluo_trace = []
        self.ch_fluo_trace = []
        self.bg_ch_fluo_trace = []
        
        self.roi = []
        self.bg_roi = []
        self.elec_val = 0
        self.cell_image_val = 0


        
        print('Imported a model class.')

    def create_model(self, filename, filepath):
        
        if filename.find('.tsm') > 0:
            data_type = TsmDataFactory()
        elif filename.find('.da') > 0:
            data_type = DaDataFactory()
        else:
            print('no file')
            return
        
        self.data_container = DataContainer(filename, filepath, data_type)
        if self.data_container is None:
            print('No file')
            return None

        # for displayed data
        self.full_fluo_trace.append(FullFluoTrace(self.data_container))
        self.bg_full_fluo_trace.append(FullFluoTrace(self.data_container))
        self.ch_fluo_trace.append(ChFluoTrace(self.data_container))
        self.bg_ch_fluo_trace.append(ChFluoTrace(self.data_container))
        
        self.elec_trace = ElecTrace(self.data_container)
        self.cell_image = CellImage(self.data_container)
        
        # for control valiables
        self.roi.append(RoiVal())
        self.bg_roi.append(RoiVal())
        self.elec_val = ElecVal()
        self.cell_image_val = CellImageVal()
        
        # add traces to roi_val observer
        self.roi[0].add_observer(self.full_fluo_trace[0])
        self.roi[0].add_observer(self.ch_fluo_trace[0])
        self.bg_roi[0].add_observer(self.bg_full_fluo_trace[0])
        self.bg_roi[0].add_observer(self.bg_ch_fluo_trace[0])
        self.elec_val.add_observer(self.elec_trace)
        self.cell_image_val.add_observer(self.cell_image)

    def set_data(self, control_type, val):
        control_type.set_data(val)

    def get_data(self, data_type):
        return data_type.get_data()
    
    def get_object(self, data_type):
        return data_type.get_object()
    
    def create_roi(self):
        self.roi.append(RoiVal())
        self.full_fluo_trace.append(FullFluoTrace(self.data_container))
        self.ch_fluo_trace.append(ChFluoTrace(self.data_container))
        
        self.roi[len(self.roi)-1].add_observer(self.full_fluo_trace[len(self.roi)-1])
        self.roi[len(self.roi)-1].add_observer(self.ch_fluo_trace[len(self.roi)-1])
        print(len(self.roi))
        

class DataContainer:
    def __init__(self, filename, filepath, factory_type):
        self.filename = filename
        self.filepath = filepath
        

        
        # read data from a file
        self.fileinfor = factory_type.create_fileinfor(self.filename, self.filepath)
        self.imaging_data = factory_type.create_imaging_data(self.fileinfor)
        self.elec_data = factory_type.create_elec_data(self.fileinfor)

        print('Imported a data container class.')
        
        
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import time
    import copy

    
    filename = '20408B002.tsm'
    filepath = 'E:\\Data\\2022\\220408\\'
    #filepath = 'C:\\Users\\lulul\\マイドライブ\\Programing\\Python\\220408\\'
    model = Model()

    model.create_model(filename, filepath)
    model.create_roi()  # The second roi
    model.create_roi()
    
    #model.data_container.fileinfor.print_fileinfor()
    
    # for cell image
    model.set_data(model.cell_image_val,[0,1])
    cell = model.get_object(model.cell_image)
    d = plt.figure()
    plt.imshow(cell.cell_image_data[:,:,0], cmap='gray', interpolation='none')
    fig, ax = plt.subplots()
    
    model.set_data(model.roi[0],[10,10,10,1])
    model.set_data(model.bg_roi[0],[32,32,3,3])
    
    fluo_trace = model.get_object(model.ch_fluo_trace[0])
    bg_trace = model.get_object(model.bg_ch_fluo_trace[0])
    fluo2_trace = model.get_object(model.ch_fluo_trace[1])
    fluo3_trace = model.get_object(model.ch_fluo_trace[2])

    ax.plot(fluo_trace.ch_fluo_time_data, fluo_trace.ch_fluo_trace_data[:,0], color='blue')
    model.set_data(model.roi[1],[20,20,50,50])
    ax.plot(fluo2_trace.ch_fluo_time_data, fluo2_trace.ch_fluo_trace_data[:,0], color='red')
    ax.plot(bg_trace.ch_fluo_time_data, bg_trace.ch_fluo_trace_data[:,0], color='green')
    model.set_data(model.roi[2],[10,10,10,10])
    ax.plot(fluo3_trace.ch_fluo_time_data, fluo3_trace.ch_fluo_trace_data[:,0], color='yellow')
    
   
    """   
    model.set_data(model.elec_val, None)
    elec = model.get_data(model.elec_trace)
    e = plt.figure()
    plt.plot(elec[:,1])

    model.set_data(model.cell_image_val,[0,99])
    cell = model.get_object(model.cell_image)
    d = plt.figure()
    plt.imshow(cell.cell_image_data[:,:,1], cmap='gray', interpolation='none')
    
    val = [10,10,50,50,1]
    model.set_data(model.roi_val, val)
    model.ch_fluo_trace.create_data
    a = plt.figure()
    model.data_container.elec_data.plot_elec_data(0)
    b = plt.figure()
    model.data_container.imaging_data.show_frame(1,0)
    
    
    print(model.data_container.imaging_data.full_frame.shape)
    print(model.data_container.elec_data.elec_trace.shape)
    print(model.data_container.elec_data.elec_trace)
    print(model.data_container.elec_data.elec_trace.shape)
    
    e = plt.figure()
    model.cell_image.show_frame(0)
    
    print(type(model.ch_fluo_trace))
    print(model.ch_fluo_trace.ch_fluo_trace.shape)
    #print(model.ch_fluo_trace.ch_fluo_trace)
    
    #roi_data = [45, 45]
    #model.displayed_data.create_full_trace(roidata)
    val = [1,1,1,1,1]
    model.set_data(model.roi_val, val)
    print(model.roi_val.get_data())
    
        
    model.set_data(model.roi_val,[5,5,1,1,1])
    ch_trace = model.get_data(model.ch_fluo_trace)
    a = plt.figure()
    plt.plot(ch_trace[:,0])
    
    model.set_data(model.roi_val,[10,10,50,50,1])
    model.ch_fluo_trace.create_data()
    ch_trace = model.get_data(model.ch_fluo_trace)
    b = plt.figure()
    plt.plot(ch_trace[:,0])
    
    electrace = model.get_data(model.elec_trace)
    c = plt.figure()
    plt.plot(electrace[:,1])
    
    #final code
    #model.set_data(roi_cval, [10, 10, 2, 2, 1])  # (x, y, x_length, y_lentch, roi#)
    #observer tell traces
    #traces change data by myself
    
    #model.get_data(ch_fluo_trace)

    """
    print('複数の動的インスタンスの作り方')
    print('オブジェクト指向での例外処理で変数をクリアして抜ける')
    print('trace classとroi classにリセット関数をつけて、model interfaceに加える。その後mmodel test modelインスタンスを作った後に起動')