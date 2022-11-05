# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""

from abc import ABCMeta, abstractmethod
from model_package.roi import RoiVal
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
    def set_val(self, control_type, val):  # control_type = RoiVal()
        pass
    
    @abstractmethod
    def request_data(self, data_type):
        pass
    

class Model(ModelInterface):
    def __init__(self):
        self.filename = 'no file'
        self.filepath = 'no path'
        self.data_container = None
        self.roi = 0
        
        self.control_type = 0
        
    def create_model(self, filename, filepath):
        self.data_container = DataContainer(filename, filepath)
        if self.data_container is None:
            print('no file')
            return
        self.roi_val = RoiVal()
        self.cell_image_val = CellImageVal()
        self.full_fluo_trace = FullFluoTrace()
        self.full_fluo_trace.create_data(self.data_container, self.roi_val)
        self.ch_fluo_trace = ChFluoTrace()
        self.ch_fluo_trace.create_data(self.data_container, self.roi_val)

        self.elec_trace = ElecTrace(self.data_container)
        self.cell_image = CellImage(self.data_container, self.roi_val)
        #self.dif_image = np.array(0)
        print('imported model')

    def set_val(self, control_type, val):
        control_type.set_val(val)
        print('sent val = ' + str(val))

    def request_data(self, data_type):
        data_type.get_data()
        print('Request received')


class DataContainer:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        
        print('imported Data Container')
        
        if filename.find('.tsm') > 0:
            factory_type = TsmDataFactory()
        elif filename.find('.da') > 0:
            factory_type = DaDataFactory()
        else:
            print('no file')
            return
        
        # read data from a file
        self.fileinfor = factory_type.create_fileinfor(self.filename, self.filepath)
        self.imaging_data = factory_type.create_imaging_data(self.fileinfor)
        self.elec_data = factory_type.create_elec_data(self.fileinfor)
        


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    filename = '20408A001.tsm'
    filepath = 'E:\\Data\\2022\\220408\\'
    #filepath = 'C:\\Users\\lulul\\マイドライブ\\Programing\\Python\\220408\\'
    model= Model()
    model.create_model(filename, filepath)
        
    #model.data_container.fileinfor.print_fileinfor()


    print(model.data_container.imaging_data.full_frame.shape)
    #print(model.data_container.elec_data.elec_trace.shape)
    #print(model.data_container.elec_data.elec_trace)
    #print(model.data_container.elec_data.elec_trace.shape)
    
    val = [10,10,50,50,1]
    model.set_val(model.roi_val, val)
    model.ch_fluo_trace.create_data
    a = plt.figure()
    model.data_container.elec_data.plot_elec_data(0)
    b = plt.figure()
    model.data_container.imaging_data.show_frame(1,0)
    #model.request_data('full_fluo_trace')
    #model.request_data('ch_fluo_trace')
    c = plt.figure()
    model.ch_fluo_trace.plot_trace(0)
    d = plt.figure()
    model.elec_trace.plot_trace(0)
    e = plt.figure()
    model.cell_image.show_frame(0)
    
    print(type(model.ch_fluo_trace))
    print(model.ch_fluo_trace.ch_fluo_trace.shape)
    #print(model.ch_fluo_trace.ch_fluo_trace)
    
    #roi_data = [45, 45]
    #model.displayed_data.create_full_trace(roidata)
    val = [1,1,1,1,1]
    model.set_val(model.roi_val, val)
    print(model.roi_val.get_data())
    
    a = model.request_data(ChFluoTrace())
    print(a)
    
    #final code
    #model.set_val(roi_cval, [10, 10, 2, 2, 1])  # (x, y, x_length, y_lentch, roi#)
    #observer tell traces
    #traces change data by myself
    
    #model.get_data(ch_fluo_trace)
    #send to view
model.request_dataが空になる
ch_fluo_trace.create_dataに引数を持たせてはいけない。自身で更新
