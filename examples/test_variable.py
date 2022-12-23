# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 23:00:57 2022

@author: lulul
"""

class Model:
    def __init__(self, filename):
        self.container_filename = filename
        self.container_filename = DataContainer(filename)

        #self.A001 = DataContainer(filename)
        #self.A002 = DataContainer(filename)
        #実質的にこのようになってほしい

class DataContainer:
    def __init__(self, filename):
        self.filename = filename

#このクラスに
filename = "A001"
test = Model(filename)
filename = "A002"
test = Model(filename)
#のようにクラスへ渡す引数名でインスタンスをnewしていきたいのですが、可能でしょうか？
filename = "A001"
print(test.container_filename.filename)
filename = "A003"
print(test.container_filename.filename)
#のように参照したいです。