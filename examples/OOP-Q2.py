# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Shape(metaclass=ABCMeta):   # shape interface
    @abstractmethod
    def get_infor(self):
        pass
    
    
class Globe(Shape):
    def __init__(self, dimension):
        self.dimension = dimension
        
    def get_infor(self):
        if self.dimension == '2D':
            print('This is a 2 dimensional Globe')
        elif self.dimension == '3D':
            print('This is a 3 dimensional Globe')
        
class Cube(Shape):
    def __init__(self, dimension):
        self.dimension = dimension
        
    def get_infor(self):
        if self.dimension == '2D':
            print('This is a 2 dimensional Cube')
        elif self.dimension == '3D':
            print('This is a 3 dimensional Cube')
        
    
if __name__ == '__main__':
    data = Cube('2D')
    data.get_infor()
    
    data = Globe('3D')
    data.get_infor()
    
# Make the same results without "if"