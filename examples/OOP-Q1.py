# -*- coding: utf-8 -*-

class Shape:
    def __init__(self, dimension, shape):
        self.dimension = dimension
        self.shape = shape
            
    def get_infor(self):
        if self.shape == 'globe':
            if self.dimension == '2D':
                print('This is a 2 dimensional Globe')
            elif self.dimension == '3D':
                print('This is a 3 dimensional Globe')
                
        elif self.shape == 'cube':
            if self.dimension == '2D':
                print('This is a 2 dimensional Cube')
            elif self.dimension == '3D':
                print('This is a 3 dimensional Globe')
    
if __name__ == '__main__':
    data = Shape('2D', 'cube')
    data.get_infor()
    
    data = Shape('3D', 'globe')
    data.get_infor()
    
# Make the same results without "if"