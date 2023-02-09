# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

    
class Dimension(metaclass=ABCMeta):    # dimension interface
    @abstractmethod
    def get_infor(self):
        pass


class Shape(metaclass=ABCMeta):   # shape interface
    @abstractmethod
    def get_infor(self):
        pass
    
    
class Globe(Shape):    # globe
    def __init__(self, dimension):
        self.dimension = dimension
        
    def get_infor(self):
        str_dimension = self.dimension.get_infor()
        print('This is a ' + str_dimension + ' Globe')
        
    
class Cube(Shape):    # cube
    def __init__(self, dimension):
        self.dimension = dimension
        
    def get_infor(self):
        str_dimension = self.dimension.get_infor()
        print('This is a ' + str_dimension + ' Cube')  
    
    
class Dimension2D(Dimension):    # 2D dimension
    def get_infor(self):
        return '2 dimensional'
        
        
class Dimension3D(Dimension):    # 3D dimension
    def get_infor(self):
        return '3 dimensional'
    
    
if __name__ == '__main__':
    data = Cube(Dimension2D())
    data.get_infor()
    
    data = Globe(Dimension3D())
    data.get_infor()