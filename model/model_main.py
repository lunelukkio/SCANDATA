# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
main module for model
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
        
        """read data from a file"""
        self.file_infor = data_factory_type.create_FileInfor(self.filename, self.filepath)
        self.imaging_data = data_factory_type.create_ImagingData(self.file_infor)
        
        self.create_fluo_trace()  # add roi
        self.create_cell_image()
        


    def create_fluo_trace(self):
        self.data_type = DisplayedFluoTraceFactory()
        self.displayed_fluo_trace = self.data_type.create_displayed_data(self.imaging_data)
        
    def create_cell_image(self):
        self.data_type = DisplayedImageFactory()
        self.cell_image = self.data_type.create_displayed_data(self.imaging_data)

class DisplayedFluoTrace:
    def __init__(self, original_data):
        self.file_infor = original_data.file_infor


class DisplayedElecTrace:
    def __init__(self, original_data):
        self.file_infor = original_data.file_infor


class DisplayedImage:
    def __init__(self, original_data):
        self.file_infor = original_data.file_infor


"""where should it be located"""
class PrintFileName:
    @staticmethod
    def print_filename(self):
        print(self.file_infor.filename)
        print('This is a ' + self.__class__.__name__)


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
    filename = '20408A001.tsm'
    filepath = 'E:\\Data\\2022\\220408\\'
    #filepath = 'C:\\Users\\lulul\\マイドライブ\\Programing\\Python\\220408\\'
    test= Model(filename, filepath)

    print(test.data_container.imaging_data.imaging_data.shape)
    test.data_container.file_infor.print_header()
    test.data_container.imaging_data.print_imaging_data()
    print(vars(test.data_container.imaging_data))
    test.data_container.displayed_fluo_trace.get_data()
