# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""

from abc import ABCMeta, abstractmethod
import re  # call regular expression
import pprint
from model_package.roi import Roi, TimeWindow, FrameShift, Line
from model_package.data_factory import TsmFileIO
from model_package.data_factory import FullFrameFactory, ChFrameFactory
from model_package.data_factory import CellImageFactory, DifImageFactory
from model_package.data_factory import ElecTraceFactory, FullTraceFactory, ChTraceFactory

"""
abstract class
"""
class ModelInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_data_objects(self, filename, filepath):
        pass
    
    @abstractmethod
    def create_control_objects(self):
        pass
        
    @abstractmethod
    def set_data(self, control_type, val):
        pass
    
    @abstractmethod
    def get_data(self, filename, data_type):
        pass
    
    @abstractmethod
    def set_mod(self, control_type, mod_type, val):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
    
class DataFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_data_factory(self, model, filename, filepath):
        pass
    
class TsmFactory(DataFactory):
    def create_data_factory(self, model,filename, filepath):
        return TsmData(model, filename, filepath)
    
class DaFactory(DataFactory):
    def create_data_factory(self, model, filename, filepath):
        raise NotImplementedError
    
class AbfFactory(DataFactory):
    def create_data_factory(self, model, filename, filepath):
        raise NotImplementedError
        
class WcpFactory(DataFactory):
    def create_data_factory(self, model, filename, filepath):
        raise NotImplementedError


class DataInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_file_io(self):
        pass
    
    @abstractmethod
    def create_frame_obj(self):
        pass
    
    @abstractmethod
    def create_image_obj(self):
        pass
    
    @abstractmethod
    def create_trace_obj(self):
        pass
    
    @abstractmethod
    def get_data(self, data_name):
        pass


"""
Concrete class
"""
class Model(ModelInterface):
    def __init__(self):
        # experiments data
        self.filename = []
        self.filepath = []
        self.data_file_obj = []  # data_file instances
        self.data_file = {}  # dictionary for data_files

        # data controllers for any files
        self.roi_name = []
        self.roi_obj = []
        self.roi = {}
        
        self.time_window_name = []
        self.time_window_obj = []
        self.time_window = {}
        
        self.frame_shift_name = []
        self.frame_shift_obj = []
        self.frame_shift = {}
        
        self.line_name = []
        self.line_obj = []
        self.line = {}

        print('Created a model.')
        
        self.create_control_objects()
          
    def create_data_objects(self, filename, filepath):
        factory_type = self.file_type_checker(filename)
        self.filename.append(filename)
        self.filepath.append(filepath)
        self.data_file_obj.append(factory_type.create_data_factory(self, filename, filepath))
        self.data_file = dict(zip(self.filename, self.data_file_obj))

    def create_control_objects(self):
        self.create_roi()
        self.create_time_window()
        self.create_frame_shift()
        self.create_line()

    def create_roi(self):
        product = Roi()
        self.roi_obj.append(product)
        self.roi_name.append('Roi' + str(product.num_instance))
        self.roi = dict(zip(self.roi_name, self.roi_obj))  # filename = [list]
        
    def create_time_window(self):
        product = TimeWindow()
        self.time_window_obj.append(product)
        self.time_window_name.append('TimeWindow' + str(product.num_instance))
        self.time_window = dict(zip(self.time_window_name, self.time_window_obj))  # filename = [list]
        
    def create_frame_shift(self):
        self.frame_shift_name.append('FrameShift' + str(len(self.frame_shift_obj)))
        self.frame_shift_obj.append(FrameShift())
        self.frame_shift = dict(zip(self.frame_shift_name, self.frame_shift_obj))  # filename = [list]
        
    def create_line(self):
        self.line_name.append('Line' + str(len(self.line_obj)))
        self.line_obj.append(Line())
        self.line = dict(zip(self.line_name, self.line_obj))  # filename = [list]

    def set_data(self, data_type, val):  # e.g. model.set_data(roi[0], [10,10,3,3])
        return data_type.set_data(val)
    
    def get_data(self, filename, data_name):  # e.g. model.get_data('20408A001,tsm, Trace['trace1'])
        return self.data_file[filename].get_data(data_name)
    
    def set_mod(self, control_type, mod_type, val):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    @staticmethod
    def file_type_checker(filename):
        if filename.find('.tsm') > 0:
            return TsmFactory()
        elif filename.find('.da') > 0:
            return DaFactory()
        elif filename.find('.abf') > 0:
            return AbfFactory()
        elif filename.find('.wcp') > 0:
            return WcpFactory()
        else:
            print('---------------------')
            print('Can not find the file')
            print('---------------------')
            return None


