from abc import ABCMeta, abstractmethod

class Shape(metaclass=ABCMeta):   # 図形のインターフェイス
    @abstractmethod
    def print_shape(self):
        pass
    
    def print_dimension(self):
        pass
    
    
class Globe(Shape):
    def __init__(self, dimension):
        self.dimension = dimension
        
    def print_shape(self):
        print('This is a Globe')
        
    def print_dimension(self):
        if self.dimension == 3:
            print('This is a 3D object')
        elif self.dimension == 2:
            print('This is a 2D object')
        
class Cube(Shape):
    def __init__(self, dimension):
        self.dimension = dimension
        
    def print_shape(self):
        print('This is a Cube')
        
    def print_dimension(self):
        if self.dimension == 3:
            print('This is a 3D object')
        elif self.dimension == 2:
            print('This is a 2D object')
        
    
if __name__ == '__main__':
    data = Cube(2)
    data.print_shape()
    data.print_dimension()
    
    data = Globe(3)
    data.print_shape()
    data.print_dimension()
    
# これをif文を使わずに同じ結果を得たい