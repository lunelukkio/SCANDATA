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
from model.data_factory import TsmFileIO
from model.data_factory import FullFrameFactory, ChFrameFactory
from model.data_factory import CellImageFactory, DifImageFactory
from model.data_factory import ElecTraceFactory, FullTraceFactory, ChTraceFactory

"""
abstract class
"""
class ModelInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_data_set(self, filename, filepath) -> key:
        raise NotImplementedError()

    @abstractmethod
    def create_obj(self, filename, key) -> key:
        raise NotImplementedError()

    @abstractmethod
    def set_data(self, filename, key, val) -> None:  # key = 'ROI1','ChTrace','ModDF','ModAverage'
        raise NotImplementedError()

    @abstractmethod
    def get_data(self, filename, key) -> object:
        raise NotImplementedError() 

    @abstractmethod
    def bind(self, filename_controller, model_controller_key, filename_data, data_key) -> None:
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError()

    def add_mod(self, mod_key, data_key) -> key:
        raise NotImplementedError()

""" Data file factory """
class DataSetFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_data_set_factory(self, model, filename, filepath):
        raise NotImplementedError()


class TsmFactory(DataSetFactory):
    def create_data_set_factory(self, model,filename, filepath):
        return TsmData(model, filename, filepath)


class DaFactory(DataSetFactory):
    def create_data_set_factory(self, model, filename, filepath):
        raise NotImplementedError


class AbfFactory(DataSetFactory):
    def create_data_set_factory(self, model, filename, filepath):
        raise NotImplementedError


class WcpFactory(DataSetFactory):
    def create_data_set_factory(self, model, filename, filepath):
        raise NotImplementedError


""" Data file products"""
class DataSetInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_file_io(self):
        raise NotImplementedError()

    @abstractmethod
    def create_object(self):
        raise NotImplementedError()



    @abstractmethod
    def create_frame_obj(self):
        raise NotImplementedError()

    @abstractmethod
    def create_image_obj(self):
        raise NotImplementedError()

    @abstractmethod
    def create_trace_obj(self):
        raise NotImplementedError()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()


"""
Concrete class
"""
class Model(ModelInterface):
    def __init__(self):
        # experiments data
        self.__filename_list = []
        self.__filepath_list = []
        self.__data_set = {}  # dictionary for data_files
        print('Created an empty model.')

    def create_data_set(self, filename, filepath) -> key:
        factory_type = self.file_type_checker(filename)  # check extension (.tsm)
        self.__filename.append(filename)
        self.__filepath.append(filepath)
        new_data_file_obj = factory_type.create_data_set_factory(self, filename, filepath)
        self.__data_set[filename] = new_data_file_obj  # dict of data_file(key filename : object)
        print(filename)
        return filename

    @abstractmethod
    def create_obj(self, filename, key) -> key:
        key_name = self.__filename[filename].create_obj(key)
        return key_name
        

    
    
    
    @abstractmethod
    def set_data(self, filename, key, val) -> None:  # key = 'ROI1','ChTrace','ModDF','ModAverage'
        raise NotImplementedError()

    @abstractmethod
    def get_data(self, filename, key) -> obj:
        raise NotImplementedError()

    @abstractmethod
    def bind(self, filename_controller, model_controller_key, filename_data, data_key):
        raise NotImplementedError()

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError()

    def add_mod(self, mod_key, data_key) -> key:
        raise NotImplementedError()
    
    
    
    

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

class TsmData(DataSetInterface):
    def __init__(self filename, filepath):
        self.__filename = filename
        self.__filepath = filepath
        self.__key = {}
        
        key = self.check_key()
        
        # controller objects
        self.model_controller = {}
        self.model_controller_counter = {}
        
        # counter for frame, image and trace instance

                self.create_control_objects()
        #Read .tsm and .tbn file set.
        self.file_io = 0


        # object dictionaly
        self.frame = {}
        self.image = {}
        self.trace = {}
        self.data_counter = {}

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
        
    def create_object(self, key):
        
        
        
    def create_model_controller(self, factory_type):
        product = factory_type.create_model_controller()
        object_name = product.__class__.__name__  # str
        
        last_num = self.model_controller_counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.mode_controller_counter[object_name] = new_num  # Sdd key and num to counter dict.
        self.model_controller[object_name + str(product.num)] = product
        

        
    def create_frame_obj(self, factory_type, data, interval):  #FullFrameFactory, ChFrameFactory
        product = factory_type.create_frame(data, interval)
        object_name = product.__class__.__name__  # str
        
        last_num = self.data_counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.data_counter[object_name] = new_num  # Sdd key and num to counter dict.
        self.frame[object_name + str(product.num)] = product

         
    def create_image_obj(self, factory_type, data):
        product = factory_type.create_image(data)
        object_name = product.__class__.__name__  # str

        last_num = self.data_counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.data_counter[object_name] = new_num  # Sdd key and num to counter dict.
        self.image[object_name + str(product.num)] = product        

        
    def create_trace_obj(self, factory_type, data, interval):
        product = factory_type.create_trace(data, interval)
        object_name = product.__class__.__name__  # str
        
        last_num = self.data_counter.get(object_name, 0)  # Get counter num of instance.
        new_num = last_num + 1
        product.num = new_num  # Add counter num to instance.
        
        self.data_counter[object_name] = new_num  # Sdd key and num to counter dict.
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
    
    

    print('??????????????????????????????????????????????????????????????????????????????')
    print('?????????????????????????????????????????????????????????????????????????????????')
    print('?????????data_file???FullFrame3??????????????????????????????????????????????????????FullFrame class???????????????????????????????????????????????????')
    print('??????????????????????????????????????????')
    print('Frame ??????????????? Roi TimeWindopw?????????????????????')
    


    
    

