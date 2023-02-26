# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:30:22 2023

lunelukkio@gmail.com
"""
import numpy as np

np_data = np.arange(1, 11)

print(np_data[1])

b = np_data[1:5]
print(b)

d = np_data/2
print(d)
print(type(d[1]))