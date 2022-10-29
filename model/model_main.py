# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""
from model.experimentdata_factory import TsmDataFactory
from model.experimentdata_factory import DaDataFactory
from model.displayed_data_factory import DisplayedFluoTraceFactory
from model.displayed_data_factory import DisplayedElecTraceFactory
from model.displayed_data_factory import DisplayedImageFactory


class Model:
    def __init__(self, filename, filepath):
        self.data_container = DataContainer(filename, filepath)

        print('imported model')


class DataContainer:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        
        self.displayed_fluo_trace = 0
        self.cell_image = 0
        
        print('imported Data Container')
        
        if filename.find('.tsm') > 0:
            data_factory_type = TsmDataFactory()
        elif filename.find('.da') > 0:
            data_factory_type = DaDataFactory()
        else:
            print('no file')
            return
        
        # read data from a file
        self.file_infor = data_factory_type.create_fileinfor(self.filename, self.filepath)
        self.imaging_data = data_factory_type.create_imaging_data(self.file_infor)
        self.elec_data = data_factory_type.create_elec_data(self.file_infor)
        
        self.create_fluo_trace()  # add roi
        self.create_cell_image()


    def create_fluo_trace(self):
        self.data_type = DisplayedFluoTraceFactory()
        self.displayed_fluo_trace = self.data_type.create_displayed_data(self.imaging_data)
        
    def create_cell_image(self):
        self.data_type = DisplayedImageFactory()
        self.cell_image = self.data_type.create_displayed_data(self.imaging_data)


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
    import numpy as np
    
    filename = '20408A001.tsm'
    filepath = 'E:\\Data\\2022\\220408\\'
    #filepath = 'C:\\Users\\lulul\\マイドライブ\\Programing\\Python\\220408\\'
    
    test= Model(filename, filepath)
    
    test.data_container.file_infor.print_fileinfor()
    test.data_container.imaging_data.print_frame()

    #print(test.data_container.elec_data.elec_trace)
    #print(test.data_container.elec_data.elec_trace.shape)
    
    a = plt.figure()
    test.data_container.elec_data.plot_elec_data(1)
    b = plt.figure()
    test.data_container.imaging_data.show_frame(0,1)
    


