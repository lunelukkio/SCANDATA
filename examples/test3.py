from abc import ABCMeta, abstractmethod

class Object_factroy(metaclass=ABCMeta):
    @abstractmethod
    def create_Dimansion2D_factory(self):
        pass
    
    @abstractmethod
    def create_Dimansion3D_factory(self):
        pass

class Dimension2D_factory(Object_factroy):
    return 
    
    
    
class Dimension(metaclass=ABCMeta):    # 次元のインターフェイス
    @abstractmethod
    def print_dimension(self):
        pass
    
    @abstractmethod
    def print_shape(self):
        pass

class Shape(metaclass=ABCMeta):   # 図形のインターフェイス
    @abstractmethod
    def print_shape(self):
        pass
    
""" dimension """
class Dimension2D(Dimension):    # 2Dの次元
    def __init__(self, shape):
        self.shape = shape
        
    def print_shape(self):
        self.shape.print_shape()
        
    def print_dimension(self):
        print('This is a 2D object')
        
class Dimension3D(Dimension):    # 3Dの次元
    def __init__(self, shape):
        self.shape = shape
        
    def print_dimension(self):
        print('This is a 3D object')
        
    def print_shape(self):
        self.shape.print_shape()
    
    
""" shape """  
class Globe(Shape):    # 球      
    def print_shape(self):
        print('This is a Globe')       
    
class Cube(Shape):    # 立方体
    def print_shape(self):
        print('This is a Cube')
        
        
class Main():
    def __init__(self, object_factory, shape):
        object_factory.create_demension()
            
            

        data = Dimension2D(Globe())
        data.print_shape()
        data.print_dimension()
        
        data = Dimension3D(Cube())
        data.print_shape()
        data.print_dimension()
        
    
if __name__ == '__main__':
    test = Main()

    
