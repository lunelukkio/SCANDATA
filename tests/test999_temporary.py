# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

class MyImageView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyImageView, self).__init__()
        self.imageView = pg.ImageView()
        self.setCentralWidget(self.imageView)

        # シグナルを接続
        self.imageView.scene().sigMouseClicked.connect(self.onMouseClicked)

    def onMouseClicked(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.scenePos()  # シーン内でのクリック位置
            print(f"Clicked at: {pos}")
            # imageView の座標系に変換する場合は追加の計算が必要になる場合があります。

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mainWin = MyImageView()
    mainWin.show()
    app.exec_()