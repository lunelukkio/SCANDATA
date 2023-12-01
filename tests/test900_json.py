# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:55:57 2023

@author: lunel
"""

import json

scandata_setting = {
    "color_ch": {"FULL": "black", 
                  "CH1": "red", 
                  "CH2": "blue"},
    "color_roi" : {"ROI1": "black", 
                    "ROI2": "red", 
                    "ROI3": "blue", 
                    "ROI4": "green", 
                    "ROI5": "purple", 
                    "ROI6": "brown", 
                    "ROI7": "pink", 
                    "ROI8": "olive", 
                    "ROI9": "cyan", 
                    "ROI10": "orange"}
    }


json_data = json.dumps(scandata_setting, indent=4)

print(json_data)

with open("scandata_setting.json", "w") as json_file:
    json_file.write(json_data)