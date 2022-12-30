# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 21:04:52 2022


lunelukkio@gmail.com
"""


import tkinter as tk
import tkinter.filedialog
import os


class ButtonFn:
    def __init__(self, controller):
        self.contoller = controller
  
    def open_file(self):
        fullname = self.__get_fullname()
        whole_fullnames = self.__get_whole_fullname(fullname)
        return fullname, whole_fullnames
    
    def open_file_from_list(self):
        fullname = self.__get_fullname()
        
  
    def get_fullname(self, event=None):
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
    
    def get_whole_filenames(self, fullname):
        pass




