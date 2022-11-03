# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""

from abc import ABCMeta, abstractmethod
from model.roi import Roi
from model.experimentdata_factory import TsmDataFactory
from model.experimentdata_factory import DaDataFactory
from model.displayed_data_factory import FullFluoTraceFactory
from model.displayed_data_factory import ChFluoTraceFactory
from model.displayed_data_factory import ElecTraceFactory
from model.displayed_data_factory import CellImageFactory
from model.displayed_data_factory import DifImageFactory

class ModelInterface(metaclass=ABCMeta):

    @abstractmethod
    def set_roi(self, type, val):
        pass
    
    @abstractmethod
    def request_data(self, data_type):
        pass
    

class ModelMain(ModelInterface):
    def __init__(self, filename, filepath):
        self.data_container = DataContainer(filename, filepath)
        self.roi = Roi()
        self.full_fluo_trace = 0
        self.ch_fluo_trace = 0

        #self.elec_trae = np.array(0)
        #self.cell_image = np.array(0)
        #self.dif_image = np.array(0)
        print('imported model')

    def set_roi(self, type, val):
        pass
        
    def request_data(self, data_type):
        if data_type == 'full_fluo_trace':
            factory_type = FullFluoTraceFactory()
            self.full_fluo_trace = factory_type.create_displayed_data(self.data_container, self.roi)
        elif data_type == 'ch_fluo_trace':
            factory_type = ChFluoTraceFactory()
            self.ch_fluo_trace = factory_type.create_displayed_data(self.data_container, self.roi)
            




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
        

"""
for observer method
"""
class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def _notify_update(self, message):
        for observer in self._observers:
            observer.update(message)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    filename = '20408A001.tsm'
    filepath = 'E:\\Data\\2022\\220408\\'
    #filepath = 'C:\\Users\\lulul\\マイドライブ\\Programing\\Python\\220408\\'
    test = ModelMain(filename, filepath)
        
    test.data_container.fileinfor.print_fileinfor()
    #test.data_container.imaging_data.print_frame()

    print(test.data_container.imaging_data.full_frame.shape)
    #print(test.data_container.elec_data.elec_trace.shape)
    #print(test.data_container.elec_data.elec_trace)
    #print(test.data_container.elec_data.elec_trace.shape)
    
    a = plt.figure()
    test.data_container.elec_data.plot_elec_data(1)
    b = plt.figure()
    test.data_container.imaging_data.show_frame(2,0)
    test.request_data('full_fluo_trace')
    test.request_data('ch_fluo_trace')
    c = plt.figure()
    test.full_fluo_trace.plot_trace()
    test.ch_fluo_trace.plot_trace(0)
    
    print(type(test.ch_fluo_trace))
    print(test.ch_fluo_trace.ch_fluo_trace.shape)
    #print(test.ch_fluo_trace.ch_fluo_trace)
    
    #roi_data = [45, 45]
    #test.displayed_data.create_full_trace(roidata)
    
    
    #最終的にこう書く
    #test.set_roi(roi, 10, 10, 2, 2)  # (x, y, x_length, y_lentch)
    #オブザーバーでそれぞれのobjectに変更通知->それぞれのobjectが自身を変更
    
    #test.set_roi(diff, 50, 100, 5, 5)
    #オブザーバーでそれぞれのobjectに変更通知->それぞれのobjectが自身を変更
    #test.create_data(dif_image)

