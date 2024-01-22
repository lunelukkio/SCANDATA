# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""

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
