# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:39:55 2022
This is the main module for a model called by a controller
lunelukkio@gmail.com

"""

from abc import ABCMeta, abstractmethod
import re  # call regular expression
import pprint
from model_package.roi import Roi, TimeWindow, FrameShift, Line
from model.data_factory import TsmFileIO
from model.data_factory import FullFrameFactory, ChFrameFactory
from model.data_factory import CellImageFactory, DifImageFactory
from model.data_factory import ElecTraceFactory, FullTraceFactory, ChTraceFactory

class DataSet():
    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder
    
    print("Standard basic product: ")
    director.build_minimal_viable_product()
    builder.product.list_parts()

    print("\n")

    print("Standard full featured product: ")
    director.build_full_featured_product()
    builder.product.list_parts()

    print("\n")

    # Remember, the Builder pattern can be used without a Director class.
    print("Custom product: ")
    builder.produce_part_a()
    builder.produce_part_b()
    builder.product.list_parts()
    
class Builder(metaclass=ABCMeta):
    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def crete_file_io(self) -> None:
        pass

    @abstractmethod
    def create_data(self) -> None:
        pass

    @abstractmethod
    def create_model_controller(self) -> None:
        pass


class TsmFileBuilder(Builder):
    def __init__(self):
        self.reset()
        
    def reset(self) -> None:
        self._tsm_file = TsmFile()
        
    @property
    def tsm_file(self) -> TsmFile:
        product = self._tsm_file
        self.reset()
        return product
    
    def file_io(self) -> None:
        self._product.add("PartA1")

    def produce_part_b(self) -> None:
        self._product.add("PartB1")

    def produce_part_c(self) -> None:
        self._product.add("PartC1")
        
        
class TsmFile():  # Product
    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"Product parts: {', '.join(self.parts)}", end="")
        
class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder
        
    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()
        self.builder.produce_part_a()
    
    
if __name__ == '__main__':
    pass
    


    
    

