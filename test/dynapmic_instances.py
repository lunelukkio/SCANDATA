# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:07:27 2022

lunelukkio@gmail.com
"""
class Fluo:
    def __init__(self, slope, num):
        self.num = num
        self.length = len(slope)
        self.name = slope

fluo = []
name = []
for i in range(5):  
    fluo.append(Fluo('type'+ str(i), i))  # make instance
    name.append('type' + str(i))  # make the name of the key for dict

trace = dict(zip(name, fluo))  # convine objects and keys

print(trace['type4'].name)
print(trace['type4'].num)
print(trace['type4'].length)




