# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022
concrete classes for model controllers
lunelukkio@gmail.com
"""
from abc import ABCMeta, abstractmethod
from SCANDATA.model.value_object import RoiVal, FrameWindowVal, TimeWindowVal
from SCANDATA.model.builder import TsmFileBuilder, AbfFileBuilder, WcpFileBuilder, KeyCounter

"""
abstract factory
"""
class ModelControllerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_controller(self, val):
        raise NotImplementedError()


"""
contrete factory
"""
class RoiFactory(ModelControllerFactory):
    def create_controller(self):
        return Roi()
        
class FrameWindowFactory(ModelControllerFactory):
    def create_controller(self):
        return FrameWindow()
    
class FrameShiftFactory(ModelControllerFactory):
    def create_controller(self):
        return FrameShift()
        
class LineFactory(ModelControllerFactory):
    def create_controller(self):
        return Line()
        
class ElecControllerFactory(ModelControllerFactory):
    def create_controller(self):
        return ElecController() 
    


"""
abstract product
"""
class ModelController(metaclass=ABCMeta):
    @abstractmethod
    def set_data(self):
        raise NotImplementedError()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
        
    @abstractmethod
    def get_infor(self):
        raise NotImplementedError()

    @abstractmethod
    def print_infor(self):
        raise NotImplementedError()
    
    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def add_observer(self, observer):
        raise NotImplementedError()

    @abstractmethod
    def notify_observer(self):
        raise NotImplementedError()


"""
concrete product
"""
class Roi(ModelController):
    def __init__(self):
        self.__roi_obj = RoiVal(40, 40, 2, 2)
        self.object_num = 0  # instance number
        self.__data_counter = {}  # counter dict
        self.__data_dict = {}  # data dict
        self.__observer = ControllerObserver()
        self.__builder = TsmFileBuilder()
        #print('Created ROI-{}.'.format(self.object_num))
        
    def __del__(self):
        #print('.')
        print('----- Deleted a Roi object.' + '  myId={}'.format(id(self)))
        #pass
        
    def check_val(self, x, y, x_width, y_width) -> None:
        # check the val as the same or not
        if x == self.__roi_obj.data[0] and \
           y == self.__roi_obj.data[1] and \
           x_width == self.__roi_obj.data[2] and \
           y_width == self.__roi_obj.data[3]:
               print('----- The new ROI value is the same as previous.')
               return False
        # check the val for limit
        else:
            if x < 0 or \
               y < 0 or \
               x_width < 1 or \
               y_width < 1:
                print('ROI value shold be more than 1')
                return False
            else:
                return True

    def set_data(self, x = None, y = None, x_width = None, y_width = None) -> None:
        if x is None:
            x = self.__roi_obj.data[0]
        if y is None:
            y = self.__roi_obj.data[1]
        if x_width is None:
            x_width = self.__roi_obj.data[2]
        if y_width is None:
            y_width = self.__roi_obj.data[3]
        check_bool = self.check_val(x, y, x_width, y_width)
        # make a new value object
        if check_bool is True:
            self.__roi_obj = RoiVal(x, y, x_width, y_width)  # replace the roi
            self.print_infor()
            self.notify_observer()
        elif check_bool is False:
            pass

    def add_data(self, x: int, y: int, x_width=0, y_width=0) -> None:
        check_bool = self.check_val(self.__roi_obj.data[0] + x,
                                    self.__roi_obj.data[1] + y,
                                    self.__roi_obj.data[2] + x_width,
                                    self.__roi_obj.data[3] + y_width)
        if check_bool is True:
            add_roi_obj = RoiVal(x, y, x_width, y_width)  # make new additional RoiVal
            self.__roi_obj += add_roi_obj  # override of + in type:RoiVal
            self.print_infor()
            self.notify_observer()
        elif check_bool is False:
            pass

    def get_data(self) -> object:
        return self.__roi_obj
    
    def reset(self) -> None:
        self.__roi_obj = RoiVal(40, 40, 2, 2)
        self.print_infor()
        self.notify_observer()
        print('----- Reset ROI{} and notified'.format(self.object_num))

    def add_observer(self, observer):
        self.__observer.add_observer(observer)
        #self.notify_observer()  # this message come from a controller
        print(self.get_infor())
            
    def notify_observer(self):
        self.__observer.notify_observer(self.__roi_obj)

    @property
    def observers(self) -> list:
        return self.__observer.observers
    
    def get_infor(self):  # get names from observers
        name_list = self.__observer.get_infor()
        return name_list
    
    def print_infor(self) -> None:
        name_list = []
        num = len(self.__observer.observers)
        for i in range(num):
            name_list.append(self.__observer.observers[i].name)
        print(f'Roi{self.object_num} observer list = {str(name_list)}, ROI = {self.get_data().data}')


class FrameWindow(ModelController):
    def __init__(self):
        self.__frame_window_obj = FrameWindowVal(0, 0, 1, 1)
        self.__observer = ControllerObserver()
        self.object_num = 0
        #print('Create FrameWindow{}.'.format(self.object_num))

    def set_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        # check data
        print('Tip: Didnt test this check program.')
        if start == self.__frame_window_obj.data[0] and \
           end == self.__frame_window_obj.data[1] and \
           start_width == self.__frame_window_obj.data[2] and \
           end_width == self.__frame_window_obj.data[3]:
               print('----- The new FrameWindow value is the same as previous.')
               return
        self.__frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.print_infor()
        self.notify_observer()
        #print('Set FrameWindow-{} and notified'.format(self.object_num))

        
    def add_data(self, start: int, end: int, start_width=0, end_width=0) -> None:
        add_frame_window_obj = FrameWindowVal(start, end, start_width, end_width)
        self.__frame_window_obj += add_frame_window_obj
        self.print_infor()
        self.notify_observer()
        #print('Add to FrameWindow{} and notified'.format(self.object_num))

    def get_data(self) -> object:
        return self.__frame_window_obj
    
    def reset(self) -> None:
        self.__frame_window_obj = FrameWindowVal(0, 0, 0, 0)
        self.print_infor()
        self.notify_observer()
        #print('Reset FrameWindow{} and notified'.format(self.object_num))

    def add_observer(self, observer: object) -> None:
        self.__observer.add_observer(observer)
        #self.notify_observer()  # this message come from a controller
    
    def notify_observer(self) -> None:
        self.__observer.notify_observer(self.__frame_window_obj)
            
    @property
    def observers(self) -> list:
        return self.__observer.observers
    
    def get_infor(self):  # get names from observers
        name_list = self.__observer.get_infor()
        return name_list

    def print_infor(self) -> None:
        name_list = []
        num = len(self.__observer.observers)
        for i in range(num):
            name_list.append(self.__observer.observers[i].name)
        print(f'FrameWindow{self.object_num} observer list = {str(name_list)}, ROI = {self.get_data().data}')


class FrameShift(ModelController): 
    def __init__(self):
        self.__observers = []
    
    def set_data(self, val):
        pass

    def get_data(self):
        pass

    def print_infor(self):
        pass

    def reset(self):
        pass

    def add_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass
    
    @property
    def observers(self) -> list:
        return self.__observers
    
    def get_infor(self):
        name_list = []
        for i in range(len(self.__observers)):
            name_list.append(self.__observers[i].name)
        return name_list


class Line(ModelController): 
    def __init__(self):
        self.__observers = []
    
    def set_data(self, val):
        pass

    def get_data(self):
        pass

    def print_infor(self):
        pass

    def reset(self):
        pass

    def add_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass

    def notify_observer(self):
        pass
    
    @property
    def observers(self) -> list:
        return self.__observers
    
    def get_infor(self):
        name_list = []
        for i in range(len(self.__observers)):
            name_list.append(self.__observers[i].name)
        return name_list
    
    
class ElecController(ModelController):
    def __init__(self):
        self.__time_window_obj = TimeWindowVal(0, 100)
        self.__observer = ControllerObserver()
        self.object_num = 0
        #print('Create TimeController{}.'.format(self.object_num))

    def set_data(self, start: int, end: int) -> None:
        self.__time_window_obj = TimeWindowVal(start, end)
        self.print_infor()
        self.notify_observer()
        #print('Set TimeWindow{} and notified'.format(self.object_num))

    def add_data(self, start: int, end: int) -> None:
        add_time_window_obj = TimeWindowVal(start, end)
        self.__time_window_obj += add_time_window_obj
        self.print_infor()
        self.notify_observer()
        #print('Add to TimeWindow{} and notified'.format(self.object_num))

    def get_data(self) -> object:
        return self.__time_window_obj
    
    def reset(self) -> None:
        self.__time_window_obj = FrameWindowVal(0, 100)
        self.print_infor()
        self.notify_observer()
        #print('Reset FrameWindow{} and notified'.format(self.object_num))
    
    def add_observer(self, observer: object) -> None:
        self.__observer.add_observer(observer)
        #self.notify_observer()  # this message come from a controller
    
    def notify_observer(self) -> None:
        self.__observer.notify_observer(self.__time_window_obj)
            
    @property
    def observers(self) -> list:
        return self.__observer.observers
    
    def get_infor(self):  # get names from observers
        name_list = self.__observer.get_infor()
        return name_list

    def print_infor(self) -> None:
        name_list = []
        num = len(self.__observer.observers)
        for i in range(num):
            name_list.append(self.__observer.observers[i].name)
        print(f'ElecController{self.object_num} observer list = {str(name_list)}, ROI = {self.get_data().data}')
        
class ControllerObserver:
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