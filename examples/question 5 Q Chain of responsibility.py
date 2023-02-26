# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 21:33:12 2023

@author: lulul
"""

class Client:
    def __init__(self):
        self.color = 'black'

        self.test1 = Test1Handler()
        self.test2 = Test2Handler()
        self.test3 = Test3Handler()
    
        self.test1.set_next(self.test2).set_next(self.test3)
        
    def mod_color(self, key_list):
        for key in key_list:
            self.color = self.test1.apply_mod(key, self.color)
        print(self.color)
    
class Handler:
    def __init__(self):
        self.__next_handler = None

    def set_next(self, next_handler):
        self.__next_handler = next_handler
        return next_handler
    
    def handle_request(self, key, color):
        if self.__next_handler:
            return self.__next_handler.apply_mod(key, color)

class Test1Handler(Handler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, key, color):
        if key == '1red':
            color += ' red'
            return color
        else:
            return super().handle_request(key, color)
        
class Test2Handler(Handler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, key, color):
        if key == '2green':
            color += ' green'
            return color
        else:
            return super().handle_request(key, color)
        
class Test3Handler(Handler):
    def __init__(self):
        super().__init__()
        
    def apply_mod(self, key, color):
        if key == '3blue':
            color += ' blue'
            return color
        else:
            return super().handle_request(key, color)
    
        
if __name__ == '__main__':
    test = Client()
    
    key_list = ['1red', '2green', '3blue']
    sorted_key_list = sorted(key_list)
    test.mod_color(sorted_key_list)
    
    test.color = 'black'
    
    key_list = ['1red', '3blue', '2green']
    sorted_key_list = sorted(key_list)
    test.mod_color(sorted_key_list)