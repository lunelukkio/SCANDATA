# -*- coding: utf-8 -*-

class Shape:
    def __init__(self, dimension, shape):
        self.dimension = dimension
        self.shape = shape
            
    def get_infor(self):
        if self.dimension == '2D':
            str_dimension = '2 dimensional'
        elif self.dimension == '3D':
            str_dimension = '3 dimensional'
            
        if self.shape == 'globe':
            print('This is a ' + str_dimension + ' Globe')
                
        elif self.shape == 'cube':
            print('This is a ' + str_dimension + ' Cube')
    
if __name__ == '__main__':
    data = Shape('2D', 'cube')
    data.get_infor()
    
    data = Shape('3D', 'globe')
    data.get_infor()
    
# Make the same results without "if"