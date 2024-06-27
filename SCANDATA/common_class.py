# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:42:38 2023

@author: lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod
import os
import sys
import glob
import copy
import re
try:
    from PyQt5.QtWidgets import QFileDialog, QApplication
except:
    import tkinter as tk

class FileService:
    def open_file(self, *filename):  # it can catch variable num of filenames.
        if filename == ():
            fullname = self.get_fullname()  # This is str filename
            if fullname == None:
                print("No filename.")
                return
            new_full_filename = fullname
        else:
            new_full_filename = filename
        return WholeFilename(new_full_filename)
    
    # Function to rename multiple files: https://www.youtube.com/watch?v=uhpnT8hGTnY&t=511s
    def rename_files(self):
        folder_path = "C:/Users/lunel/Documents/python/nnUNetFrame/testfolder"
        for count, filename in enumerate(sorted(os.listdir(folder_path))):
            dst = "ABD_" + str(count).zfill(3) + ".nii.gz"
            src = f"{folder_path}/{filename}"  # foldername/filename, if .py file
            dst = f"{folder_path}/{dst}"
            # rename() function will rename all the files
            os.rename(src, dst)
    
    @staticmethod
    def get_fullname(event=None):
        
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)

            fullname, _ = QFileDialog.getOpenFileName(
            None,
            "Open File",
            os.getcwd(),
            "All files (*.*);;"
            "Tsm files (*.tsm);;"
            "Da files (*.da);;"
            "Axon files (*.abf);;"
            "WinCP files (*.wcp)"
            )
        except:
            # open file dialog
            fullname = tk.filedialog.askopenfilename(
                initialdir = os.getcwd(), # current dir
                filetypes=(('All files', '*.*'), 
                           ('Tsm files', '*.tsm'),
                           ('Da files', '*.da'), 
                           ('Axon files', '*.abf'),
                           ('WinCP files', '*.wcp')
                          ))
        return fullname


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
        

class SingletonKeyDict:  # _dict = {"CONTROLLER": ["data_keys"], "CH": ["data_keys"]} 
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


class DataDict(metaclass=ABCMeta):
    def __init__(self):
        self._data_dict = {}
        self._filename_dict = {}

    @abstractmethod
    def update(self, key_dict):
        raise NotImplementedError()

    @abstractmethod
    def set_val(self, controller_key, data_key, val):  # "ALL" in controller and data key is acceptable.
        raise NotImplementedError()
                    
    def update_filename(self, filename_list):
        old_dict = self._filename_dict
        new_dict = {}
        copy_list = copy.deepcopy(filename_list)
        # make a new dict from the keylist
        for filename_key in copy_list:
            if filename_key in old_dict:
                new_dict[filename_key] = old_dict[filename_key]
            else:
                new_dict[filename_key] = True
        self._filename_dict = new_dict
        
    def set_filename_val(self, filename_key, val=None):
        if filename_key not in self._filename_dict:
            print(f"Filename key: {filename_key} doesn't exist.")
        else:
            if val is None:
                self._filename_dict[filename_key] = not self._filename_dict[filename_key]
            else:
                self._filename_dict[filename_key] = val
        
    def get_dict(self):
        return self._data_dict
    
    def get_filename_dict(self):
        return self._filename_dict
    
    def print_infor(self):
        print(f"Data Flags: {self._data_dict}")
        print(f"Filename flags: {self._filename_dict}")
        print("")

    @staticmethod
    def data_dict_to_key_dict(data_dict) -> dict:
        if isinstance(data_dict, dict):
            if all(not isinstance(value, dict) for value in data_dict.values()):
                return list(data_dict.keys())
            else:
                return {key: FlagDict.data_dict_to_key_dict(value) for key, value in data_dict.items()}
        return data_dict

