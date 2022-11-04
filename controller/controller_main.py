# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:45:37 2022

lunelukkio@gmail.com
main for controller
"""

from model.model import ModelMain
from view.view import ViewMain
from model.experimentdata_factory import TmsDataFactory

class Controller:
    def __init__(self):
        print('Imported controller')
        

        self.filename = 'no file'
        self.filepath = 'no file'

        
        self.model = Model.ModelMain(self.filename, self.filepath)     #test code
        self.view = View.View(self)
        
        self.filename = self.view.main.filename
        
        print(self.filename)
        print('Controller End')
        

    
    def main(self):
        self.view.main()
        
    def roi_controller(self):
        print('ROI controller')