# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""
import torch
print("pytorch version")
print(torch.__version__)
print("available")
print(torch.cuda.is_available())
print("device count")
print(torch.cuda.device_count())
print("current divice")
print(torch.cuda.current_device())
print("device name")
print(torch.cuda.get_device_name())
print("cdevice capability")
print(torch.cuda.get_device_capability())
