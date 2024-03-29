# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""

from pyoptools.all import *

class test:
    def __init__(self):
        L=library.Edmund.get("32475")
        SEN=CCD(size=(20,20))
        R=parallel_beam_c(origin=(0.0, 0.0, 0.0), direction=(0.0, 0.0, 0.0),
                  size=(10, 10), num_rays=(5, 5), wavelength=0.58929)
        S=System(complist=[(L,(0,0,50),(0,0,0)),(SEN,(0,0,150),(0,0,0))],n=1)
        Plot3D(S)
        print("Done")
  

if __name__ == '__main__':
    mainWin = test()
