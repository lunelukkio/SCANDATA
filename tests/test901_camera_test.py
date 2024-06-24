# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
import pco
import sys
from PyQt5 import QtCore

class CameraWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CameraWindow, self).__init__(parent)
        self.camera_status = "off"
        
        self.cam = pco.Camera()
        print(self.cam.is_color)
        
        self.cam.default_configuration()
        self.cam.configuration = {'exposure time': 10e-3,
                                  'roi': (1, 1, 2048, 2048),
                                  'delay time': 0,
                                  'trigger': 'auto sequence',
                                  'acquire': 'auto',
                                  'noise filter': 'on',
                                  'binning': (1, 1)}
        
        print(self.cam.configuration)
        
        self.cam.record(mode="sequence non blocking")
        
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.view = pg.GraphicsLayoutWidget()
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

            if self.camera_status == "off":
                print("rrrrrrrrrrrrrrrrrrrrr")
                self.camera_status = "on"
                self.timer.start(50) 
            elif self.camera_status == "on":
                print("weeeeeeeeeeeeeeeeeer")
                self.timer.stop()
                self.cam.stop()
                self.camera_status = "off"
        else:
            super().keyPressEvent(event)



def main():
    app = QtWidgets.QApplication(sys.argv)
    win = CameraWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
