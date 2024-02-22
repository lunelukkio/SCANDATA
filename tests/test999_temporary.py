# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # ウィンドウのタイトルとサイズを設定
        self.setWindowTitle('Image and Plots Example')
        self.setGeometry(100, 100, 800, 600)

        # 中心ウィジェットとレイアウトを作成
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        layout = QtWidgets.QHBoxLayout(centralWidget)

        # 左側の画像表示エリア
        self.imageView = pg.ImageView()
        
        # 右側のプロットエリアを作成するための垂直分割
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.plot1 = pg.PlotWidget(title="Plot 1")
        self.plot2 = pg.PlotWidget(title="Plot 2")
        self.splitter.addWidget(self.plot1)
        self.splitter.addWidget(self.plot2)

        # 水平分割にウィジェットを追加
        layout.addWidget(self.imageView)
        layout.addWidget(self.splitter)

        # デモデータを表示
        self.displayDemoData()

    def displayDemoData(self):
        # デモ画像データ
        imageData = np.random.normal(size=(200, 200))
        self.imageView.setImage(imageData)
        
        # デモプロットデータ
        x = np.arange(100)
        y1 = np.random.normal(size=100)
        y2 = np.random.normal(size=100)
        self.plot1.plot(x, y1)
        self.plot2.plot(x, y2)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
