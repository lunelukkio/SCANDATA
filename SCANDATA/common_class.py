# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:42:38 2023

@author: lunelukkio@gmail.com
"""

import os
import glob
import copy
from abc import ABCMeta, abstractmethod

        
"""
Value object
"""
class WholeFilename:  # Use it only in a view and controller
    def __init__(self, fullname: str):
        self.__fullname = os.path.join(fullname)  # replace separater for each OS
        self.__filename = os.path.basename(self.__fullname)
        self.__filepath = os.path.dirname(self.__fullname) + os.sep
        self.__abspath = os.path.abspath(fullname)# absolute path
        split_filename = os.path.splitext(self.__filename)
        self.__file_name_no_ext = split_filename[0]
        self.__extension =  split_filename[1]  # get only extension
        
        self.__filename_list = self.__make_filename_list()
        
    # List need A000-Z999 in the last of filenames
    def __make_filename_list(self) -> list:
        
        find = os.path.join(os.path.dirname(self.__abspath), '*' + str(self.__extension))
        filename_list = [os.path.basename(f) for f in glob.glob(find)]
        return  filename_list
    
    def __del__(self):
        #print('.')
        #print('Deleted a ImageData object.' + '  myId= {}'.format(id(self)))
        pass
        
    @property
    def fullname(self) -> str:
        return self.__fullname
    
    @property
    def name(self) -> str:
        return self.__filename
    
    @property
    def path(self) -> str:
        return self.__filepath
    
    @property
    def abspath(self) -> str:
        return self.__abspath
    
    @property
    def file_name_no_ext(self) -> str:
        return self.__file_name_no_ext
    
    @property
    def extension(self) -> str:
        return self.__extension
    
    @property
    def filename_list(self) -> list:
        return self.__filename_list
    
    def print_infor(self) -> None:
        print('THe absolute path = ' + self.__abspath)
        print('The full path = ' + self.__fullname)
        print('The file name = ' + self.__filename)
        print('The file path = ' + self.__filepath)
        print('The file name without extension = ' + self.__file_name_no_ext)
        print('The file extension = ' + self.__extension)
        print('The file name list in the same folder = ' + str(self.__filename_list))
        
class DataKeySet:  # singleton
    _instance = None  # class valiable

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.__observers = []
        self.__key_dict = {"CONTROLLER": KeyList(), "FILENAME": KeyList(), "CH": KeyList(), "MOD": KeyList()}




class KeyList(list):
    def set_data_key(self, key):   
        key = key.upper()
        if key in self:
            self.remove(key)
            print(f"Deleted data key: [{key}]")
        elif key not in  self:
            self.append(key)
            print(f"Added data key: [{key}]")
    
            
class KeyDict(dict):
    def set_data_key(self, key):   
        key = key.upper()
        if key in self:
            del self[key]
            print(f"Deleted data key: [{key}]")
        elif key not in self:
            self[key] = True
            print(f"Added data key: [{key}]")
            
    def set_val(self, key, val=None):
        if not (isinstance(val, bool) or val is None):   # val is not bool or None.
            raise Exception(f"This is not boolen value: {val}")
        if key not in self:
            raise Exception(f"No key in the dict: {key}")
        if val is not None:
            self[key] = val
        elif val is None:
            self[key] = not self[key]
            
    def update(self, keys):
        # delete a key
        for key in list(self.keys()):  # take own key
            if key not in keys:  # check the new key_list
                del self[key]  # if old is not in the new key list, delete it.
        # add a new key without changing
        for key in keys:
            self.setdefault(key, self.get(key, True))  # True or key value (bool)

    
class DataSwitchSet:  # controller class should have this class
    def __init__(self):
        self.__switch_set = {"CONTROLLER": KeyDict(), "FILENAME": KeyDict(), "CH": KeyDict(), "MOD": KeyDict()}

    def set_val(self, dict_key, key, val=None):
        dict_key = dict_key.upper()
        key = key.upper()
        self.__switch_set[dict_key].set_val(key, val)
            
    def get_val(self, key):
        for dict_key in self.__switch_set:
            if key in self.__switch_set[dict_key].keys():
                return self.__switch_set[dict_key][key]
            else:
                raise Exception("No key in the view data dict")
    
    # No type_key: get every true list.
    def get_true_list(self, dict_key, key_type=None):  # e.g. type_key = "ROI"
        dict_key = dict_key.upper()
        if key_type:
            key_type = key_type.upper()
            true_key = [key for key, value in self.__switch_set[dict_key].items() if value is True]
            return [key for key in true_key if key_type in key]
        else:
            return [key for key, value in self.__switch_set[dict_key].items() if value is True]
                
    def update(self, list_keys):
        for dict_key in self.__switch_set:
            self.__switch_set[dict_key].update(list_keys[dict_key])

    @property
    def switch_set(self):
        return self.__switch_set
    
    
    
    
    
    
    
    
    
    
class SingletonKeyDict:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonKeyDict, cls).__new__(cls)
            cls._instance._dict = {}
            cls._instance._observers = []
        return cls._instance

    def copy_dict(self, original_dict):
        self._dict = copy.deepcopy(original_dict)

    def get_dict(self):
        return self._dict

    def set_data_key(self, list_key, key):   
        list_key = list_key.upper()
        key = key.upper()
        print(f"Data key [{list_key}] -> ", end="")
        self.__key_dict[list_key].set_data_key(key)
        self.__notify()

    def get_controller_key(self):
        return list(self._dict.keys())
    
    def get_ch_key(self, controller_key):
        return list(self._dict[controller_key].keys())
    
    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)

    def __notify(self):
        for observer in self.__observers:
            observer.update(self.__key_dict)
    

        
    def get_key_dict(self):
        return self.__key_dict
        
    @property
    def observers(self):
        return self.__observers
    
    
    
class Entry(metaclass=ABCMeta):
    def __init__(self):
        self.__name = None
        self.__list = []
        self.__switch = True
        
    def set_data_key(self, key):   
        key = key.upper()
        if key in self:
            del self[key]
            print(f"Deleted data key: [{key}]")
        elif key not in self:
            self[key] = True
            print(f"Added data key: [{key}]")
        
    @abstractmethod
    def update(self, keys):
        raise NotImplementedError()


    
    
class DataSwitchDict(Entry):
    # e.g. {CH0: False, CH1: True, CH2: True}  
    def __init__(self):
        self.__name = None
        self.__list = []
        self.__switch = True
        
    def set_data_key(self, key):   
        key = key.upper()
        if key in self:
            del self[key]
            print(f"Deleted data key: [{key}]")
        elif key not in self:
            self[key] = True
            print(f"Added data key: [{key}]")
            
    def set_val(self, key, val=None):
        if not (isinstance(val, bool) or val is None):   # val is not bool or None.
            raise Exception(f"This is not boolen value: {val}")
        if key not in self:
            raise Exception(f"No key in the dict: {key}")
        if val is not None:
            self[key] = val
        elif val is None:
            self[key] = not self[key]
            
    def update(self, keys):
        # delete a key
        for key in list(self.keys()):  # take own key
            if key not in keys:  # check the new key_list
                del self[key]  # if old is not in the new key list, delete it.
        # add a new key without changing
        for key in keys:
            self.setdefault(key, self.get(key, True))  # True or key value (bool)


class KeyDict(dict, Entry):
    # self = dict
    def set_data_key(self, key):   
        key = key.upper()
        if key in self:
            del self[key]
            print(f"Deleted data key: [{key}]")
        elif key not in self:
            self[key] = True
            print(f"Added data key: [{key}]")
            
    def update(self, keys):
        # delete a key
        for key in list(self.keys()):  # take own key
            if key not in keys:  # check the new key_list
                del self[key]  # if old is not in the new key list, delete it.
        # add a new key without changing
        for key in keys:
            self.setdefault(key, self.get(key, True))  # True or key value (bool)
            
    def add(self, entry):
        entry.path = self.name
        #self[] = entry