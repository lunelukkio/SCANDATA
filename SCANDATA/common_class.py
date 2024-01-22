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

    def set_key(self, controller_key, data_key=None):
        controller_key.upper()
        if data_key is None:
            print(f"Controller key: {controller_key} -> ", end="")
            if controller_key in list(self._dict.keys()):
                del self._dict[controller_key]
                print("Deleted")
            elif controller_key not in list(self._dict.keys()):
                self._dict[controller_key] = None
                print("Added")
        elif data_key is not None:
            data_key = data_key.upper()
            print(f"Data key in {controller_key}: {data_key} -> ", end="")
            if data_key in self._dict[controller_key]:
                self._dict[controller_key].remove(data_key)
                print("Deleted")
            elif data_key not in self._dict[controller_key]:
                self._dict[controller_key].append(data_key)
                print("Added")
        self.__notify()

    # get keys of controller or data.
    def get_key(self, controller_key=None):
        if controller_key is None:
            return list(self._dict.keys())
        elif controller_key is not None:
            return self._dict[controller_key]
        
    def get_dict(self):
        return self._dict
    
    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def __notify(self):
        for observer in self._observers:
            observer.update(self._dict)

    @property
    def observers(self):
        return self._observers


    
class swith_dict(self):
    def __init__(self):
        self._dict = {}

    def create_switch_from_keys(self, original_key):
        self._dict = copy.deepcopy(original_key)

    def set_key(self, controller_key, data_key=None):
        controller_key.upper()
        if data_key is None:
            print(f"Controller key: {controller_key} -> ", end="")
            if controller_key in list(self._dict.keys()):
                del self._dict[controller_key]
                print("Deleted")
            elif controller_key not in list(self._dict.keys()):
                self._dict[controller_key] = None
                print("Added")
        elif data_key is not None:
            data_key = data_key.upper()
            print(f"Data key in {controller_key}: {data_key} -> ", end="")
            if data_key in self._dict[controller_key]:
                self._dict[controller_key].remove(data_key)
                print("Deleted")
            elif data_key not in self._dict[controller_key]:
                self._dict[controller_key].append(data_key)
                print("Added")
        self.__notify()

    # get keys of controller or data.
    def get_key(self, controller_key=None):
        if controller_key is None:
            return list(self._dict.keys())
        elif controller_key is not None:
            return self._dict[controller_key]
        
    def get_dict(self):
        return self._dict