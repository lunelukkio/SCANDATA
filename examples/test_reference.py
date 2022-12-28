# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 16:21:15 2022

lunelukkio@gmail.com
"""


class B():
    def __init__(self, x):
        self.b = x
g=1

test2 = B(g)
print(test2.b)
g=2 #新しいオブジェクト
print(test2.b)

g=[1,1]

test2 = B(g)
print(test2.b)
g[0]=2  #元のオブジェクト　IDそのまま
print(test2.b)

g=[2,2]  #新しいオブジェクト　新ID
print(test2.b)

#基本的にID参照
#新オブジェクト作成時のみあらたなIDをつくる 