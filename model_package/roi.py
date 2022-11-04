# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:11:48 2022

lunelukkio@gmail.com
"""

class Roi:
    def __init__(self):
        self.x = 40
        self.y = 40
        self.x_length = 3
        self.y_length = 3
        self.dif_base = 50
        self.dif_base_length = 5
        self.ave_num_cell_image = [0,4]  # [start frame, end frame]
        self.dif_df = 100
        self.dif_df_length = 5
        self.mod_list = [list]
        
    def make_roi(self):
        pass
    
    def delete_roi(self):
        pass
        