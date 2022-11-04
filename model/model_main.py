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
from model.displayed_data_factory import FullFluoTrace
from model.displayed_data_factory import ChFluoTrace
from model.displayed_data_factory import ElecTrace
from model.displayed_data_factory import CellImage
from model.displayed_data_factory import DifImage

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
        self.full_fluo_trace = FullFluoTrace(self.data_container, self.roi)
        self.ch_fluo_trace = ChFluoTrace(self.data_container, self.roi)

        self.elec_trace = ElecTrace(self.data_container)
        self.cell_image = CellImage(self.data_container, self.roi)
        #self.dif_image = np.array(0)
        print('imported model')

    def set_roi(self, type, val):
        pass
        
    def request_data(self, data_type):
        if data_type == 'full_fluo_trace':
            return self.full_fluo_trace.get_data()
        elif data_type == 'ch_fluo_trace':
            return self.ch_fluo_trace.get_data()


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
        
    #test.data_container.fileinfor.print_fileinfor()


    print(test.data_container.imaging_data.full_frame.shape)
    #print(test.data_container.elec_data.elec_trace.shape)
    #print(test.data_container.elec_data.elec_trace)
    #print(test.data_container.elec_data.elec_trace.shape)
    
    a = plt.figure()
    test.data_container.elec_data.plot_elec_data(4)
    b = plt.figure()
    test.data_container.imaging_data.show_frame(1,0)
    #test.request_data('full_fluo_trace')
    #test.request_data('ch_fluo_trace')
    c = plt.figure()
    test.full_fluo_trace.plot_trace()
    test.ch_fluo_trace.plot_trace(0)
    d = plt.figure()
    test.elec_trace.plot_trace(0)
    e = plt.figure()
    test.cell_image.show_frame(0)
    
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

