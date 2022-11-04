# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:37:41 2022

@author: kenichi_miyazaki
This is the main program
"""
from model_package.model import Model
from view_package.view import View
from controller_package.controller import Controller

class Main:
    def __init__(self):
        print('start the program')


        self.scandata_model = Model()
        self.scandata_view = View()
        self.scandata_controller = Controller()
        
        self.scandata_view.model = self.scan_model
        self.scandata_view.controller = self.scandata_controller
        
        self.scandata_controller.model = self.scandata_model
        self.scandata_controller.view = self.scandata_view

        
        
        print('SCANDATA End')


if __name__ == '__main__':
    scandata = Main()