class TsmData(DataInterface):
    def __init__(self, model, filename, filepath):
        self.model = model
        self.filename = filename
        self.filepath = filepath
        
        #Read .tsm and .tbn file set.
        self.file_io = 0

        self.frame_obj = []  #data instances
        self.frame_type = []  # 'full_frame', 'ch_frame'
        self.frame = {}  # dictionaly
        
        self.image_obj = []
        self.image_type = []  # 'cell_image', 'dif_image'
        self.image = {}
        
        self.trace_obj = []
        self.trace_type = []  # 'full_trace', 'ch1_trace1', 'elec_trace1', 'bg_trace'
        self.trace = {}

        print('created a data_file.')
        
        self.create_file_io(self.filename, self.filepath)
        
        # create frame data
        self.create_frame_obj(FullFrameFactory(),
                              self.file_io.full_frame,
                              self.file_io.full_frame_interval)
        for i in range(0, self.file_io.num_fluo_ch):
            self.create_frame_obj(ChFrameFactory(), 
                                  self.file_io.ch_frame[:,:,:,i], 
                                  self.file_io.ch_frame_interval)
        
        # create image data
        for i in range(1, self.file_io.num_fluo_ch + 1):
            self.create_image_obj(CellImageFactory(), 
                                  self.frame['ChFrame' + str(i)].frame_data)
        
        # create elec trace
        for i in range(0, self.file_io.num_elec_ch):
            self.create_trace_obj(ElecTraceFactory(), 
                                  self.file_io.elec_trace[:, i], 
                                  self.file_io.elec_interval)
        
        # create fluo trace
        self.create_trace_obj(FullTraceFactory(), 
                              self.frame['FullFrame1'].frame_data, 
                              self.file_io.full_frame_interval)
        self.create_trace_obj(ChTraceFactory(), 
                              self.frame['ChFrame1'].frame_data, 
                              self.file_io.ch_frame_interval)
        self.create_trace_obj(ChTraceFactory(), 
                              self.frame['ChFrame2'].frame_data, 
                              self.file_io.ch_frame_interval)
        
        # Bind image observers to time controller
        self.model.time_window['TimeWindow1'].add_observer(self.image['CellImage1'])
        self.model.time_window['TimeWindow1'].add_observer(self.image['CellImage2'])
        
        # Bind trace observers to time controller
        self.model.roi['Roi1'].add_observer(self.trace['FullTrace1'])
        self.model.roi['Roi1'].add_observer(self.trace['ChTrace1'])
        self.model.roi['Roi1'].add_observer(self.trace['ChTrace2'])
        
    def create_file_io(self, filename, filepath):
        self.file_io = TsmFileIO(filename, filepath)
        
    def create_frame_obj(self, factory_type, data, interval):  #FullFrameFactory, ChFrameFactory
        product = factory_type.create_frame(data, interval)
        object_name = product.__class__.__name__  # str
        num_product = product.num_instance  # int
        
        self.frame_obj.append(product)
        self.frame_type.append(object_name + str(num_product))
        self.frame = dict(zip(self.frame_type, self.frame_obj))
         
    def create_image_obj(self, factory_type, data):
        product = factory_type.create_image(data)
        object_name = product.__class__.__name__  # str
        num_product = product.num_instance  # int
        
        self.image_obj.append(product)
        self.image_type.append(object_name + str(num_product))
        self.image = dict(zip(self.image_type, self.image_obj))
        
    def create_trace_obj(self, factory_type, data, interval):
        product = factory_type.create_trace(data, interval)
        object_name = product.__class__.__name__  # str
        num_product = product.num_instance  # int
        
        self.trace_obj.append(product)
        self.trace_type.append(object_name + str(num_product))
        self.trace = dict(zip(self.trace_type, self.trace_obj))
        
    # the function for searching key word in dict
    def dict_regex(self, dict_name, search_word):
        cp_search_word = re.compile(search_word)
        ret = []
        for k in dict_name:
            if cp_search_word.search(k):
                ret.append(dict_name[k])
        return ret
    
    def get_data(self, data_name):
        # Should chage this code. 
        if data_name.find('Frame') > 0:
            obj = self.frame.get(data_name)
        elif data_name.find('Image') > 0:
            obj = self.image.get(data_name) 
        elif data_name.find('Trace') > 0:
            obj = self.trace.get(data_name) 
        
        if obj is None:
            print('---------')
            print('No object')
            print('---------')
        else:
            return obj
   
    def print_fileinfor(self):
        self.file_io.print_fileinfor()
        print('Object List')
        pprint.pprint('file_io = ' + str(self.file_io))
        pprint.pprint(self.frame)
        pprint.pprint(self.image)
        pprint.pprint(self.trace)
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    filename = '20408A001.tsm'
    filepath = '..\\220408\\'
    model = Model()
    model.create_data_objects(filename, filepath)
    model.data_file[filename].print_fileinfor()
    
    model.data_file[filename].frame['ChFrame1'].show_frame(6)

    model.time_window['TimeWindow1'].set_data([2,2,2,2])
    image = plt.figure()
    model.data_file[filename].image['CellImage1'].show_image()
    electrace = plt.figure()
    model.data_file[filename].trace['ElecTrace1'].plot_trace()
    fluotrace = plt.figure()
    model.data_file[filename].trace['FullTrace1'].plot_trace()
    #model.set_data(model.roi['Roi1'],[10,10,40,40])
    model.roi['Roi1'].set_data([10,10,2,3])
    model.data_file[filename].trace['ChTrace1'].plot_trace()
    
    #elc1 = model.get_data(filename, 'ElecTrace1')
    
    

    print('オブジェクト指向での例外処理で変数をクリアして抜ける')
    print('オブザーバーのリストを辞書にしてキーで消せるようにする')
    print('新しいdata_fileでFullFrame3からになる。これは名前用のカウントがFullFrame classで共通にカウントされるからである。')
    print('単体テストができるようにする')
    


    
    

