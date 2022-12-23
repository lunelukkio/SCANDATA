# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:56:12 2022

lunelukkio@gmail.com
"""

from abc import ABCMeta, abstractmethod

class main:
    def __init__(self, factory_type, ):
     dim = factory_type.create_dimension_facroty(Dimension2D())
     shp = factory_type.create_shape_facroty(Globe())

class ObjectFactory(metaclass=ABCMeta):  # Abstract factory
    @abstractmethod
    def create_dimension_factory(self, dimension):
        pass
    
    @abstractmethod
    def create_shape_factory(self, shpae):
        pass
    
    
class AtypeDatasetFactory(ObjectFactory):  # Concrete factory
    def create_dimension_factory(self, dimension):
        return DimensionFactory(dimension)
    
    def create_shape_factory(self, shape):
        return ShapeFactory(shape)


class DimensionFactory(metaclass=ABCMeta):  # Factory method interface
    @abstractmethod
    def create_dimension(self, dimension):
        pass
    
class ShapeFactory(metaclass=ABCMeta):  # Factory method interface
    @abstractmethod
    def create_shape(self, shape):
        pass
    

class Dimension(metaclass=ABCMeta):  # 次元のインターフェイス, Concrete product from an abstract factory
    @abstractmethod
    def print_dimension(self):
        pass

class Shape(metaclass=ABCMeta):  # 図形のインターフェイス, Concrete product from an abstract factory
    @abstractmethod
    def print_shape(self):
        pass
    
    @abstractmethod
    def print_dimension(self):
        pass
    


class Dimension2D(Dimension):    # 2Dの次元, Product from a factory method
    def print_dimension(self):
        print('This is a 2D object')
        
class Dimension3D(Dimension):    # 3Dの次元, Product from a factory method
    def print_dimension(self):
        print('This is a 3D object')
    
    
    
class Globe(Shape):    # 球
    def __init__(self, dimension):
        self.dimension = dimension
        
    def print_shape(self):
        print('This is a Globe')
        
    def print_dimension(self):
        self.dimension.print_dimension()
        
    
class Cube(Shape):    # 立方体
    def __init__(self, dimension):
        self.dimension = dimension
        
    def print_shape(self):
        print('This is a Cube')

    def print_dimension(self):
        self.dimension.print_dimension()   
    
    
if __name__ == '__main__':
    factory_type = AtypeDatasetFactory()
    data = factory_type.create_dimension_facroty(Dimension2D())
    data = factory_type.create_shape_facroty(Globe())
    
    data.print_shape()
    data.print_dimension()
    
    data = factory_type.create_dimension_facroty(Dimension3D())
    data = factory_type.create_shape_facroty(Cube())

    data.print_shape()
    data.print_dimension()