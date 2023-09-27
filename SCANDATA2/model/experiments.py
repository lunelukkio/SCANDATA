# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:47:25 2023

@author: lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
from SCANDATA2.model.value_object import FramesData, ImageData, TraceData
from SCANDATA2.model.file_io import TsmFileIo

"""
Entity
"""
class Experiments:   # entity
    def __init__(self, filename_obj):
        self.filename_obj = filename_obj
        # create default data set.
        builder_factory = self.__factory_selector(self.filename_obj)
        self.builder = builder_factory.create_builder(self.filename_obj)

        txt_data = self.builder.get_infor()
        frames_dict = self.builder.get_frame()   # {type:frames data}
        image_dict = self.builder.get_image()
        trace_dict = self.builder.get_trace()   # {type:Elec data}
        self.data_dict = {"Txt":txt_data,
                          "Frames":frames_dict,
                          "Image":image_dict,
                          "Trace":trace_dict}

        self.__observer = ExperimentsObserver()
        
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
            
    def get_data(self):
        return self.data_dict

            
    def get_frames_list(self):   # dict_type = txt_data, frame_dict...
        key_list = list(self.frames_dict.keys())
        return key_list
    
    def get_image_list(self):   # dict_type = txt_data, frame_dict...
        key_list = list(self.image_dict.keys())
        return key_list
    
    def get_trace_list(self):   # dict_type = txt_data, frame_dict...
        key_list = list(self.trace_dict.keys())
        return key_list


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


class TsmBuilder(Builder):
    def __init__(self, filename_obj):
        num_ch = 2   # this is for Na+ and Ca2+ recording.
        infor_keys = ["Full_interval",
                     "Ch1_interval",
                     "Ch2_interval",
                     "Elec1_interval",
                     "Elec2_interval",
                     "Elec3_interval",
                     "Elec4_interval",
                     "Elec5_interval",
                     "Elec6_interval",
                     "Elec7_interval",
                     "Elec8_interval"]
        file_io = TsmFileIo(filename_obj, num_ch)
        
        # get and set data from files
        data_infor = file_io.get_infor()   # get interval infor from the io
        self.data_infor_dict = dict(zip(infor_keys, data_infor))   # make an interval dict
        self.frames = file_io.get_3d()
        self.elec_data = file_io.get_1d()
        
        file_io.print_data_infor()
        
        del file_io   # release the io object to allow file changes during recording.
        
    def get_infor(self):
        return self.data_infor_dict
        
    def get_frame(self):
        return {"Full": FramesData(self.frames[0], 
                                   self.data_infor_dict["Full_interval"]),   # change to numpy to value obj
                "Ch1": FramesData(self.frames[1], 
                                  self.data_infor_dict["Ch1_interval"]),    # change to numpy to value obj
                "Ch2": FramesData(self.frames[2], 
                                  self.data_infor_dict["Ch2_interval"])}   # change to numpy to value obj

    def get_image(self):
        print("There is no image data")
        return None
    
    def get_trace(self):       
        return {"Elec_ch1": TraceData(self.elec_data[0], 
                                      self.data_infor_dict["Elec1_interval"]), 
                "Elec_ch2": TraceData(self.elec_data[1], 
                                      self.data_infor_dict["Elec2_interval"]), 
                "Elec_ch3": TraceData(self.elec_data[2], 
                                      self.data_infor_dict["Elec3_interval"]),
                "Elec_ch4": TraceData(self.elec_data[3], 
                                      self.data_infor_dict["Elec4_interval"]),
                "Elec_ch5": TraceData(self.elec_data[4], 
                                      self.data_infor_dict["Elec5_interval"]),
                "Elec_ch6": TraceData(self.elec_data[5], 
                                      self.data_infor_dict["Elec6_interval"]),
                "Elec_ch7": TraceData(self.elec_data[6], 
                                      self.data_infor_dict["Elec7_interval"]),
                "Elec_ch8": TraceData(self.elec_data[7], 
                                      self.data_infor_dict["Elec8_interval"])}
    