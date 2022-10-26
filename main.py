# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:37:41 2022

@author: kenichi_miyazaki
This is the main program
"""

import controller.controller_main as CT

class Main:
    def __init__(self):
        print('start the program')
        self.controller = CT.Controller()

        print('SCANDATA End')


if __name__ == '__main__':
    scandata = Main()
