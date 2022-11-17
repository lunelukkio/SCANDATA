# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""

from abc import ABCMeta, abstractmethod
#from model_package.roi import Roi, TimeWindow

from model_package.data_factory import TsmDataFactory, DaDataFactory
from data_factory import Data3D, Data2D, Data1D


"""
abstract class
"""
class ModelInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def create_data_file(self, filename, filepath):
        pass
        
    @abstractmethod
    def set_data(self, control_type, val):
        pass
    
    @abstractmethod
    def get_object(self, data_type):
        pass
    
    @abstractmethod
    def set_mod(self, control_type, mod_type, val):
        pass
    
    @abstractmethod
    def reset(self):
        pass


"""
Concrete class
"""
class Model(ModelInterface):
    def __init__(self):

        self.filename = []
        self.filepath = []
        
        # experiments data
        self.data_file_obj = []  # data_file instances
        self.data_file_name = []  # keys for instances of data_file
        self.data_file = {}  # dictionary for data_files
        
        # data controllers for any files
        self.roi_obj = []
        self.roi_name = []
        self.roi = {}
        self.time_window_obj = []
        self.time_window_name = []
        self.time_window = {}
        self.line_obj = []
        self.line_name = []
        self.line = {}
        

        print('Created a model.')

    def create_data_file(self, filename, filepath):
        self.filename.append(filename)
        self.filepath.append(filepath)
        
        if filename.find('.tsm') > 0:
            factory_type = TsmDataFactory()
        elif filename.find('.da') > 0:
            factory_type = DaDataFactory()
        else:
            print('---------------------')
            print('Can not find the file')
            print('---------------------')
            return None
        
        self.data_file_obj.append(DataFile(filename, filepath, factory_type))
        self.data_file = dict(zip(self.filename, self.data_file_obj))  # filename = [list]

    def set_data(self, control_type, val):
        raise NotImplementedError
    
    def get_object(self, data_file):
        pass
    
    def set_mod(self, control_type, mod_type, val):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError


class DataFile:
    def __init__(self, filename, filepath, factory_type):
        self.filename = filename
        self.filepath = filepath
        self.factory_type = factory_type
        self.file_io = factory_type.create_file_io(self.filename, self.filepath)
        
        # Main data objects
        
        self.data_3d_obj = []  #data instances
        self.data_2d_obj = []
        self.data_1d_obj = []
        
        self.data_3d_type = []  # 'full_frame', 'ch_frame'
        self.data_2d_type = []  # 'cell_image', 'dif_image'
        self.data_1d_type = []  # 'full_trace', 'ch1_trace1', 'elec_trace1', 'bg_trace'


        self.data_3d = {}  # dictionaly, 
        self.data_2d = {}
        self.data_1d = {}

        print('created a data_file.')
        
        # it need dependency injection
        #self.data_3d['full_frame'].split_data(2)

    def create_data_3d(self, data_type):
        self.data_3d_obj.append(self.factory_type.create_data_3d(self.file_io, data_type))
        self.data_3d_type.append(data_type)
        self.data_3d = dict(zip(self.data_3d_type, self.data_3d_obj))
         
    def create_data_2d(self):
        self.data_2d.append(Data2D())
        self.data_2d[len(self.data_2d)-1].create_data()
        
    def create_data_1d(self):
        self.data_1d.append(Data1D())
        self.data_1d[len(self.data_1d)-1].create_data()

        

if __name__ == '__main__':
    filename = '20408A001.tsm'
    filepath = '..\\220408\\'
    model = Model()
    model.create_data_file(filename, filepath)
    model.data_file['20408A001.tsm'].create_data_3d('full_frame')
    model.data_file['20408A001.tsm'].create_data_3d('ch1_frame')
    model.data_file['20408A001.tsm'].create_data_3d('ch2_frame')
    
    model.data_file['20408A001.tsm'].create_data_1d('ch2_frame')
    
    
    print(model.data_file['20408A001.tsm'].filename)
    print(model.data_file['20408A001.tsm'].data_3d)
    model.data_file['20408A001.tsm'].data_3d['ch2_frame'].show_frame(10)


    
    
    print('オブジェクト指向での例外処理で変数をクリアして抜ける')
