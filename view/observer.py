# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 13:41:11 2022

lunelukkio@gmail.com
observer for model
"""

import abc

class Subject:    # this should be in Model
    def __init__(self):
        self._observers = set() #make empty set([])
        
    def attach(self, observer):
        self._observers.add(observer)
        
    def detach(self, observer):
        self._observers.discard(observer)
        
    def _notify_update(self, message):
        for observer in self._observers:
            observer.update(message)
            
            
#view
class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, message):
        pass
    
        

class MainWindow(Observer): # these should be in View
    def update(self, message):
        print(f"MainWindow: {message}")

class ElectricalWindow(Observer):
    def update(self, message):
        print(f"ElectricalWindow: {message}")
        
class BaselineWindow(Observer):
    def update(self, message):
        print(f"BasslineWindow: {message}")
        
class DifferenceWindow(Observer):
    def update(self, message):
        print(f"DifferenceWindow: {message}")


def main():
    subject = Subject()
    
    main = MainWindow()
    elec = ElectricalWindow()
    base = BaselineWindow()
    
    subject.attach(main)
    subject.attach(elec)
    
    subject._notify_update("First message")
    
    subject.detach(main)
    subject.attach(base)
    
    subject._notify_update("Second message")
                          

if __name__ == "__main__":
    main()
