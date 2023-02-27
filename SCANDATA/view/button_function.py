# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 21:04:52 2022


lunelukkio@gmail.com
"""

import tkinter as tk
import tkinter.filedialog
import os


class ButtonFunc:
    def __init__(self, data_window):
        self.data_window = data_window
        
    def file_open(self, *filename):
        if filename == ():
            fullname = FileService.get_fullname()  # This is str filename
            if fullname == None:
                return
            self.__filename = self.create_filename_obj(fullname)
            
            
            
class FileService:
    @staticmethod
    def get_fullname(event=None):
        # open file dialog
        fullname = tk.filedialog.askopenfilename(
            initialdir = os.getcwd(), # current dir
            filetypes=(('Tsm files', '*.tsm'),
                       ('Da files', '*.da'), 
                       ('Axon files', '*.abf'),
                       ('WinCP files', '*.wcp'),
                       ('All files', '*.*'))
                      )
        return fullname
    
  





