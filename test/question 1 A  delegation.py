from abc import ABCMeta, abstractmethod

    
class Dimension(metaclass=ABCMeta):    # 次元のインターフェイス
    @abstractmethod
    def print_dimension(self):
        raise NotImplementedError()

class Shape(metaclass=ABCMeta):   # 図形のインターフェイス
    @abstractmethod
    def print_shape(self):
        raise NotImplementedError()
    @abstractmethod
    def print_dimension(self):
        raise NotImplementedError()
    

class Dimension2D(Dimension):    # 2Dの次元
    def print_dimension(self):
        print('This is a 2D object')
        
class Dimension3D(Dimension):    # 3Dの次元
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
    data = Cube(Dimension2D())
    data.print_shape()
    data.print_dimension()
    
    data = Globe(Dimension3D())
    data.print_shape()
    data.print_dimension()