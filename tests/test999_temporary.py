# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:48:55 2024

@author: lunel
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets  # 正しい場所から QtWidgets をインポート
import numpy as np

# ランダムなデータの生成
data = np.random.normal(size=100)

# QApplication インスタンスの作成
app = QtWidgets.QApplication([])

# プロットウィンドウの作成とデータのプロット
plot_window = pg.plot(title="Basic plotting example")
plot_window.plot(data, pen='r')

# イベントループを開始
if __name__ == '__main__':
    app.exec_()
