# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 13:41:11 2022

lunelukkio@gmail.com
C:/Users/kenichi_miyazaki/SCANDATA/view/observer_test.py
"""

import abc

class Subject:
    def __init__(self):
        self._observers = set()
        
    def attach(self, observer):
        self._observers.add(observer)
        
    def detach(self, observer):
        self._observers.discard(observer)
        
    def _notify_update(self, message):
        for observer in self._observers:
            observer.update(message)
            
            
class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self, message):
        pass
    
        

class MessageObserverOne(Observer):
    def update(self, message):
        print(f"Message Observer One: {message}")

class MessageObserverTwo(Observer):
    def update(self, message):
        print(f"Message Observer Two: {message}")
        
class MessageObserverThree(Observer):
    def update(self, message):
        print(f"Message Observer Three: {message}")


def main():
    subject = Subject()
    
    message_one = MessageObserverOne()
    message_two = MessageObserverTwo()
    message_three = MessageObserverThree()
    
    subject.attach(message_one)
    subject.attach(message_two)
    
    subject._notify_update("First message")
    
    subject.detach(message_one)
    subject.attach(message_three)
    
    subject._notify_update("Second message")
                          

if __name__ == "__main__":
    main()
