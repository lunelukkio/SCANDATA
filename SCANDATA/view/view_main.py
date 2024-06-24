# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:43:13 2022

lunelukkio@gmail.com
main for view
"""


import json
import sys
from SCANDATA.common_class import WholeFilename
from SCANDATA.controller.controller_main import MainController
import PyQt5
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

    
class QtDataWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__main_controller = MainController(self)
        self.setWindowTitle('SCANDATA')
        self.__live_camera_mode = False
        self.__live_camera_view = None


        # import a JSON setting file
        try:
            with open("../setting/data_window_setting.json", "r") as json_file:
                setting = json.load(json_file)
        except:
            with open("./setting/data_window_setting.json", "r") as json_file:
                setting = json.load(json_file)

        # window color, position and size
        self.setStyleSheet("background-color: " + 
                           setting["main_window"]["color"] + 
                           ";")
        self.setGeometry(setting["main_window"]["window_posX"], 
                         setting["main_window"]["window_posY"],
                         setting["main_window"]["geometryX"], 
                         setting["main_window"]["geometryY"])
        
        # set sentral widget
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QtWidgets.QVBoxLayout(centralWidget)
        size = centralWidget.size()

        # image window
        image_ax = pg.ImageView()
        image_ax.ui.histogram.hide()  # hide contrast bar
        image_ax.ui.menuBtn.hide()  # hide a menu button
        image_ax.ui.roiBtn.hide() # hide a ROI button
        view = image_ax.getView()
        view.setBackgroundColor(setting["main_window"]["color"])

        
        self.horizontalSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.verticalSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        trace_ax1 = pg.PlotWidget()
        trace_ax2 = pg.PlotWidget()
        self.verticalSplitter.addWidget(trace_ax1)
        self.verticalSplitter.addWidget(trace_ax2)
        
        trace_ax1.setBackground("white")
        trace_ax2.setBackground("white")
        trace_ax1.getAxis('bottom').setPen(pg.mkPen(color=(0, 0, 0), width=2))
        trace_ax1.getAxis('left').setPen(pg.mkPen(color=(0, 0, 0), width=2))
        trace_ax2.getAxis('bottom').setPen(pg.mkPen(color=(0, 0, 0), width=2))
        trace_ax2.getAxis('left').setPen(pg.mkPen(color=(0, 0, 0), width=2))
        trace_ax2.setLabel('bottom', 'Time (ms)', color='black', size=20, width=2)

        self.horizontalSplitter.addWidget(image_ax)
        self.horizontalSplitter.addWidget(self.verticalSplitter)

        mainLayout.addWidget(self.horizontalSplitter)

        self.horizontalSplitter.setSizes([600, 1000])
        self.verticalSplitter.setSizes([450, 150])
        
        self.__main_controller.add_axes("IMAGE", "IMAGE_AXES", self, image_ax)  # ax_dict["ImageAxes"]
        self.__main_controller.add_axes("TRACE", "FLUO_AXES",self, trace_ax1)
        self.__main_controller.add_axes("TRACE", "ELEC_AXES",self, trace_ax2)
        
        # main buttons
        bottom_btn_layout = QtWidgets.QHBoxLayout(centralWidget)
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        # check boxes
        self.live_view_checkbox = QtWidgets.QCheckBox("Live View")
        self.live_view_checkbox.setChecked(False)  # default
        if self.__live_camera_mode == True:
            self.live_view_checkbox.stateChanged.connect(lambda: self.__live_camera_view.start_live_view())
        mainLayout.addWidget(self.live_view_checkbox)
        
        load_btn = QtWidgets.QPushButton("Load...")
        load_btn.setFixedSize(30, 30)
        bottom_btn_layout.addWidget(load_btn, alignment=QtCore.Qt.AlignLeft)
        load_btn.clicked.connect(lambda: self.open_file())

        large_btn = QtWidgets.QPushButton("Large")
        large_btn.setFixedSize(100, 30)
        bottom_btn_layout.addWidget(large_btn, alignment=QtCore.Qt.AlignLeft)
        large_btn.clicked.connect(lambda: self.roi_size("large"))
        
        small_btn = QtWidgets.QPushButton("Small")
        small_btn.setFixedSize(100, 30)
        bottom_btn_layout.addWidget(small_btn, alignment=QtCore.Qt.AlignLeft)
        small_btn.clicked.connect(lambda: self.roi_size("small"))
        bottom_btn_layout.addSpacerItem(spacer)
        
        mainLayout.addLayout(bottom_btn_layout)
        
        if self.__live_camera_mode == True:
            # override with live camera view
            from SCANDATA.controller.controller_live_view import PcoPanda
            self.__live_camera_view = PcoPanda() 
            self.__live_camera_view.set_axes(image_ax)
            """
            try:
                from SCANDATA.controller.controller_live_view import PcoPanda
                self.__live_camera_view = PcoPanda() 
                self.__live_camera_view.set_axes(image_ax)
                except:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("Failed to find a live camera!")
                    print("")
            """
        

        # mouse click event
        image_ax.getView().scene().sigMouseClicked.connect(lambda event: self.__main_controller.onclick_axes(event, "IMAGE_AXES"))
       
        
       
    def open_file(self, filename_obj=None):
        self.__main_controller.open_file(filename_obj)  # make a model and get filename obj
        self.__main_controller.update()
        self.__main_controller.print_infor()
        

        # set image view update. No need!!!!!!
        self.__main_controller.update_flag_lock_sw("IMAGE_AXES", False)
        self.__main_controller.update_flag_lock_sw("FLUO_AXES", False)
        self.__main_controller.update_flag_lock_sw("ELEC_AXES", False)
        
    def open_file(self, filename_obj=None):
        self.__main_controller.open_file(filename_obj)  # make a model and get filename obj
        self.__main_controller.update()
        self.__main_controller.print_infor()

        # set image view update. No need!!!!!!
        self.__main_controller.update_flag_lock_sw("IMAGE_AXES", False)
        self.__main_controller.update_flag_lock_sw("FLUO_AXES", False)
        self.__main_controller.update_flag_lock_sw("ELEC_AXES", False)
        
    def live_view(self):
        self.__live_camera_view.start_live_view()

    def roi_size(self, command):
        if command == "large":
            val = [None, None, 1, 1]
        elif command == "small":
            val = [None, None, -1, -1]
        self.__main_controller.change_roi_size(val)



if __name__ == '__main__':
    fullname = '..\\..\\220408\\20408B002.tsm'
    filename_obj = WholeFilename(fullname)
    
    scandata = PyQt5.QtWidgets.QApplication(sys.argv)
    mainWindow = QtDataWindow()
    mainWindow.open_file(filename_obj)
    mainWindow.show()
    
    if sys.flags.interactive == 0:
        scandata.exec_()
    
    
    print("＝＝＝to do list＝＝＝")
    print("second trace time shift ")
    print("make dF/F mod")
    print("fix re-open method")
    print("make difference image functions")
    print("data_strage_dict shold have {filename:{controller_key:{data_key:ValueData}}}")
    print("")