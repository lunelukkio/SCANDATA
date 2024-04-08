# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 18:49:15 2024

@author: lunel
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
import pco
import sys
from PyQt5 import QtCore


class PcoPanda:
    def __init__(self):
        
        # camera settings
        self.camera_status = "off"
        self.cam = pco.Camera()
        print(self.cam.is_color)
        self.cam.default_configuration()
        self.cam.configuration = {'exposure time': 10e-3,
                                  'roi': (1, 1, 512, 512),
                                  'delay time': 0,
                                  'trigger': 'auto sequence',
                                  'acquire': 'auto',
                                  'noise filter': 'on',
                                  'binning': (2, 2)}
        print(self.cam.configuration)
        self.cam.record(mode="sequence non blocking")
        
    def set_axes(self, view_axes):
        # view settings
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.view = view_axes
        self.layout.addWidget(self.view)
        
        self.plot =self.view.addPlot()
        
        ini_image, meta = self.cam.image()
        self.img = pg.ImageItem(ini_image)
        self.plot.addItem(self.img)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)

    def update(self):
        self.cam.record(mode="sequence")
        data, meta = self.cam.image()
        self.img.setImage(data)
  
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.start_live_view()
        else:
            super().keyPressEvent(event)

    def start_live_view(self):
            if self.camera_status == "off":
                self.camera_status = "on"
                self.timer.start(50) 
            elif self.camera_status == "on":
                self.timer.stop()
                self.cam.stop()
                self.camera_status = "off"

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = PcoPanda()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