class FlagDict(DataDict):
    def __init__(self):
        super().__init__()
        
    def update(self, key_dict):
        old_dict = self._data_dict  # old_dict = {controller_key:{data_key:boolen}}
        new_dict = {}
        # make a new dict from the key list
        for controller_key, data_list in key_dict.items():  # key_dict = {"CONTROLLER": ["data_keys"], "CH": ["data_keys"]} 
            if data_list is not None:
                # If data_key is in old_dict, just copy, else make True in new data_key
                new_dict[controller_key] = {data_key: old_dict[controller_key][data_key] 
                                            if data_key in old_dict
                                            else True for data_key in data_list}
            else:
                new_dict[controller_key] = None
        self._data_dict = new_dict
        
    def set_val(self, controller_key, data_key, val=None):
        if controller_key == "ALL":
            controllers = self._data_dict.keys()
        elif controller_key in self._data_dict:
            controllers = [controller_key]
        else:
            print(f"Controller key: {controller_key} doesn't exist.")
            return
        
        for target_controller_key in controllers:
            if data_key == "ALL":
                data_keys = self._data_dict[target_controller_key].keys()
            elif data_key in self._data_dict[target_controller_key]:
                data_keys = [data_key]
            else:
                print(f"Data key: {data_key} doesn't exist in {target_controller_key}.")
                continue  # next controller_key
            for target_data_key in data_keys:
                if val is None:
                    self._data_dict[target_controller_key][target_data_key] = not self._data_dict[target_controller_key][target_data_key]
                else:
                    self._data_dict[target_controller_key][target_data_key] = val
                    
    # find only controller keys which have true in ch data.
    def find_true_controller_keys(self, controller=None) -> list:  # e.g. "ROI"
        if controller is None or controller == "ALL":
            return [key for key, value in self._data_dict.items() if any(value.values())]
        else:
            controller = controller.upper()
            true_list = [key for key, value in self._data_dict.items() if any(value.values())]
            return [key for key in true_list if controller in key]
    
    def find_true_ch_keys(self, controller_key) -> list:  # e.g. "ROI"
        return [key for key, value in self._data_dict[controller_key].items() if value]
    
    def find_true_filename_keys(self) -> list:
        return [filename_key 
                for filename_key, bool_val 
                in self._filename_dict.items() 
                if bool_val]
    
    def next_controller_to_true(self, controller):  # e.g. "ROI"
        controller_whole_list = [key for key in self._data_dict.keys() if controller in key]
        controller_true_key_list = self.find_true_controller_keys(controller)
        targeted_controller_key = controller_true_key_list[-1]  # the last key
        if targeted_controller_key in controller_whole_list:
            target_index = controller_whole_list.index(targeted_controller_key)
            if target_index + 1 < len(controller_whole_list):
                next_element = controller_whole_list[target_index + 1]

            else:
                next_element = controller_whole_list[0]
            #print(f"Switch to the next controller = {next_element}")
            ch_list = self.find_true_ch_keys(targeted_controller_key)
            for ch_key in ch_list:
                original_val = self._data_dict[targeted_controller_key][ch_key]
                self._data_dict[targeted_controller_key][ch_key] = False
                self._data_dict[next_element][ch_key] = original_val
        else:
            print(f"There is no {targeted_controller_key}")
            
        
class DataStrageDict(DataDict):
    def __init__(self):
        super().__init__()
        
    def update(self, key_dict):
        old_dict = self._data_dict
        new_dict = {}
        # make a new dict from the key list
        for controller_key, data_list in key_dict.items():
            if data_list is not None: 
                new_dict[controller_key] = {data_key: old_dict[controller_key][data_key] 
                                            if data_key in old_dict
                                            else None for data_key in data_list}
            else:
                new_dict[controller_key] = None
        self._data_dict = new_dict
        
    def set_val(self, controller_key, data_key, val:object):
        if controller_key == "ALL":
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("This method can not use ALL as controller_key.")
        elif controller_key in self._data_dict:
            controllers = [controller_key]
        else:
            print(f"Controller key: {controller_key} doesn't exist.")
            return
        
        for target_controller_key in controllers:
            if data_key == "ALL":
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("This method can not use ALL as data_key.")
            elif data_key in self._data_dict[target_controller_key]:
                data_keys = [data_key]
            else:
                print(f"Data key: {data_key} doesn't exist in {target_controller_key}.")
                continue  # next controller_key
            for target_data_key in data_keys:
                self._data_dict[target_controller_key][target_data_key] = val
    