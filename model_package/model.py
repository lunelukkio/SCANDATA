# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022

lunelukkio@gmail.com
This is the main module for a model called by a controller
"""

from abc import ABCMeta, abstractmethod
import re  # call regular expression
from model_package.roi import Roi, TimeWindow, FrameShift, Line
from model_package.data_factory import TsmIOFactory, DaIOFactory
from model_package.data_factory import FullFrame


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


class DataFileInterface():
    @abstractmethod
    def create_file_io(self):
        pass
    
    @abstractmethod
    def create_frame_data(self):
        pass
    
    @abstractmethod
    def create_image_data(self):
        pass
    
    @abstractmethod
    def create_trace_data(self):
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
        self.create_data_file()
            
    def create_control_objects(self):
        self.create_roi()
        self.create_time_window()
        self.create_frame_shift()
        self.create_line()

    def create_data_file(self, filename, filepath):
        self.filename.append(filename)
        self.filepath.append(filepath)
        self.data_file_obj.append(file_io(filename, filepath))
        self.data_file = dict(zip(self.filename, self.data_file_obj))
        
        

    def create_roi(self):
        self.roi_name.append('ROI' + str(len(self.roi_obj)))
        self.roi_obj.append(Roi())
        self.roi = dict(zip(self.roi_name, self.roi_obj))  # filename = [list]
        
    def create_time_window(self):
        self.time_window_name.append('time_window' + str(len(self.time_window_obj)))
        self.time_window_obj.append(TimeWindow())
        self.time_window = dict(zip(self.time_window_name, self.time_window_obj))  # filename = [list]
        
    def create_frame_shift(self):
        self.frame_shift_name.append('frame_shift' + str(len(self.frame_shift_obj)))
        self.frame_shift_obj.append(FrameShift())
        self.frame_shift = dict(zip(self.frame_shift_name, self.frame_shift_obj))  # filename = [list]
        
    def create_line(self):
        self.line_name.append('line' + str(len(self.line_obj)))
        self.line_obj.append(Line())
        self.line = dict(zip(self.line_name, self.line_obj))  # filename = [list]

    def set_data(self, control_type, val):
        raise NotImplementedError
    
    def get_object(self, data_file):
        pass
    
    def set_mod(self, control_type, mod_type, val):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    @staticmethod
    def file_type_checker(filename):
        if filename.find('.tsm') > 0:
            return TsmIOFactory()
        elif filename.find('.da') > 0:
            return DaIOFactory()
        else:
            print('---------------------')
            print('Can not find the file')
            print('---------------------')
            return None


class TsmFile(DataFileInterface):
    def __init__(self, filename, filepath, factory_type):
        self.filename = filename
        self.filepath = filepath
        self.factory_type = factory_type
        self.file_io = factory_type.create_file_io(self.filename, self.filepath)
        
        # Main data objects

        self.frame_obj = []  #data instances
        self.frame_type = []  # 'full_frame', 'ch_frame'
        self.frame_data = {}  # dictionaly, 
        
        self.image_obj = []
        self.image_type = []  # 'cell_image', 'dif_image'
        self.image_data = {}
        
        self.trace_obj = []
        self.trace_type = []  # 'full_trace', 'ch1_trace1', 'elec_trace1', 'bg_trace'
        self.trace_data = {}

        print('created a data_file.')
        
    def create_file_io(self):
        factory_type = self.file_type_checker(filename)
        
        self.data_file_obj.append(DataFile(filename, filepath, factory_type))
        self.data_file = dict(zip(self.filename, self.data_file_obj))  # filename = [list]

    def create_frame_data(self, factory_type):
        self.frame_data = factroy_type.read_data()
        data_file1 = factory_type.create_file_io(filename, filepath)

    def create_(self, data_type):
        
        
        self.data_3d_obj.append(self.factory_type.create_frame(self.file_io, data_type))
        self.data_3d_type.append(data_type)
        self.data_3d = dict(zip(self.data_3d_type, self.data_3d_obj))
         
    def create_image_data(self, data_3d, data_type):
        self.data_2d.append(Data2D(data_type))
        self.data_2d[len(self.data_2d)-1].create_data()
        
    def create_trace_data(self, data_3d, data_type):
        check_num = len(self.dict_regex(self.data_1d, '^' + data_type))
        print(check_num)
        
        self.data_1d_obj.append(self.factory_type.create_data_1d(data_type))
        self.data_1d_type.append(data_type + str(check_num+1))
        self.data_1d = dict(zip(self.data_1d_type, self.data_1d_obj))
        
    # the function for searching key word in dict
    def dict_regex(self, dict_name, search_word):
        cp_search_word = re.compile(search_word)
        ret = []
        for k in dict_name:
            if cp_search_word.search(k):
                ret.append(dict_name[k])
        return ret
    
    def print_fileinfor(self):
        self.file_io.print_fileinfor()

        
class TsmData(FileType):
    pass

    def create_data_set():
        # create instance of 3D data.
        self.add_data_3d('full_frame')
        self.add_data_3d('ch1_frame')
        self.add_data_3d('ch2_frame')
        
        # create empty instances of elec data.
        for i in range(0, 8):
            self.add_data_1d('elec_trace')
            
        # create empty instancse of trace data.
        for data_type in ['full_trace', 'ch1_trace', 'ch2_trace', 'bg_trace']:
            self.add_data_1d(data_type)



if __name__ == '__main__':

    filename = '20408A001.tsm'
    filepath = '..\\220408\\'
    model = Model()
    model.create_data_file(filename, filepath)
    datafile = model.data_file[filename]

    
    #model.roi['ROI1'].set_data([10,10,40,40])
    

    #model.data_file[filename].data_3d['ch1_frame'].show_frame(1)  

    print('オブジェクト指向での例外処理で変数をクリアして抜ける')


    
    

