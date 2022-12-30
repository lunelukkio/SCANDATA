# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 21:04:52 2022


lunelukkio@gmail.com
"""


import tkinter as tk
import tkinter.filedialog
import os
import glob


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
        filename = os.path.basename(fullname)
        pre_filename = os.path.splitext(filename)
        file_name_no_ext = pre_filename[0]
        extension =  pre_filename[1]
        pre_filepath = os.path.dirname(fullname)
        path = os.path.join(pre_filepath) + os.sep  # replace separater for each OS
        
        find =  path + file_name_no_ext[0:-3] + '*' + str(extension)
        print(find)
        whole_fullname_list = glob.glob(find)
        whole_filename_list = []
        for i in range(len(whole_fullname_list)):
            whole_filename_list.append(os.path.basename(whole_fullname_list[i]))
        return  whole_filename_list




