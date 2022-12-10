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
    def get_data(self):
        pass


"""
Concrete class
"""
class Model(ModelInterface):
    def __init__(self):
        # experiments data
        self.filename = []
        self.filepath = []
        self.data_file = {}  # dictionary for data_files

        # data controllers for any files
        self.roi = {}
        self.time_window = {}
        self.frame_shift = {}
        self.line = {}

        print('Created an empty model.')
        
        self.create_control_objects()
          
    def create_data_objects(self, filename, filepath):
        factory_type = self.file_type_checker(filename)  # check extension (.tsm)
        self.filename.append(filename)
        self.filepath.append(filepath)
        new_data_file_obj = factory_type.create_data_factory(self, filename, filepath)
        self.data_file[filename] = new_data_file_obj  # dict of data_file(key filename : object)

    def create_control_objects(self):
        self.create_roi()
        self.create_time_window()
        self.create_frame_shift()
        self.create_line()

    def create_roi(self):
        new_roi = Roi()
        self.roi['ROI' + str(new_roi.num_instance)] = new_roi  # new_roi.num_instance : Roi class instance

        
    def create_time_window(self):
        new_time_window = TimeWindow()
        self.time_window['TimeWindow' + str(new_time_window.num_instance)] = new_time_window

        
    def create_frame_shift(self):
        new_frame_shift = FrameShift()
        self.frame_shift['FrameShift' + str(new_frame_shift.num_instance)] = new_frame_shift

        
    def create_line(self):
        new_line = Line()
        self.line['Line' + str(new_line.num_instance)] = new_line
        
    def bind_data_controller(self, filename, data_type, controller_name):  # obj_type: 'ChTrace1, CellImage1, controller_type: ROI1, TimeWindow1 
        pass
        #self.data_file[filename].bind_data_controller(data_type, controller_type)

    def set_data(self, data_key, val):  # e.g. model.set_data('ROI1', [10,10,3,3])
        return self.roi[data_key].set_data(val)
    
    def get_data(self, data_key, filename = None):  # e.g. model.get_data('20408A001,tsm, Trace['trace1'])
        return self.data_file[filename].get_data(data_key)
    
        
        
    def set_mod(self, control_type, mod_type, val):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    @staticmethod
    def file_type_checker(filename):
        if filename.find('.tsm') > 0:
            print('Found a .tsm file')
            return TsmFactory()
        elif filename.find('.da') > 0:
            print('Found a .da file')
            return DaFactory()
        elif filename.find('.abf') > 0:
            print('Found an .abf file')
            return AbfFactory()
        elif filename.find('.wcp') > 0:
            print('Found a .wcp file')
            return WcpFactory()
        else:
            print('---------------------')
            print('Can not find the file')
            print('---------------------')
            return None
        
    def check_data_key(self, data_key):  # dict key checker
        if data_key.find('Frame') > 0:
            return 'Frame'
        elif data_key.find('Image') > 0:
            return 'Image' 
        elif data_key.find('Trace') > 0:
            return 'Trace'
        elif data_key.find('ROI') > 0:
            return 'ROI'
        elif data_key.find('TimeWindow') > 0:
            return 'TimeWindow'
        elif data_key.find('FrameShift') > 0:
            return 'FrameShift'
        elif data_key.find('Line') > 0:
            return 'Line'
        else:
            print('-----------------------')
            print('No Key')
            print('-----------------------')
            return None

class TsmData(DataInterface):
    def __init__(self, model, filename, filepath):
        self.model = model
        self.filename = filename
        self.filepath = filepath
        
        # counter for frame, image and trace instance
        self.counter = {}
        
        #Read .tsm and .tbn file set.
        self.file_io = 0

        # object dictionaly
        self.frame = {}
        self.image = {}
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
        self.model.roi['ROI1'].add_observer(self.trace['FullTrace1'])
        self.model.roi['ROI1'].add_observer(self.trace['ChTrace1'])
        self.model.roi['ROI1'].add_observer(self.trace['ChTrace2'])
        
        # set default val
        model.time_window['TimeWindow1'].set_data([2,2,2,2])
        model.roi['ROI1'].set_data([40,40,1,1])
        
    def create_file_io(self, filename, filepath):
        self.file_io = TsmFileIO(filename, filepath)
        
    def create_frame_obj(self, factory_type, data, interval):  #FullFrameFactory, ChFrameFactory
        product = factory_type.create_frame(data, interval)
        object_name = product.__class__.__name__  # str
        
        last_num = self.counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.counter[object_name] = new_num  # Sdd key and num to counter dict.
        self.frame[object_name + str(product.num)] = product

         
    def create_image_obj(self, factory_type, data):
        product = factory_type.create_image(data)
        object_name = product.__class__.__name__  # str

        last_num = self.counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.counter[object_name] = new_num  # Sdd key and num to counter dict.
        self.image[object_name + str(product.num)] = product        

        
    def create_trace_obj(self, factory_type, data, interval):
        product = factory_type.create_trace(data, interval)
        object_name = product.__class__.__name__  # str
        
        last_num = self.counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.counter[object_name] = new_num  # Sdd key and num to counter dict.
        self.trace[object_name + str(product.num)] = product 
        
    # the function for searching key word in dict
    def dict_regex(self, dict_name, search_word):
        cp_search_word = re.compile(search_word)
        ret = []
        for k in dict_name:
            if cp_search_word.search(k):
                ret.append(dict_name[k])
        return ret
    
    """ Not object oriented. Need refactoring"""
    def bind_data_controller(self, data_type, controller_name):  # obj_type: 'ChTrace1, CellImage1, controller_type: ROI1, TimeWindow1 
        if controller_name.find('ROI') > 0:
            self.model.roi[controller_name].add_observer(self.trace[data_type])
        elif controller_name.find('TimeWindow') > 0:
            self.model.time_window[controller_name].add_observer(self.image[data_type])
        elif controller_name.find('FrameShift') > 0:
            self.model.frame_shift[controller_name].add_observer(self.frame[data_type])
        elif controller_name.find('Line') > 0:
            pass
        
    """ Not object oriented. Need refactoring"""
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
    model.roi['ROI1'].set_data([10,10,2,3])
    model.data_file[filename].trace['ChTrace1'].plot_trace()
    
    #elc1 = model.get_data(filename, 'ElecTrace1')
    
    

    print('オブジェクト指向での例外処理で変数をクリアして抜ける')
    print('オブザーバーのリストを辞書にしてキーで消せるようにする')
    print('新しいdata_fileでFullFrame3からになる。これは名前用のカウントがFullFrame classで共通にカウントされるからである。')
    print('単体テストができるようにする')
    


    
    

