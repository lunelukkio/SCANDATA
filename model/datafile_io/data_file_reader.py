# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:11:22 2022

lunelukkio@gmail.com
"""

import numpy as np

class TmsFileReader:
    def __init__(self, filename, filepath):
        self.filename = filepath + filename
        self.header = 0
        self.file_read()

    def file_read(self):
        with open(self.filename, 'rb') as f:
            b = f.read(2880)
            self.header = b.decode()

    def print_header(self):
        print(self.header)


if __name__ == '__main__':

    filename = ''
    filepath = 'E:\\Data\\2022\\221014\\21014A001.tsm'
    test =TsmFileReader(filename, filepath)
    test.print_header()
    

