# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:42:38 2023

@author: lunelukkio@gmail.com
"""

import os
import glob
import copy
  
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
            cls._instance._filename_list = []
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
            else:
                self._dict[controller_key] = None
                print("Added")
        else:
            data_key = data_key.upper()
            if controller_key not in self._dict:
                self._dict[controller_key] = []
            print(f"Data key in {controller_key}: {data_key} -> ", end="")
            if data_key in self._dict[controller_key]:
                self._dict[controller_key].remove(data_key)
                print("SingletonKeyDict: Deleted")
            else:
                self._dict[controller_key].append(data_key)
                print("SingletonKeyDict: Added")
        self._notify()

    # get keys of controller or data.
    def get_key(self, controller_key=None):
        if controller_key is None:
            return list(self._dict.keys())
        else:
            return self._dict[controller_key]
        
    def get_dict(self):
        return self._dict
    
    def set_filename(self, filename_key):
        if filename_key in self._filename_list:
            self._filename_list.remove(filename_key)
            print(f"SingletonKeyDict: Removed {filename_key} from the filename list")
        else:
            self._filename_list.append(filename_key)
            print(f"SingletonKeyDict: Added {filename_key} from the filename list")
        print("")
        self._notify()
            
    def get_filename_list(self):
        return self._filename_list
    
    def set_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
            #print(f"Removed {observer} from the ovserver list")
        else:
            self._observers.append(observer)
            #print(f"Added {observer} from the observer list")    
            # update the new observer
            observer.update(self._dict)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._dict)
            observer.update_filename(self._filename_list)

    @property
    def observers(self):
        return self._observers
    
    @property
    def filename_list(self):
        return self._filename_list
    
    def print_infor(self):
        print("Singleton key dict ---------->")
        print(f"Data keys: {self._dict}")
        print(f"Filename keys: {self._filename_list}")
        print(f"Observers: {self._observers}")
        print("----------> End")


class FlagDict:
    def __init__(self):
        self.__data_dict = {}
        self.__filename_dict = {}

    def update(self, key_dict):
        old_dict = self.__data_dict
        new_dict = {}
        # make a new dict from the key list
        for controller_key, data_list in key_dict.items():
            if data_list is not None: 
                new_dict[controller_key] = {data_key: old_dict[controller_key][data_key] 
                                            if data_key in old_dict 
                                            else True for data_key in data_list}
            else:
                new_dict[controller_key] = None
        self.__data_dict = new_dict

    def set_val(self, controller_key, data_key, val):  # "ALL" in controller and data key is acceptable.
        if controller_key == "ALL":
            for controller_key in self.__data_dict.keys():
                self.__set_val(controller_key, data_key, val)
        else:
            self.__set_val(controller_key, data_key, val)
        
    def __set_val(self, controller_key, data_key, val=None):  # "ALL" in data_key is acceptable.
        if controller_key not in self.__data_dict:
            print(f"Controller key: {controller_key} doesn't exist.")
        else:
            if data_key == "ALL":
                for data_key in self.__data_dict[controller_key].keys():
                    self.__data_dict[controller_key][data_key] = val
            elif data_key not in self.__data_dict[controller_key]:
                print(f"Data key: {data_key} doesn't exist in {controller_key}")
                return
            else:
                if val is None:
                    self.__data_dict[controller_key][data_key] = not self.__data_dict[controller_key][data_key]
                else:
                    self.__data_dict[controller_key][data_key] = val
                    
    def update_filename(self, filename_list):
        old_dict = self.__filename_dict
        new_dict = {}
        copy_list = copy.deepcopy(filename_list)
        # make a new dict from the keylist
        for filename_key in copy_list:
            if filename_key in old_dict:
                new_dict[filename_key] = old_dict[filename_key]
            else:
                new_dict[filename_key] = True
        self.__filename_dict = new_dict
        
    def set_filename_val(self, filename_key, val=None):
        if filename_key not in self.__filename_dict:
            print(f"Filename key: {filename_key} doesn't exist.")
        else:
            if val is None:
                self.__filename_dict[filename_key] = not self.__filename_dict[filename_key]
            else:
                self.__filename_dict[filename_key] = val
        
    def get_dict(self):
        return self.__data_dict
    
    def get_filename_dict(self):
        return self.__filename_dict
    
    # find only controller keys which have true in ch data.
    def find_true_controller_keys(self) -> list:
        return [key for key, value in self.__data_dict.items() if any(value.values())]
    
    def find_true_ch_keys(self, controller_key) -> list:
        return [key for key, value in self.__data_dict[controller_key].items() if value]
    
    def find_true_filename_keys(self) -> list:
        return [filename_key 
                for filename_key, bool_val 
                in self.__filename_dict.items() 
                if bool_val]
    
    def print_infor(self):
        print(f"Data Flags: {self.__data_dict}")
        print(f"Filename flags: {self.__filename_dict}")
        print("")

    @staticmethod
    def data_dict_to_key_dict(data_dict) -> dict:
        if isinstance(data_dict, dict):
            if all(not isinstance(value, dict) for value in data_dict.values()):
                return list(data_dict.keys())
            else:
                return {key: FlagDict.data_dict_to_key_dict(value) for key, value in data_dict.items()}
        return data_dict


            
