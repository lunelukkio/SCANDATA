from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import random

"Frontend"
class Frontend():        
    def plot_data1(self, data):
        data = data.get_data()
        plt.plot(data[1], data[0])
        print(type(data))

    def plot_data2(self, data):
        data = data.get_data()
        plt.plot(data.time, data.raw_data) 
        print(type(data))
        
    def plot_data3(self, data):
        obj_data = data.get_data()
        plt.plot(obj_data.data.time, obj_data.data.raw_data) 
        print(type(data))


"Backend"
class Interface(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self):
        pass


class Primitive(Interface):
    def __init__(self):
        self.__data = Data()
        
    def get_data(self):
        return self.__data.raw_data, self.__data.time  # primitive data
    
    
class Value(Interface):
    def __init__(self):
        self.__data = Data()
        
    def get_data(self):
        return self.__data  # value object


class Object(Interface):
    def __init__(self):
        self.__data = Data()
        
    @property
    def data(self):
        return self.__data
  
    def get_data(self):
        return self  # object


"Value Object"
class Data():
    def __init__(self):
        self.__raw_data = [random.randint(0, 10) for i in range(100)]
        self.__time = np.linspace(1, 100, 100)

    @property
    def raw_data(self):
        return self.__raw_data
    
    @property
    def time(self):
        return self.__time

if __name__ == '__main__':

    primitive_data = Primitive()
    value_obj = Value()
    object_data = Object()
    front_end = Frontend()
    
    front_end.plot_data1(primitive_data)
    front_end.plot_data2(value_obj)
    front_end.plot_data3(object_data)