# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 20:58:05 2023

@author: lulul
"""

import scipy.ndimage
import numpy as np
scipy.ndimage.correlate(A, B, mode='constant').transpose()