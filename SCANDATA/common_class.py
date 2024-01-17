# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:42:38 2023

@author: lunelukkio@gmail.com
"""

import os
import glob

        
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
        self._observers = []
        self._key_dict = {"CONTROLLER": [], "FILENAME": [], "CH": [], "MOD": []}

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._key_dict)
            
    def set_data_key(self, dict_key, key):       
        if key in self.__view_dict[dict_key]:
            self.__view_dict[dict_key].remove(key)
            print(f"Deleted view data {key} in {dict_key}")
        elif key not in self.__view_dict[dict_key]:
            self.__view_dict[dict_key].append(key)
            print(f"Added view data {key} in {dict_key}")
        self._notify()
        
    @property
    def observers(self):
        return self._observers
    
    @property
    def key_dict(self):
        return self._key_dict


class ViewDataDict(dict):  # observer
    def update(self, keys):
        # delete a key
        for key in list(self.keys()):
            if key not in keys:
                del self[key]
        # add a new key without changing
        for key in keys:
            self.setdefault(key, self.get(key))  # None or key value (bool)

class ViewData:
    def __init__(self):
        user_controller_dict = {}  # {key: bool}
        filename_dict = {}  # {key: bool}
        ch_dict = {}  # {key: bool}
        self.__view_dict = {"CONTROLLER": user_controller_dict,
                            "FILENAME": filename_dict, 
                            "CH": ch_dict}
        
    def set_view_data(self, dict_key, key, val=True):       
        if key in self.__view_dict[dict_key]:
            del self.__view_dict[dict_key][key]
            print(f"Deleted view data {key} in {dict_key}")
        elif key not in self.__view_dict[dict_key]:
            self.__view_dict[dict_key][key] = True
            print(f"Added view data {key} in {dict_key}")

    def set_view_data_val(self, key, val=None):
        if key in self.__view_dict["CONTROLLER"]:
            sub_dict = self.__view_dict["CONTROLLER"]
        elif key in self.__view_dict["FILENAME"]:
            sub_dict = self.__view_dict["FILENAME"]
        elif key in self.__view_dict["CH"]:
            sub_dict = self.__view_dict["CH"]
        else:
            raise Exception("No key in the view data dict")
        if val is not None:
            sub_dict[key] = val
        else:
            sub_dict[key] = not sub_dict[key]
            
    def get_view_data_val(self, key):
        if key in self.__view_dict["CONTROLLER"]:
            view_switch = self.__view_dict["CONTROLLER"][key]
        elif key in self.__view_dict["FILENAME"]:
            view_switch = self.__view_dict["FILENAME"][key]
        elif key in self.__view_dict["CH"]:
            view_switch = self.__view_dict["CH"][key]
        else:
            raise Exception("No key in the view data dict")
        return view_switch

    @property
    def view_dict(self):
        return self.__view_dict



# キーセットにオブザーバーとして辞書を追加
key_set.add_observer(dict1)
key_set.add_observer(dict2)

# キーセットにキーを追加して、辞書に異なる値を設定
key_set.add_key("key1")
dict1["key1"] = "value1"
dict2["key1"] = "different value1"

# キーセットからキーを削除
key_set.remove_key("key1")

# 辞書の状態を確認
print(dict1)  # {}
print(dict2)  # {}
        