# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 22:55:37 2023

@author: lulul
"""
from SCANDATA.model.value_object import RoiVal

x = 1
y = 2
a = x + y
print(a)



class A:
    def __init__(self):
        x = RoiVal(40,40,1,1)
        y = RoiVal(10,10,10,10)
        print(x.data)
        print(y.data)
        
        z = x + y
        print(z)
        
test = A()