# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 17:15:51 2023

lunelukkio@gmail.com
"""

class A:
    def __init__(self):
        self.x = 1
        
class B:
    def __init__(self):
        self.x=5

if __name__ == "__main__":
    
    test = None
    print(id(test))
    test = A()
    print(id(test))
    print(test.x)    
    test = B()
    print(id(test)) 
    print(test.x)    
    test = None
    print(id(test))  
    test = A()
    print(id(test)) 
    print(test.x)    
    test = B()
    print(id(test))    
    print(test.x)   
    
    print('')

    #test = None
    #print(id(test))
    test = A()
    print(id(test))
    print(test.x)    
    test = B()
    print(id(test)) 
    print(test.x)    
    #test = None
    #print(id(test))  
    test = A()
    print(id(test)) 
    print(test.x)    
    test = B()
    print(id(test))    
    print(test.x) 