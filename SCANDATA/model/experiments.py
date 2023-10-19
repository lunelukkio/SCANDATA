# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:47:25 2023

@author: lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import FramesData, ImageData, TraceData
from SCANDATA.model.file_io import TsmFileIo

"""
Entity
"""
class Experiments:   # entity
    def __init__(self, filename_obj):
        self.filename_obj = filename_obj
        # create default data set.
        builder_factory = self.__factory_selector(self.filename_obj)
        self.builder = builder_factory.create_builder(self.filename_obj)

        self.__txt_data = self.builder.get_infor()
        self.__frames_dict = self.builder.get_frame()  # {key:FramsData -> val_obj}
        self.__image_dict = self.builder.get_image()   # {key:ImageData -> val_obj}
        self.__trace_dict = self.builder.get_trace()  # {key:Trace_Data -> val_obj}

        self.__observer = ExperimentsObserver()
        
        print("----- Experiments: Successful data construction!!!")
        print("")
        
    def __del__(self):  #make a message when this object is deleted.
        #print('.')
        print(f"----- Deleted a Expriments: {self.filename_obj.name}"  
              + "  myId={}".format(id(self)))
        #pass
    
    def __factory_selector(self, filename_obj):
        if filename_obj.extension == ".tsm":
            return TsmBuilderFactory()
        elif filename_obj.extension == ".da":
            raise NotImplementedError()
        else:
            raise Exception("This file is an undefineded file!!!")
            
    def get_default(self):
        return self.builder.default()
            
    def print_infor(self):
        print("Experiments information")
        print(f"Data Time interval = {self.__txt_data}")
        
        if self.__frames_dict is None:
            frames_key = "None"
        else:
            frames_key = list(self.__frames_dict.keys())
        if self.__image_dict is None:
            image_key = "None"
        else:
            image_key = list(self.__image_dict.keys())
        if self.__trace_dict is None:
            trace_key = "None"
        else:
            trace_key = list(self.__trace_dict.keys())
        print(f"frames data = {frames_key}")
        print(f"image data = {image_key}")
        print(f"trace data = {trace_key}")

    @property
    def txt_data(self):
        return self.__txt_data

    @property
    def frames_dict(self):
        return self.__frames_dict
    
    @property
    def image_dict(self):
        return self.__image_dict
    
    @property
    def trace_dict(self):
        return self.__trace_dict
    


# need refactoring(2023/09/13)
class ExperimentsObserver:
    def __init__(self):
        self.__observers = []
        
    def add_observer(self, observer):
        for check_observer in self.__observers:
            if check_observer == observer:
                self.remove_observer(observer)
                return
        self.__observers.append(observer)
        self.__observers = sorted(self.__observers, key=lambda x: str(x.sort_num)+x.name)

    def remove_observer(self, observer):
        self.__observers.remove(observer)
        name_list = []
        for i in self.__observers:
            name_list.append(i.name)
            
    def notify_observer(self, controller_obj):
        name_list = []
        for observer in self.__observers:
            name_list.append(observer.name)
        print('----- Notify to observers: ' + str(name_list))
        """ The order of ViewDatas should be after Data entiries """
        for observer_name in self.__observers:
            observer_name.update(controller_obj.data)
            
    def get_infor(self):
        name_list = []
        for observer in self.__observers:
            name_list.append(observer.name)
        return name_list

    @property
    def observers(self) -> list:
        return self.__observers


    
"""
Builder
"""
class BuilderFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_builder(self, filename_obj):
        raise NotImplementedError()


class TsmBuilderFactory(BuilderFactory):
    def create_builder(self, filename_obj):
        return TsmBuilder(filename_obj)


class Builder(metaclass=ABCMeta):
    @abstractmethod
    def get_infor(self, filename_obj):
        raise NotImplementedError()    

    @abstractmethod
    def get_frame(self, filename_obj):
        raise NotImplementedError()
        
    @abstractmethod
    def get_image(self, filename_obj):
        raise NotImplementedError()
        
    @abstractmethod
    def get_trace(self, filename_obj):
        raise NotImplementedError()
        
    @abstractmethod
    def default(self, filename_obj):
        raise NotImplementedError()   
        

# This class define the names of controllers and data
class TsmBuilder(Builder):
    def __init__(self, filename_obj):
        self.num_ch = 2   # this is for Na+ and Ca2+ recording.
        self.num_elec_ch = 8
        self.default_controller = ["ROI", "ROI", "IMAGE_CONTROLLER", "TRACE_CONTROLLER"] 
        self.default_data = ["FULL"]
        for num in range(self.num_ch):
            self.default_data.append("CH" + str(num+1))
        for num in range(self.num_elec_ch):
            self.default_data.append("ELEC" + str(num+1))  # see self.get_trace

        
        infor_keys = ["FULL_INTERVAL"]
        for idx in range(self.num_ch):
            infor_keys.append(f"CH{idx + 1}_INTERVAL")
        for idx in range(self.num_elec_ch):
           infor_keys.append(f"ELEC{idx + 1}_INTERVAL")

        file_io = TsmFileIo(filename_obj, self.num_ch)
        
        # get and set data from files
        data_infor = file_io.get_infor()   # get interval infor from the io
        self.data_infor_dict = dict(zip(infor_keys, data_infor))   # make an interval dict
        self.frames = file_io.get_3d()
        self.elec_data = file_io.get_1d()
        
        #file_io.print_data_infor()
        
        del file_io   # release the io object to allow file changes during recording.
        print("----- TsmBulder: The .tsm file was imported and the file_io object was deleted.")
        print("")
        
    def get_infor(self):
        return self.data_infor_dict
        
    # make data_dict {data_key: FrameData}  {"FULL": data, "CH1": data ......}
    def get_frame(self) -> dict:  # change to numpy to value obj
        data = {"FULL": FramesData(self.frames[0], 
                                   self.data_infor_dict["FULL_INTERVAL"])}
        for idx in range(self.num_ch):
            data[f"CH{idx + 1}"] = FramesData(self.frames[idx + 1], 
                                   self.data_infor_dict[f"CH{idx + 1}_INTERVAL"])    # change to numpy to value obj
        return data

    def get_image(self):
        print("----- There is no image data")
        return None
    
    # make data_dict {data_key: TraceData}  {"ELEC1": data, ""ELEC2": data ......}
    def get_trace(self):
        data = {}
        for idx in range(self.num_elec_ch):
            data[f"ELEC{idx + 1}"] = TraceData(self.elec_data[idx], 
                                          self.data_infor_dict[f"ELEC{idx + 1}_INTERVAL"])    # change to numpy to value obj
        return data
    
    def default(self):
        return self.default_controller, self.default_data
